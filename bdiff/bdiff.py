# Copyright (c) [2025] [Lu YAO]
# BDiff is licensed under Mulan PubL v2.
# You can use this software according to the terms and conditions of the Mulan PubL v2.
# You may obtain a copy of Mulan PubL v2 at:
#         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PubL v2 for more details.

"""Core codes of BDiff."""

import copy
import os
import re
import subprocess
from collections import OrderedDict
from pprint import pprint
from typing import Dict, List, Optional, OrderedDict, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment


def levenshtein_ratio(s1: str, s2: str) -> float:
    """
    Calculate normalized Levenshtein similarity ratio between two strings.

    Args:
        s1: First input string
        s2: Second input string

    Returns:
        Similarity ratio in [0,1], where 1 means identical strings.
        Computed as (total_length - edit_distance)/total_length.
    """
    if len(s1) == 0 and len(s2) == 0:
        return 1.0

    dp = np.zeros((len(s1) + 1, len(s2) + 1), dtype=float)
    for i in range(len(s1) + 1):
        dp[i, 0] = i * 1.0
    for j in range(len(s2) + 1):
        dp[0, j] = j * 1.0

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 2.0
            dp[i, j] = min(
                dp[i - 1, j] + 1,
                dp[i, j - 1] + 1,
                dp[i - 1, j - 1] + cost
            )
    distance = dp[len(s1), len(s2)]
    total_length = len(s1) + len(s2)
    return (total_length - distance) / total_length


def W_BESTI_LINE(
        src_line_no: int,
        dest_line_no: int,
        src_lines: list[str],
        dest_lines: list[str],
        ctx_length: int = 4,
        line_sim_weight: float = 0.6,
        sim_threshold: float = 0.5
) -> tuple[bool, float]:
    """
    Calculate line similarity considering both content and context [1].
    [1] Reiss and P. Steven. 2008. Tracking source locations. In ACM/IEEE International Conference on Software Engineering.
11.
    Args:
        src_line_no: Source line number (1-indexed)
        dest_line_no: Destination line number (1-indexed)
        src_lines: List of source lines
        dest_lines: List of destination lines
        ctx_length: Number of context lines to consider
        line_sim_weight: Weight for line content similarity, and (1 - weight) for context similarity
        sim_threshold: Threshold for considering lines as similar

    Returns:
        Tuple of (is_similar, similarity_score)
    """
    if src_lines[src_line_no - 1].strip() == "" and dest_lines[dest_line_no - 1].strip() == "":
        if src_lines[src_line_no - 1] == dest_lines[dest_line_no - 1]:
            return False, 0
        line_sim = 1
    elif not src_lines[src_line_no - 1] or not dest_lines[dest_line_no - 1]:
        return False, 0
    else:
        line_sim = levenshtein_ratio(src_lines[src_line_no - 1].strip(), dest_lines[dest_line_no - 1].strip())

    if src_line_no <= ctx_length:
        src_upper_ctx = src_lines[:src_line_no - 1]
    else:
        src_upper_ctx = src_lines[src_line_no - ctx_length - 1: src_line_no - 1]

    if src_line_no + ctx_length > len(src_lines):
        src_under_ctx = src_lines[src_line_no:]
    else:
        src_under_ctx = src_lines[src_line_no: src_line_no + ctx_length]

    if dest_line_no <= ctx_length:
        dest_upper_ctx = dest_lines[:dest_line_no - 1]
    else:
        dest_upper_ctx = dest_lines[dest_line_no - ctx_length - 1: dest_line_no - 1]

    if dest_line_no + ctx_length >= len(dest_lines):
        dest_under_ctx = dest_lines[dest_line_no:]
    else:
        dest_under_ctx = dest_lines[dest_line_no: dest_line_no + ctx_length]

    upper_group = [group[0].strip() == group[1].strip() for group in zip(src_upper_ctx, dest_upper_ctx)]
    under_group = [group[0].strip() == group[1].strip() for group in zip(src_under_ctx, dest_under_ctx)]

    if len(upper_group) + len(under_group) == 0:
        return True if line_sim >= sim_threshold else False, round(line_sim, 3)

    ctx_sim = (upper_group.count(True) + under_group.count(True)) / (len(upper_group) + len(under_group))
    synthetic_sim = line_sim * line_sim_weight + ctx_sim * (1 - line_sim_weight)
    return True if synthetic_sim >= sim_threshold else False, round(synthetic_sim, 3)


def construct_line_data(diffs: list[tuple[str, str]], indent_tabs_size: int) -> tuple[
        OrderedDict, OrderedDict, list[str]]:
    """
    Construct structured data from diff results.

    Args:
        diffs: List of diff tuples (mode, line_content)
        indent_tabs_size: Number of spaces a tab represents

    Returns:
        Tuple of (source_lines_dict, added_lines_dict, diff_scripts)
    """
    diff_line_dict_src = OrderedDict()
    diff_line_dict_added = OrderedDict()
    a_line_no = 0
    b_line_no = 0
    diff_scripts = []
    hunk = 0
    counting_hunk = False

    for mode, line in diffs:
        if mode == 'k':
            if counting_hunk:
                counting_hunk = False
            a_line_no += 1
            b_line_no += 1
            diff_line_dict_src[a_line_no] = (
                line.lstrip().rstrip('\n'), compute_line_indent(line, indent_tabs_size), 'k')
            diff_scripts.append('k' + str(a_line_no))
        elif mode == 'r':
            if not counting_hunk:
                hunk += 1
                counting_hunk = True
            a_line_no += 1
            diff_line_dict_src[a_line_no] = (
                line.lstrip().rstrip('\n'), compute_line_indent(line, indent_tabs_size), 'r', hunk)
            diff_scripts.append('r' + str(a_line_no))
        elif mode == 'i':
            if not counting_hunk:
                hunk += 1
                counting_hunk = True
            b_line_no += 1
            diff_line_dict_added[b_line_no] = (
                line.lstrip().rstrip('\n'), compute_line_indent(line, indent_tabs_size), 'i', hunk)
            diff_scripts.append('i' + str(b_line_no))

    return diff_line_dict_src, diff_line_dict_added, diff_scripts


def _find_same_left(a: str, b: str, /, min_len: int) -> int:
    """
    Count the number of characters in the maximum left-side matching region of two strings

    Args:
        a: First string
        b: Second string
        min_len: Maximum length to check

    Returns:
        Length of the longest common prefix
    """
    low, high = 0, min_len

    while low < high:
        mid = (low + high) >> 1
        if a[low:mid + 1] == b[low:mid + 1]:
            low = mid + 1
        else:
            high = mid

    return low


def _find_diff_area(a: str, b: str, /) -> tuple[int, int]:
    """
    Find the differing regions between two strings.

    Args:
        a: First string
        b: Second string

    Returns:
        Tuple of (left_common_length, right_common_length)
    """
    min_len = min(len(a), len(b))

    left = _find_same_left(a, b, min_len)
    right = _find_same_left(a[::-1], b[::-1], min_len)

    return left, min(right, min_len - left)


def find_diff_area(a: str, b: str, /) -> list[list[list[int]] | list]:
    """
    Identify non-matching regions between two strings.

    Args:
        a: First string
        b: Second string

    Returns:
        List of non-matching regions in [start, end) format
    """
    start, end = _find_diff_area(a, b)

    area_a = [start, len(a) - end - 1]
    area_b = [start, len(b) - end - 1]

    if area_a[0] > area_a[1]:
        area_a = []

    if area_b[0] > area_b[1]:
        area_b = []

    return [[area_a], [area_b]]


def construct_str_diff_data(src_tuple: tuple, dest_tuple: tuple) -> list[list[list[int]]]:
    """
    Construct difference data for string comparison.

    Args:
        src_tuple: Source string data tuple
        dest_tuple: Destination string data tuple

    Returns:
        List of difference regions
    """
    left_range, right_range = find_diff_area(src_tuple[0], dest_tuple[0])
    if not left_range[0] and not right_range[0]:
        left_range[0].append(0)
        left_range[0].append(src_tuple[1][1] + src_tuple[1][2] - 1)
        right_range[0].append(0)
        right_range[0].append(dest_tuple[1][1] + dest_tuple[1][2] - 1)
        return [left_range, right_range]

    if left_range[0]:
        left_range[0][0] = left_range[0][0] + src_tuple[1][1] + src_tuple[1][2]
        left_range[0][1] = left_range[0][1] + src_tuple[1][1] + src_tuple[1][2]

    if right_range[0]:
        right_range[0][0] = right_range[0][0] + dest_tuple[1][1] + dest_tuple[1][2]
        right_range[0][1] = right_range[0][1] + dest_tuple[1][1] + dest_tuple[1][2]

    return [left_range, right_range]


def compute_line_indent(diff_line: str, indent_tabs_size: int) -> tuple[int, int, int]:
    """
    Calculate indentation information for a line.

    Args:
        diff_line: Line to analyze
        indent_tabs_size: Number of spaces a tab represents

    Returns:
        Tuple of (total_indent, space_count, tab_count)
    """
    if diff_line.startswith(" ") or diff_line.startswith("\t"):
        if diff_line.lstrip() == "":
            first_chara_index = len(diff_line) + 1
        else:
            first_chara_index = diff_line.find(diff_line.lstrip()[0])

        n_spaces = diff_line[:first_chara_index].count(" ")
        n_tabs = diff_line[:first_chara_index].count("\t")
        return n_spaces + n_tabs * indent_tabs_size, n_spaces, n_tabs
    else:
        return 0, 0, 0


def is_pure_punctuation(s: str) -> bool:
    """
    Check if a string contains only punctuation characters.

    Args:
        s: String to check

    Returns:
        True if string is pure punctuation, False otherwise
    """
    if not s:
        return True
    pattern = r'^[~`!@#$%^&*()-_+={}\[\]|\\:;"\'<,>.?/\n\s]+$'
    return bool(re.match(pattern, s))


def pure_block_len(
        block_length: int,
        src_start: int,
        src_lines_list: list[str],
        added_start: int,
        added_lines_list: list[str],
        pure_mv_block_contain_punc: bool,
        pure_cp_block_contain_punc: bool,
        mode: str
) -> int:
    """
    Calculate effective block length excluding pure punctuation lines.

    Args:
        block_length: Total block length
        src_start: Starting line in source
        src_lines_list: List of source lines
        added_start: Starting line in destination
        added_lines_list: List of destination lines
        pure_mv_block_contain_punc: Whether to include punctuation in move blocks
        pure_cp_block_contain_punc: Whether to include punctuation in copy blocks
        mode: Block mode ('r' for move, 'k' for copy)

    Returns:
        Effective block length
    """
    i = 0
    pure_block_length = block_length
    while i < block_length:
        if not src_lines_list[src_start - 1] and not added_lines_list[added_start - 1]:
            pure_block_length -= 1
        elif ((not pure_mv_block_contain_punc and mode == 'r') or (
            not pure_cp_block_contain_punc and mode == 'k')) and is_pure_punctuation(
                src_lines_list[src_start - 1]) and is_pure_punctuation(added_lines_list[added_start - 1]):
            pure_block_length -= 1
        src_start += 1
        added_start += 1
        i += 1
    return pure_block_length


def mapping_block_move(
        src_lines: OrderedDict,
        added_lines: OrderedDict,
        src_all_lines: list[str],
        dest_all_lines: list[str],
        min_block_length: int,
        diff_scripts: list[str],
        pure_mv_block_contain_punc: bool,
        count_mv_block_update: bool
) -> list[dict]:
    """
    Identify candidate moved blocks between source and destination.

    Args:
        src_lines: Source lines dictionary
        added_lines: Added lines dictionary
        src_all_lines: All source lines
        dest_all_lines: All destination lines
        min_block_length: Minimum block length to consider
        diff_scripts: List of diff scripts
        pure_mv_block_contain_punc: Whether to count punctuation lines when calculating move block length
        count_mv_block_update: Whether to include line updates in moved blocks

    Returns:
        List of potential move mappings
    """
    mappings = []
    checked_dict = {}

    for added_line in added_lines:
        if added_lines[added_line][0] == "":
            continue

        for src_line in src_lines:
            if src_lines[src_line][0] == "" or (src_line, added_line) in checked_dict or src_lines[src_line][2] == "k":
                continue

            checked_dict[(src_line, added_line)] = True
            cur_src_line_no = src_line
            cur_added_line_no = added_line
            indent_diff = added_lines[added_line][1][0] - src_lines[src_line][1][0]
            src_mode = "r"
            block_length = 0
            pure_block_length = 0
            edit_actions = 2
            m_updates = []

            while (cur_src_line_no in src_lines and
                   cur_added_line_no in added_lines and
                   src_lines[cur_src_line_no][2] == src_mode and
                   (src_lines[cur_src_line_no][0] == added_lines[cur_added_line_no][0] or
                    (src_lines[cur_src_line_no][0] != added_lines[cur_added_line_no][0] and
                     count_mv_block_update and
                     levenshtein_ratio(src_lines[cur_src_line_no][0], added_lines[cur_added_line_no][0]) >= 0.6)) and
                   ((added_lines[cur_added_line_no][0] != "" and
                     added_lines[cur_added_line_no][1][0] - src_lines[cur_src_line_no][1][0] == indent_diff) or
                    added_lines[cur_added_line_no][0] == "")):

                if count_mv_block_update and src_lines[cur_src_line_no][0] != added_lines[cur_added_line_no][0]:
                    edit_actions += 1
                    m_updates.append([cur_src_line_no, cur_added_line_no])

                if src_lines[cur_src_line_no][0] != "" and added_lines[cur_added_line_no][0] != "":
                    if pure_mv_block_contain_punc or not (
                            is_pure_punctuation(src_lines[cur_src_line_no][0]) and
                            is_pure_punctuation(added_lines[cur_added_line_no][0])):
                        pure_block_length += 1

                checked_dict[(cur_src_line_no, cur_added_line_no)] = True
                cur_src_line_no += 1
                cur_added_line_no += 1
                block_length += 1

            if (pure_block_length >= min_block_length and
                    not is_pure_punctuation(
                        "".join([src_lines[line][0] for line in range(src_line, src_line + block_length)]))):

                cur_src_line_no = src_line - 1
                cur_added_line_no = added_line - 1

                while cur_src_line_no >= 1 and cur_added_line_no >= 1:
                    if (cur_src_line_no in src_lines and
                            cur_added_line_no in added_lines and
                            src_lines[cur_src_line_no][2] == src_mode and
                            src_lines[cur_src_line_no][0] == "" and
                            added_lines[cur_added_line_no][0] == ""):

                        src_line = cur_src_line_no
                        added_line = cur_added_line_no
                        block_length += 1
                        cur_src_line_no -= 1
                        cur_added_line_no -= 1
                    else:
                        break

                ctx_similarity = context_similarity(src_line, added_line, block_length, src_all_lines, dest_all_lines)

                if src_lines[src_line][3] == added_lines[added_line][3]:
                    move_type = "h"
                elif src_lines[src_line][3] < added_lines[added_line][3]:
                    move_type = "d"
                else:
                    move_type = "u"

                if move_type == 'h' and indent_diff == 0:
                    continue

                if indent_diff != 0 and move_type != "h":
                    edit_actions += 1

                rd = relative_distance(src_line, added_line, block_length, diff_scripts)
                candidate = {
                    "mode": src_mode,
                    "block_length": block_length,
                    "src_start": src_line,
                    "added_start": added_line,
                    "context_similarity": ctx_similarity,
                    "weight": (edit_actions / block_length + (1 - ctx_similarity) / 10 + rd / 100),
                    "move_type": move_type,
                    "updates": m_updates,
                    "indent_diff": indent_diff,
                    "edit_actions": edit_actions,
                    "relative_distance": rd
                }

                mappings.append(candidate)

    return mappings


def mapping_block_copy(
        src_lines: OrderedDict,
        added_lines: OrderedDict,
        src_all_lines: list[str],
        dest_all_lines: list[str],
        min_copy_block_length: int,
        hunks: list,
        diff_scripts: list[str],
        pure_cp_block_contain_punc: bool,
        count_cp_block_update: bool
) -> list[dict]:
    """
    Identify candidate copied blocks between source and destination.

    Args:
        src_lines: Source lines dictionary
        added_lines: Added lines dictionary
        src_all_lines: All source lines
        dest_all_lines: All destination lines
        min_copy_block_length: Minimum copy block length
        hunks: List of diff hunks
        diff_scripts: List of diff scripts
        pure_cp_block_contain_punc: Whether to count punctuation lines when calculating copy block length
        count_cp_block_update: Whether to include line updates in copied blocks

    Returns:
        List of potential copy mappings
    """
    mappings = []
    checked_dict = {}

    for added_line in added_lines:
        if added_lines[added_line][0] == "":
            continue

        candidates = {}
        for src_line in src_lines:
            if src_lines[src_line][0] == "" or (src_line, added_line) in checked_dict:
                continue

            checked_dict[(src_line, added_line)] = True
            cur_src_line_no = src_line
            cur_added_line_no = added_line
            indent_diff = added_lines[added_line][1][0] - src_lines[src_line][1][0]
            src_mode = "k"
            block_length = 0
            pure_block_length = 0
            edit_actions = 4
            c_updates = []

            while (cur_src_line_no in src_lines and
                   cur_added_line_no in added_lines and
                   (src_lines[cur_src_line_no][0] == added_lines[cur_added_line_no][0] or
                    (src_lines[cur_src_line_no][0] != added_lines[cur_added_line_no][0] and
                     count_cp_block_update and
                     levenshtein_ratio(src_lines[cur_src_line_no][0], added_lines[cur_added_line_no][0]) >= 0.6)) and
                   ((added_lines[cur_added_line_no][0] != "" and
                     added_lines[cur_added_line_no][1][0] - src_lines[cur_src_line_no][1][0] == indent_diff) or
                    added_lines[cur_added_line_no][0] == "")):

                checked_dict[(cur_src_line_no, cur_added_line_no)] = True

                if count_cp_block_update and src_lines[cur_src_line_no][0] != added_lines[cur_added_line_no][0]:
                    edit_actions += 1
                    c_updates.append([cur_src_line_no, cur_added_line_no])

                if src_lines[cur_src_line_no][0] != "" and added_lines[cur_added_line_no][0] != "":
                    if pure_cp_block_contain_punc or not (
                            is_pure_punctuation(src_lines[cur_src_line_no][0]) and
                            is_pure_punctuation(added_lines[cur_added_line_no][0])):
                        pure_block_length += 1

                cur_src_line_no += 1
                cur_added_line_no += 1
                block_length += 1

            if (pure_block_length >= min_copy_block_length and
                    not copy_block_in_hunk(
                        {"mode": src_mode, "block_length": block_length,
                         "src_start": src_line, "added_start": added_line}, hunks) and
                    not is_pure_punctuation(
                        "".join([src_lines[line][0] for line in range(src_line, src_line + block_length)]))):

                cur_src_line_no = src_line - 1
                cur_added_line_no = added_line - 1

                while cur_src_line_no >= 1 and cur_added_line_no >= 1:
                    if (cur_src_line_no in src_lines and
                            cur_added_line_no in added_lines and
                            src_lines[cur_src_line_no][0] == "" and
                            added_lines[cur_added_line_no][0] == ""):

                        src_line = cur_src_line_no
                        added_line = cur_added_line_no
                        block_length += 1
                        cur_src_line_no -= 1
                        cur_added_line_no -= 1
                    else:
                        break

                if indent_diff != 0:
                    edit_actions += 1

                ctx_similarity = context_similarity(src_line, added_line, block_length, src_all_lines, dest_all_lines)
                rd = relative_distance(src_line, added_line, block_length, diff_scripts)
                weight = edit_actions / block_length + (1 - ctx_similarity) / 10 + rd / 100

                for s in candidates:
                    if candidates[s]['block_length'] == block_length:
                        if candidates[s]['weight'] > weight:
                            del candidates[s]
                            candidate = {
                                "mode": src_mode,
                                "block_length": block_length,
                                "src_start": src_line,
                                "added_start": added_line,
                                "context_similarity": ctx_similarity,
                                "weight": weight,
                                "updates": c_updates,
                                "indent_diff": indent_diff,
                                "edit_actions": edit_actions,
                                "relative_distance": rd
                            }
                            candidates[src_line] = candidate
                            break
                        else:
                            break
                else:
                    candidate = {
                        "mode": src_mode,
                        "block_length": block_length,
                        "src_start": src_line,
                        "added_start": added_line,
                        "context_similarity": ctx_similarity,
                        "weight": weight,
                        "updates": c_updates,
                        "indent_diff": indent_diff,
                        "edit_actions": edit_actions,
                        "relative_distance": rd
                    }
                    candidates[src_line] = candidate

        for s in candidates:
            mappings.append(candidates[s])

    return mappings


def context_similarity(
        src_start: int,
        dest_start: int,
        block: int,
        src_lines: list[str],
        dest_lines: list[str]
) -> float:
    """
    Calculate similarity between contexts of source and destination blocks.

    Args:
        src_start: Source block start line
        dest_start: Destination block start line
        block: Block length
        src_lines: All source lines
        dest_lines: All destination lines

    Returns:
        Context similarity score
    """
    src_context = construct_context(src_start, block, src_lines)
    dest_context = construct_context(dest_start, block, dest_lines)
    return levenshtein_ratio(src_context, dest_context)


def construct_context(start: int, block_length: int, lines: list[str]) -> str:
    """
    Construct context string for a given block.

    Args:
        start: Block start line
        block_length: Block length
        lines: All lines to extract context from

    Returns:
        Constructed context string
    """
    context = ""
    i, j = 1, 1
    start_ptr = start - 2

    while i < 5 and start_ptr >= 0:
        if lines[start_ptr].strip() == "":
            start_ptr -= 1
            continue
        else:
            context = lines[start_ptr].strip() + " " + context
            start_ptr -= 1
            i += 1

    start_ptr = start + block_length - 1
    while j < 5 and start_ptr < len(lines):
        if lines[start_ptr].strip() == "":
            start_ptr += 1
            continue
        else:
            context = context + " " + lines[start_ptr].strip()
            start_ptr += 1
            j += 1

    return context


def judge_overlap_type(
        assigned_start: int,
        assigned_block_length: int,
        overlapped_start: int,
        overlapped_block_length: int
) -> str | None:
    """
    Determine the type of overlap between two blocks.

    Args:
        assigned_start: Start of first block
        assigned_block_length: Length of first block
        overlapped_start: Start of second block
        overlapped_block_length: Length of second block

    equal: e, cover: c, inner: i, up: u, down: d

    Returns:
        Overlap type code or None if no overlap
    """
    if assigned_start == overlapped_start and assigned_block_length == overlapped_block_length:
        return "e"
    elif (assigned_start >= overlapped_start and
          (assigned_start + assigned_block_length) <= (overlapped_start + overlapped_block_length)):
        return "c"
    elif (assigned_start <= overlapped_start and
          (assigned_start + assigned_block_length) >= (overlapped_start + overlapped_block_length)):
        return "i"
    elif overlapped_start <= assigned_start <= overlapped_start + overlapped_block_length - 1:
        return "u"
    elif assigned_start <= overlapped_start <= assigned_start + assigned_block_length - 1:
        return "d"
    else:
        return None


def km_compute(
        mappings: list[dict],
        src_all_lines: list[str],
        dest_all_lines: list[str],
        min_move_block_length: int = 2,
        min_copy_block_length: int = 2,
        pure_mv_block_contain_punc: bool = True,
        pure_cp_block_contain_punc: bool = True
) -> tuple[list[dict], list[dict]]:
    """
    Compute optimal block mappings using Kuhn-Munkres algorithm.

    Args:
        mappings: List of candidate mappings
        src_all_lines: All source lines
        dest_all_lines: All destination lines
        min_move_block_length: Minimum move block length
        min_copy_block_length: Minimum copy block length
        pure_mv_block_contain_punc: Whether to count punctuation lines when calculating move-block length
        pure_cp_block_contain_punc: Whether to count punctuation lines when calculating copy-block length

    Returns:
        Tuple of (optimal_mappings, remaining_mappings)
    """
    mappings = [x for i, x in enumerate(mappings) if x not in mappings[:i]]
    grouped_mappings_src = []
    grouped_mappings_added = []
    mappings.sort(key=lambda x: x["src_start"])
    km_start = 0
    km_end = 0

    for index, mapping in enumerate(mappings):
        # state: a: assigned, d: deleted, None: waiting for assigned, s: sliced
        mapping['state'] = None
        found_src_mapping = False

        for group_src in grouped_mappings_src:
            for mapping_src in group_src:
                if (not ((mapping['src_start'] + mapping['block_length'] - 1) < mapping_src['src_start'] or
                         mapping['src_start'] > (mapping_src['src_start'] + mapping_src['block_length'] - 1)) and
                        mapping['mode'] != 'k' and mapping_src['mode'] != 'k'):
                    mapping['km_start'] = mapping_src['km_start']
                    group_src.append(mapping)
                    found_src_mapping = True
                    break

            if found_src_mapping:
                break

        if not found_src_mapping:
            mapping['km_start'] = km_start
            grouped_mappings_src.append([mapping])
            km_start += 1

    mappings.sort(key=lambda x: x["added_start"])
    for index, mapping in enumerate(mappings):
        found_added_mapping = False

        for group_added in grouped_mappings_added:
            for mapping_added in group_added:
                if not ((mapping['added_start'] + mapping['block_length'] - 1) < mapping_added['added_start'] or
                        mapping['added_start'] > (mapping_added['added_start'] + mapping_added['block_length'] - 1)):
                    mapping['km_end'] = mapping_added['km_end']
                    group_added.append(mapping)
                    found_added_mapping = True
                    break

            if found_added_mapping:
                break

        if not found_added_mapping:
            mapping['km_end'] = km_end
            km_end += 1
            grouped_mappings_added.append([mapping])

    cost_matrix = np.full((km_start, km_end), 1000.0)
    for mapping in mappings:
        x = mapping['km_start']
        y = mapping['km_end']
        if cost_matrix[x][y] != 1000:
            if mapping['weight'] < cost_matrix[x][y]:
                cost_matrix[x][y] = mapping['weight']
        else:
            cost_matrix[x][y] = mapping['weight']

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    assignments = list(zip(row_ind, col_ind))
    km_matches = []
    remain_mappings = []

    for assignment in assignments:
        present_assignment = {}
        max_weight = len(src_all_lines) * 2

        for mapping1 in mappings:
            if (not mapping1['state'] and
                    mapping1['km_start'] == assignment[0] and
                    mapping1['km_end'] == assignment[1] and
                    mapping1['weight'] < max_weight):
                present_assignment = mapping1
                max_weight = mapping1['weight']

        if present_assignment:
            present_assignment['state'] = 'a'
            km_matches.append(present_assignment)
        else:
            continue

        for mapping2 in mappings:
            if (mapping2['state'] or
                    (mapping2['km_start'] == assignment[0] and
                     mapping2['km_end'] == assignment[1] and
                     mapping2['mode'] != 'u')):
                continue

            elif mapping2['km_start'] == assignment[0]:
                overlap_type = judge_overlap_type(
                    present_assignment['src_start'],
                    present_assignment['block_length'],
                    mapping2['src_start'],
                    mapping2['block_length']
                )

                if overlap_type == 'e' or overlap_type == 'i':
                    mapping2['state'] = 'd'
                    continue
                elif overlap_type is None:
                    mapping2['state'] = 's'
                    remain_mappings.append(mapping2)
                elif overlap_type == 'c':
                    cannot_be_sliced = True
                    up_offset = present_assignment['src_start'] - mapping2['src_start']
                    pure_up_offset = pure_block_len(
                        up_offset, mapping2['src_start'], src_all_lines,
                        mapping2['added_start'], dest_all_lines,
                        pure_mv_block_contain_punc, pure_cp_block_contain_punc, mapping2['mode']
                    )

                    edit_actions = 1 if mapping2['mode'] == 'u' else 2 if mapping2['mode'] == 'r' else 4
                    if (mapping2['indent_diff'] != 0 and mapping2['mode'] == 'k') or (
                            mapping2['indent_diff'] != 0 and mapping2['mode'] == 'r' and
                            mapping2['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in mapping2['updates']:
                        if ud[0] in range(mapping2['src_start'], present_assignment['src_start']):
                            updates.append(ud)
                            edit_actions += 1

                    if (mapping2['mode'] == 'r' and pure_up_offset >= min_move_block_length) or (
                            mapping2['mode'] == 'k' and pure_up_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            mapping2['src_start'], mapping2['added_start'], up_offset,
                            src_all_lines, dest_all_lines
                        )

                        mapping2['state'] = 's'
                        cannot_be_sliced = False
                        new_mapping = {
                            'mode': mapping2['mode'],
                            'block_length': up_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / up_offset + (1 - ctx_similarity) / 10 +
                            mapping2['relative_distance'] / 100,
                            'src_start': mapping2['src_start'],
                            'added_start': mapping2['added_start'],
                            'km_start': mapping2['km_start'],
                            'km_end': mapping2['km_end'],
                            'indent_diff': mapping2['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            'relative_distance': mapping2['relative_distance'],
                            'state': None
                        }

                        if mapping2['mode'] == 'r':
                            new_mapping['move_type'] = mapping2['move_type']

                        remain_mappings.append(new_mapping)

                    down_offset = (mapping2['src_start'] + mapping2['block_length'] -
                                   (present_assignment['src_start'] + present_assignment['block_length']))

                    pure_down_offset = pure_block_len(
                        down_offset,
                        present_assignment['src_start'] + present_assignment['block_length'],
                        src_all_lines,
                        mapping2['added_start'] + (present_assignment['src_start'] +
                                                   present_assignment['block_length'] - mapping2['src_start']),
                        dest_all_lines,
                        pure_mv_block_contain_punc,
                        pure_cp_block_contain_punc,
                        mapping2['mode']
                    )

                    edit_actions = 1 if mapping2['mode'] == 'u' else 2 if mapping2['mode'] == 'r' else 4
                    if (mapping2['indent_diff'] != 0 and mapping2['mode'] == 'k') or (
                            mapping2['indent_diff'] != 0 and mapping2['mode'] == 'r' and
                            mapping2['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in mapping2['updates']:
                        if ud[0] in range(present_assignment['src_start'] + present_assignment['block_length'],
                                          present_assignment['src_start'] + present_assignment[
                                              'block_length'] + down_offset):
                            updates.append(ud)
                            edit_actions += 1

                    if (mapping2['mode'] == 'r' and pure_down_offset >= min_move_block_length) or (
                            mapping2['mode'] == 'k' and pure_down_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            present_assignment['src_start'] + present_assignment['block_length'],
                            mapping2['added_start'] + present_assignment['src_start'] +
                            present_assignment['block_length'] - mapping2['src_start'],
                            down_offset,
                            src_all_lines, dest_all_lines
                        )

                        mapping2['state'] = 's'
                        cannot_be_sliced = False
                        new_mapping = {
                            'mode': mapping2['mode'],
                            'block_length': down_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / down_offset + (1 - ctx_similarity) / 10 +
                            mapping2['relative_distance'] / 100,
                            'src_start': present_assignment['src_start'] + present_assignment['block_length'],
                            'added_start': mapping2['added_start'] + (present_assignment['src_start'] +
                                                                      present_assignment['block_length'] - mapping2[
                                                                          'src_start']),
                            'km_start': mapping2['km_start'],
                            'km_end': mapping2['km_end'],
                            'indent_diff': mapping2['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": mapping2['relative_distance'],
                            'state': None
                        }

                        if mapping2['mode'] == 'r':
                            new_mapping['move_type'] = mapping2['move_type']

                        remain_mappings.append(new_mapping)

                    if cannot_be_sliced:
                        mapping2['state'] = 's'
                elif overlap_type == 'u':
                    up_offset = present_assignment['src_start'] - mapping2['src_start']
                    pure_up_offset = pure_block_len(
                        up_offset, mapping2['src_start'], src_all_lines,
                        mapping2['added_start'], dest_all_lines,
                        pure_mv_block_contain_punc, pure_cp_block_contain_punc, mapping2['mode']
                    )

                    edit_actions = 1 if mapping2['mode'] == 'u' else 2 if mapping2['mode'] == 'r' else 4
                    if (mapping2['indent_diff'] != 0 and mapping2['mode'] == 'k') or (
                            mapping2['indent_diff'] != 0 and mapping2['mode'] == 'r' and
                            mapping2['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in mapping2['updates']:
                        if ud[0] in range(mapping2['src_start'], present_assignment['src_start']):
                            updates.append(ud)
                            edit_actions += 1

                    ctx_similarity = context_similarity(
                        mapping2['src_start'], mapping2['added_start'], up_offset,
                        src_all_lines, dest_all_lines
                    )

                    mapping2['state'] = 's'
                    if (mapping2['mode'] == 'r' and pure_up_offset >= min_move_block_length) or (
                            mapping2['mode'] == 'k' and pure_up_offset >= min_copy_block_length):

                        new_mapping = {
                            'mode': mapping2['mode'],
                            'block_length': up_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / up_offset + (1 - ctx_similarity) / 10 +
                            mapping2['relative_distance'] / 100,
                            'src_start': mapping2['src_start'],
                            'added_start': mapping2['added_start'],
                            'km_start': mapping2['km_start'],
                            'km_end': mapping2['km_end'],
                            'indent_diff': mapping2['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": mapping2['relative_distance'],
                            'state': None
                        }

                        if mapping2['mode'] == 'r':
                            new_mapping['move_type'] = mapping2['move_type']

                        remain_mappings.append(new_mapping)
                    else:
                        mapping2['state'] = 's'
                elif overlap_type == 'd':
                    down_offset = (mapping2['src_start'] + mapping2['block_length'] -
                                   (present_assignment['src_start'] + present_assignment['block_length']))

                    pure_down_offset = pure_block_len(
                        down_offset,
                        present_assignment['src_start'] + present_assignment['block_length'],
                        src_all_lines,
                        mapping2['added_start'] + (present_assignment['src_start'] +
                                                   present_assignment['block_length'] - mapping2['src_start']),
                        dest_all_lines,
                        pure_mv_block_contain_punc,
                        pure_cp_block_contain_punc,
                        mapping2['mode']
                    )

                    edit_actions = 1 if mapping2['mode'] == 'u' else 2 if mapping2['mode'] == 'r' else 4
                    if (mapping2['indent_diff'] != 0 and mapping2['mode'] == 'k') or (
                            mapping2['indent_diff'] != 0 and mapping2['mode'] == 'r' and
                            mapping2['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in mapping2['updates']:
                        if ud[0] in range(present_assignment['src_start'] + present_assignment['block_length'],
                                          present_assignment['src_start'] + present_assignment[
                                              'block_length'] + down_offset):
                            updates.append(ud)
                            edit_actions += 1

                    if (mapping2['mode'] == 'r' and pure_down_offset >= min_move_block_length) or (
                            mapping2['mode'] == 'k' and pure_down_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            present_assignment['src_start'] + present_assignment['block_length'],
                            mapping2['added_start'] + present_assignment['src_start'] +
                            present_assignment['block_length'] - mapping2['src_start'],
                            down_offset,
                            src_all_lines, dest_all_lines
                        )

                        mapping2['state'] = 's'
                        new_mapping = {
                            'mode': mapping2['mode'],
                            'block_length': down_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / down_offset + (1 - ctx_similarity) / 10 +
                            mapping2['relative_distance'] / 100,
                            'src_start': present_assignment['src_start'] + present_assignment['block_length'],
                            'added_start': mapping2['added_start'] + (present_assignment['src_start'] +
                                                                      present_assignment['block_length'] - mapping2[
                                                                          'src_start']),
                            'km_start': mapping2['km_start'],
                            'km_end': mapping2['km_end'],
                            'indent_diff': mapping2['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": mapping2['relative_distance'],
                            'state': None
                        }

                        if mapping2['mode'] == 'r':
                            new_mapping['move_type'] = mapping2['move_type']

                        remain_mappings.append(new_mapping)
                    else:
                        mapping2['state'] = 's'

    for assignment2 in assignments:
        for mapping2 in mappings:
            if (not mapping2['state'] and
                    mapping2['km_end'] == assignment2[1] and
                    ((mapping2['mode'] == 'k' and mapping2['block_length'] >= min_copy_block_length) or
                     mapping2['mode'] == 'u' or mapping2['mode'] == 'r')):

                if mapping2 not in remain_mappings:
                    remain_mappings.append(mapping2)

    final_remain_mappings = []
    for remain_mapping in remain_mappings:
        for km_match in km_matches:
            if (remain_mapping['state'] != 'd' and
                    remain_mapping['km_end'] == km_match['km_end'] and
                    (remain_mapping['km_start'] != km_match['km_start'] or
                     (km_match['mode'] == 'u' and remain_mapping['mode'] == 'u'))):

                end_overlap_type = judge_overlap_type(
                    km_match['added_start'], km_match['block_length'],
                    remain_mapping['added_start'], remain_mapping['block_length']
                )

                if end_overlap_type == 'e' or end_overlap_type == 'i':
                    continue
                elif end_overlap_type is None:
                    final_remain_mappings.append(remain_mapping)
                elif end_overlap_type == 'c':
                    up_offset = km_match['added_start'] - remain_mapping['added_start']
                    pure_up_offset = pure_block_len(
                        up_offset, remain_mapping['src_start'], src_all_lines,
                        remain_mapping['added_start'], dest_all_lines,
                        pure_mv_block_contain_punc, pure_cp_block_contain_punc,
                        remain_mapping['mode']
                    )

                    edit_actions = 1 if remain_mapping['mode'] == 'u' else 2 if remain_mapping['mode'] == 'r' else 3
                    if (remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'k') or (
                            remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'r' and
                            remain_mapping['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in remain_mapping['updates']:
                        if ud[1] in range(remain_mapping['added_start'], km_match['added_start']):
                            updates.append(ud)
                            edit_actions += 1

                    if (remain_mapping['mode'] == 'r' and pure_up_offset >= min_move_block_length) or (
                            remain_mapping['mode'] == 'k' and pure_up_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            remain_mapping['src_start'], remain_mapping['added_start'],
                            up_offset, src_all_lines, dest_all_lines
                        )

                        new_mapping = {
                            'mode': remain_mapping['mode'],
                            'block_length': up_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / up_offset + (1 - ctx_similarity) / 10 +
                            remain_mapping['relative_distance'] / 100,
                            'src_start': remain_mapping['src_start'],
                            'added_start': remain_mapping['added_start'],
                            'km_start': remain_mapping['km_start'],
                            'km_end': remain_mapping['km_end'],
                            'indent_diff': remain_mapping['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            'relative_distance': remain_mapping['relative_distance'],
                            'state': None
                        }

                        if remain_mapping['mode'] == 'r':
                            new_mapping['move_type'] = remain_mapping['move_type']

                        final_remain_mappings.append(new_mapping)

                    down_offset = (remain_mapping['added_start'] + remain_mapping['block_length'] -
                                   (km_match['added_start'] + km_match['block_length']))

                    pure_down_offset = pure_block_len(
                        down_offset,
                        remain_mapping['src_start'] + km_match['added_start'] + km_match['block_length'] -
                        remain_mapping['added_start'],
                        src_all_lines,
                        km_match['added_start'] + km_match['block_length'],
                        dest_all_lines,
                        pure_mv_block_contain_punc,
                        pure_cp_block_contain_punc,
                        remain_mapping['mode']
                    )

                    edit_actions = 1 if remain_mapping['mode'] == 'u' else 2 if remain_mapping['mode'] == 'r' else 3
                    if (remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'k') or (
                            remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'r' and
                            remain_mapping['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in remain_mapping['updates']:
                        if ud[1] in range(km_match['added_start'] + km_match['block_length'],
                                          km_match['added_start'] + km_match['block_length'] + down_offset):
                            updates.append(ud)
                            edit_actions += 1

                    if (remain_mapping['mode'] == 'r' and pure_down_offset >= min_move_block_length) or (
                            remain_mapping['mode'] == 'k' and pure_down_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            remain_mapping['src_start'] + km_match['added_start'] + km_match['block_length'] -
                            remain_mapping['added_start'],
                            km_match['added_start'] + km_match['block_length'],
                            down_offset,
                            src_all_lines,
                            dest_all_lines
                        )

                        new_mapping = {
                            'mode': remain_mapping['mode'],
                            'block_length': down_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / down_offset + (1 - ctx_similarity) / 10 +
                            remain_mapping['relative_distance'] / 100,
                            'src_start': remain_mapping['src_start'] + km_match['added_start'] +
                            km_match['block_length'] - remain_mapping['added_start'],
                            'added_start': km_match['added_start'] + km_match['block_length'],
                            'km_start': remain_mapping['km_start'],
                            'km_end': remain_mapping['km_end'],
                            'indent_diff': remain_mapping['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": remain_mapping['relative_distance'],
                            'state': None
                        }

                        if remain_mapping['mode'] == 'r':
                            new_mapping['move_type'] = remain_mapping['move_type']

                        final_remain_mappings.append(new_mapping)
                elif end_overlap_type == 'u':
                    up_offset = km_match['added_start'] - remain_mapping['added_start']
                    pure_up_offset = pure_block_len(
                        up_offset, remain_mapping['src_start'], src_all_lines,
                        remain_mapping['added_start'], dest_all_lines,
                        pure_mv_block_contain_punc, pure_cp_block_contain_punc,
                        remain_mapping['mode']
                    )

                    edit_actions = 1 if remain_mapping['mode'] == 'u' else 2 if remain_mapping['mode'] == 'r' else 3
                    if (remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'k') or (
                            remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'r' and
                            remain_mapping['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in remain_mapping['updates']:
                        if ud[1] in range(remain_mapping['added_start'], km_match['added_start']):
                            updates.append(ud)
                            edit_actions += 1

                    if (remain_mapping['mode'] == 'r' and pure_up_offset >= min_move_block_length) or (
                            remain_mapping['mode'] == 'k' and pure_up_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            remain_mapping['src_start'], remain_mapping['added_start'],
                            up_offset, src_all_lines, dest_all_lines
                        )

                        new_mapping = {
                            'mode': remain_mapping['mode'],
                            'block_length': up_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / up_offset + (1 - ctx_similarity) / 10 +
                            remain_mapping['relative_distance'] / 100,
                            'src_start': remain_mapping['src_start'],
                            'added_start': remain_mapping['added_start'],
                            'km_start': remain_mapping['km_start'],
                            'km_end': remain_mapping['km_end'],
                            'indent_diff': remain_mapping['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": remain_mapping['relative_distance'],
                            'state': None
                        }

                        if remain_mapping['mode'] == 'r':
                            new_mapping['move_type'] = remain_mapping['move_type']

                        final_remain_mappings.append(new_mapping)
                elif end_overlap_type == 'd':
                    down_offset = (remain_mapping['added_start'] + remain_mapping['block_length'] -
                                   (km_match['added_start'] + km_match['block_length']))

                    pure_down_offset = pure_block_len(
                        down_offset,
                        remain_mapping['src_start'] + (km_match['added_start'] + km_match['block_length'] -
                                                       remain_mapping['added_start']),
                        src_all_lines,
                        km_match['added_start'] + km_match['block_length'],
                        dest_all_lines,
                        pure_mv_block_contain_punc,
                        pure_cp_block_contain_punc,
                        remain_mapping['mode']
                    )

                    edit_actions = 1 if remain_mapping['mode'] == 'u' else 2 if remain_mapping['mode'] == 'r' else 3
                    if (remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'k') or (
                            remain_mapping['indent_diff'] != 0 and remain_mapping['mode'] == 'r' and
                            remain_mapping['move_type'] != 'h'):
                        edit_actions += 1

                    updates = []
                    for ud in remain_mapping['updates']:
                        if ud[1] in range(km_match['added_start'] + km_match['block_length'],
                                          km_match['added_start'] + km_match['block_length'] + down_offset):
                            updates.append(ud)
                            edit_actions += 1

                    if (remain_mapping['mode'] == 'r' and pure_down_offset >= min_move_block_length) or (
                            remain_mapping['mode'] == 'k' and pure_down_offset >= min_copy_block_length):

                        ctx_similarity = context_similarity(
                            remain_mapping['src_start'] + km_match['added_start'] + km_match['block_length'] -
                            remain_mapping['added_start'],
                            km_match['added_start'] + km_match['block_length'],
                            down_offset,
                            src_all_lines,
                            dest_all_lines
                        )

                        new_mapping = {
                            'mode': remain_mapping['mode'],
                            'block_length': down_offset,
                            'context_similarity': ctx_similarity,
                            'weight': edit_actions / down_offset + (1 - ctx_similarity) / 10 +
                            remain_mapping['relative_distance'] / 100,
                            'src_start': remain_mapping['src_start'] + (km_match['added_start'] +
                                                                        km_match['block_length'] - remain_mapping[
                                                                            'added_start']),
                            'added_start': km_match['added_start'] + km_match['block_length'],
                            'km_start': remain_mapping['km_start'],
                            'km_end': remain_mapping['km_end'],
                            'indent_diff': remain_mapping['indent_diff'],
                            'edit_actions': edit_actions,
                            'updates': updates,
                            "relative_distance": remain_mapping['relative_distance'],
                            'state': None
                        }

                        if remain_mapping['mode'] == 'r':
                            new_mapping['move_type'] = remain_mapping['move_type']

                        final_remain_mappings.append(new_mapping)

    return km_matches, final_remain_mappings


def generate_edit_action(mode: str, *args) -> str:
    """
    Generate human-readable edit action description.

    Args:
        mode: Type of edit action
        *args: Arguments specific to the action type

    Returns:
        String description of the edit action
    """
    if mode == 'move':
        if args[3] < 0:
            move_direction = f" with moving left {abs(args[3])} whitespaces."
        elif args[3] == 0:
            move_direction = ""
        else:
            move_direction = f" with moving right {args[3]} whitespaces."

        if args[0] == 1:
            return f"Move 1 line from line {args[1]} to line {args[2]}{move_direction}"
        else:
            return f"Move a {args[0]}-line block from line {args[1]} to line {args[2]}{move_direction}"

    elif mode == 'copy':
        if args[3] < 0:
            move_direction = f" with moving left {abs(args[3])} whitespaces."
        elif args[3] == 0:
            move_direction = ""
        else:
            move_direction = f" with moving right {args[3]} whitespaces."

        return f"Copy a {args[0]}-line block from line {args[1]} to line {args[2]}{move_direction}"

    elif mode == 'm_update':
        return f"Update line {args[0]} to line {args[1]}"

    elif mode == 'c_update':
        return f"Update line {args[0]} to line {args[1]}"

    elif mode == 'update':
        if args[2] < 0:
            move_direction = f" with moving left {abs(args[2])} whitespaces."
        elif args[2] == 0:
            move_direction = ""
        else:
            move_direction = f" with moving right {args[2]} whitespaces."

        return f"Update line {args[0]} to line {args[1]}{move_direction}"

    elif mode == 'insert':
        return f"Insert line {args[0]}"

    elif mode == 'delete':
        return f"Delete line {args[0]}"

    elif mode == "split":
        return f"Split line {args[0]} to lines {args[1][0]}-{args[1][-1]}"

    elif mode == "merge":
        return f"Merge lines {args[0][0]}-{args[0][-1]} to line {args[1]}"


def generate_edit_scripts_from_match(
    km_matches: List[Dict],
    diff_scripts: List[str],
    src_lines: OrderedDict,
    added_lines: OrderedDict,
    splits_merges: List[List[List[int]]],
    hunks: List[List[List[int]]],
    src_len: int,
    dest_len: int
) -> List[Dict]:
    """
    Generate structured edit scripts from the results computed from the Kuhn-Munkres process.


    Args:
        km_matches: List of dictionaries containing Kuhn-Munkres algorithm matches with keys like
                    'mode' ('k' for copy, 'r' for move, 'u' for update), 'block_length', 'src_start',
                    'added_start', 'indent_diff', and 'updates'
        diff_scripts: List of raw diff operation strings (e.g., 'k123' for keep, 'r456' for remove, 'i789' for insert)
        src_lines: OrderedDict mapping source line numbers to tuples containing line content and metadata
        added_lines: OrderedDict mapping destination line numbers to tuples containing added line content and metadata
        splits_merges: List of line split/merge mappings
        hunks: List of diff hunks, each containing lists of source lines and destination lines involved in the hunk
        src_len: Total number of lines in the source file
        dest_len: Total number of lines in the destination file

    Returns:
        List of dictionaries representing structured edit operations, each containing:
        - 'mode': Type of edit (e.g., 'copy', 'move', 'update', 'split', 'merge', 'insert', 'delete')
        - 'src_line': Starting line number in the source file
        - 'dest_line': Starting line number in the destination file
        - 'block_length': Number of lines involved in block operations
        - 'edit_action': Formatted action string describing the edit
        - Additional mode-specific fields (e.g., 'indent_offset' for copy/move, 'str_diff' for updates)
    """
    diff_scripts_dict = {}
    k_pairs = {}
    src_line_no, dest_line_no = 1, 1
    for ds in diff_scripts:
        diff_scripts_dict[ds] = None
        if ds[0] == 'k':
            k_pairs[int(ds[1:])] = dest_line_no
            src_line_no += 1
            dest_line_no += 1
        elif ds[0] == 'r':
            src_line_no += 1
        else:
            dest_line_no += 1
    edit_scripts = []
    for split_merge in splits_merges:
        if len(split_merge[0]) == 1:
            edit_action = generate_edit_action("split", split_merge[0][0], split_merge[1])
            edit_scripts.append({"src_line": split_merge[0][0], "block_length": len(split_merge[1]),
                                 "dest_line": split_merge[1][0], "mode": "split",
                                 "edit_action": edit_action})
            diff_scripts_dict['r' + str(split_merge[0][0])] = "split-" + str(split_merge[1][0])
            for d_no in range(split_merge[1][0], split_merge[1][0] + len(split_merge[1])):
                diff_scripts_dict['i' + str(d_no)] = "split-" + str(split_merge[0][0])
        else:
            edit_action = generate_edit_action("merge", split_merge[0], split_merge[1][0])
            edit_scripts.append({"src_line": split_merge[0][0], "block_length": len(split_merge[0]),
                                 "dest_line": split_merge[1][0], "mode": "merge",
                                 "edit_action": edit_action})
            diff_scripts_dict['i' + str(split_merge[1][0])] = "merge-" + str(split_merge[0][0])
            for s_no in range(split_merge[0][0], split_merge[0][0] + len(split_merge[0])):
                diff_scripts_dict['r' + str(s_no)] = "merge-" + str(split_merge[1][0])
    for km_match in km_matches:
        if km_match['mode'] == 'k':
            edit_action = generate_edit_action("copy", km_match['block_length'], km_match['src_start'],
                                               km_match['added_start'], added_lines[km_match['added_start']][1][0] -
                                               src_lines[km_match['src_start']][1][0])
            edit_scripts.append({"src_line": km_match['src_start'], "block_length": km_match['block_length'],
                                 "dest_line": km_match['added_start'], "mode": "copy",
                                 "indent_offset": km_match['indent_diff'],
                                 "edit_action": edit_action,
                                 "updates": km_match['updates']})
            for d_no in range(km_match['added_start'], km_match['added_start'] + km_match['block_length']):
                diff_scripts_dict['i' + str(d_no)] = "copy-" + str(km_match['src_start'])
            for update in km_match['updates']:
                copy_update = {}
                edit_action = generate_edit_action("c_update", update[0], update[1])
                copy_update["src_line"] = update[0]
                copy_update["dest_line"] = update[1]
                copy_update["mode"] = "c_update"
                copy_update["edit_action"] = edit_action
                copy_update["str_diff"] = construct_str_diff_data(src_lines[update[0]], added_lines[update[1]])
                edit_scripts.append(copy_update)
        elif km_match['mode'] == 'r':
            edit_action = generate_edit_action("move", km_match['block_length'], km_match['src_start'],
                                               km_match['added_start'], added_lines[km_match['added_start']][1][0] -
                                               src_lines[km_match['src_start']][1][0])
            edit_scripts.append({"src_line": km_match['src_start'], "block_length": km_match['block_length'],
                                 "dest_line": km_match['added_start'], "mode": "move",
                                 "indent_offset": km_match['indent_diff'], "edit_action": edit_action,
                                 "move_type": km_match['move_type'],
                                 "updates": km_match['updates']})
            for bl in range(km_match['block_length']):
                r_line_no = km_match['src_start'] + bl
                i_line_no = km_match['added_start'] + bl
                diff_scripts_dict['r' + str(r_line_no)] = "move-" + str(km_match['added_start'])
                diff_scripts_dict['i' + str(i_line_no)] = "move-" + str(km_match['src_start'])
            for update in km_match['updates']:
                move_update = {}
                edit_action = generate_edit_action("m_update", update[0], update[1])
                move_update["src_line"] = update[0]
                move_update["dest_line"] = update[1]
                move_update["mode"] = "m_update"
                move_update["edit_action"] = edit_action
                move_update["str_diff"] = construct_str_diff_data(src_lines[update[0]], added_lines[update[1]])
                edit_scripts.append(move_update)
        elif km_match['mode'] == 'u':
            edit_action = generate_edit_action("update", km_match['src_start'], km_match['added_start'],
                                               added_lines[km_match['added_start']][1][0] -
                                               src_lines[km_match['src_start']][1][0])
            diff_scripts_dict['r' + str(km_match['src_start'])] = "update-" + str(km_match['added_start'])
            diff_scripts_dict['i' + str(km_match['added_start'])] = "update-" + str(km_match['src_start'])
            edit_scripts.append({"src_line": km_match['src_start'],
                                 "dest_line": km_match['added_start'], "mode": "update", "str_diff":
                                     construct_str_diff_data(src_lines[km_match['src_start']],
                                                             added_lines[km_match['added_start']]),
                                 "indent_offset": added_lines[km_match['added_start']][1][0] -
                                 src_lines[km_match['src_start']][1][0],
                                 "edit_action": edit_action})
    for hunk in hunks:
        if not hunk[0]:
            hunk_last_index = diff_scripts.index("i" + str(hunk[1][-1]))
            if hunk_last_index == len(diff_scripts) - 1:
                src_line_no = src_len + 1
            else:
                src_line_no = int(diff_scripts[hunk_last_index + 1][1:])
            for i_line_no in hunk[1]:
                if not diff_scripts_dict["i" + str(i_line_no)]:
                    diff_scripts_dict['i' + str(i_line_no)] = "insert"
                    edit_action = generate_edit_action("insert", i_line_no)
                    edit_scripts.append(
                        {"mode": "insert", "dest_line": i_line_no, "src_line": src_line_no, "edit_action": edit_action})
        elif not hunk[1]:
            hunk_last_index = diff_scripts.index("r" + str(hunk[0][-1]))
            if hunk_last_index == len(diff_scripts) - 1:
                dest_line_no = dest_len + 1
            else:
                dest_line_no = k_pairs[int(diff_scripts[hunk_last_index + 1][1:])]
            for r_line_no in hunk[0]:
                if not diff_scripts_dict['r' + str(r_line_no)]:
                    diff_scripts_dict['r' + str(r_line_no)] = "delete"
                    edit_action = generate_edit_action("delete", r_line_no)
                    edit_scripts.append(
                        {"mode": "delete", "dest_line": dest_line_no, "src_line": r_line_no,
                         "edit_action": edit_action})
        else:
            hunk_last_index = diff_scripts.index("i" + str(hunk[1][-1]))
            if hunk_last_index == len(diff_scripts) - 1:
                cur_left_line = src_len + 1
                cur_right_line = dest_len + 1
            else:
                cur_left_line = int(diff_scripts[hunk_last_index + 1][1:])
                cur_right_line = k_pairs[cur_left_line]
            for rs in hunk[1][::-1]:
                cur_i_ds = 'i' + str(rs)
                if not diff_scripts_dict[cur_i_ds]:
                    diff_scripts_dict[cur_i_ds] = "insert"
                    edit_action = generate_edit_action("insert", rs)
                    edit_scripts.append(
                        {"mode": "insert", "dest_line": rs, "src_line": cur_left_line,
                         "edit_action": edit_action})
                    cur_right_line = rs
                else:
                    s_line_no = int(diff_scripts_dict[cur_i_ds].split("-")[1])
                    if diff_scripts_dict[cur_i_ds].startswith("update") or diff_scripts_dict[cur_i_ds].startswith(
                            "split") or diff_scripts_dict[cur_i_ds].startswith("merge") or (
                            diff_scripts_dict[cur_i_ds].startswith("move") and (
                            int(diff_scripts_dict['r' + str(s_line_no)].split("-")[1]) - cur_right_line) == (
                                s_line_no - cur_left_line)):
                        cur_left_line = s_line_no
                        cur_right_line = int(diff_scripts_dict['r' + str(s_line_no)].split("-")[1])
                    else:
                        cur_right_line = rs
            if hunk_last_index == len(diff_scripts) - 1:
                cur_left_line = src_len + 1
                cur_right_line = dest_len + 1
            else:
                cur_left_line = int(diff_scripts[hunk_last_index + 1][1:])
                cur_right_line = k_pairs[cur_left_line]
            for ls in hunk[0][::-1]:
                cur_r_ds = 'r' + str(ls)
                if not diff_scripts_dict[cur_r_ds]:
                    diff_scripts_dict[cur_r_ds] = "delete"
                    edit_action = generate_edit_action("delete", ls)
                    edit_scripts.append(
                        {"mode": "delete", "dest_line": cur_right_line, "src_line": ls,
                         "edit_action": edit_action})
                    cur_left_line = ls
                else:
                    d_line_no = int(diff_scripts_dict[cur_r_ds].split("-")[1])
                    if diff_scripts_dict[cur_r_ds].startswith("update") or diff_scripts_dict[cur_r_ds].startswith(
                            "split") or diff_scripts_dict[cur_r_ds].startswith("merge") or (
                            diff_scripts_dict[cur_r_ds].startswith("move") and (
                            int(diff_scripts_dict['i' + str(d_line_no)].split("-")[1]) - cur_left_line) == (
                                d_line_no - cur_right_line)):
                        cur_right_line = d_line_no
                        cur_left_line = int(diff_scripts_dict['i' + str(d_line_no)].split("-")[1])
    edit_scripts.sort(key=lambda x: (x["src_line"], x["dest_line"]))
    for esr in edit_scripts:
        if esr['mode'] == 'delete':
            for esi in edit_scripts:
                if esi['mode'] == "insert" and esr["dest_line"] > esi['dest_line'] and esr["src_line"] < esi[
                        'src_line']:
                    esr['dest_line'] = esi['dest_line']
    return edit_scripts


def generate_edit_scripts_from_diff(diff_scripts: List[str]) -> List[Dict]:
    """
    Generate basic edit scripts directly from raw diff action strings, when no line-level or block-level mappings were found.

    Args:
        diff_scripts: List of raw diff action strings, where each string starts with:
                      - 'k': Keep (no edit, line exists in both source and destination)
                      - 'r': Remove (line exists in source but not destination)
                      - 'i': Insert (line exists in destination but not source)
                      Followed by the line number (e.g., 'r5' = remove source line 5, 'i8' = insert destination line 8)

    Returns:
        List of structured edit script dictionaries with consistent fields:
        - 'mode': Edit type ('delete' for 'r' actions, 'insert' for 'i' actions)
        - 'src_line': Source line number (relevant line for 'delete'; reference line for 'insert')
        - 'dest_line': Destination line number (reference line for 'delete'; relevant line for 'insert')
        - 'edit_action': Human-readable description of the edit (generated by generate_edit_action)
    """
    src_line_no = 1
    dest_line_no = 1
    edit_scripts = []
    for diff_script in diff_scripts:
        if diff_script[0] == 'r':
            r_line_no = int(diff_script[1:])
            edit_action = generate_edit_action("delete", r_line_no)
            edit_scripts.append(
                {"mode": "delete", "src_line": r_line_no, "dest_line": dest_line_no, "edit_action": edit_action})
            src_line_no += 1
        elif diff_script[0] == 'i':
            i_line_no = int(diff_script[1:])
            edit_action = generate_edit_action("insert", i_line_no)
            edit_scripts.append({"mode": "insert", "dest_line": int(diff_script[1:]), "src_line": src_line_no,
                                 "edit_action": edit_action})
            dest_line_no += 1
        else:
            src_line_no += 1
            dest_line_no += 1
    return edit_scripts


def exists_hunk_inter(changes: OrderedDict) -> Optional[Tuple[int, int, float]]:
    """
    Check for conflicting changes in a hunk and return the first conflicting change key.

    A "conflicting change" is defined as a change entry (in the input OrderedDict)
    whose associated value (list of conflicting other changes) is non-empty. This function
    iterates through the OrderedDict and returns the first key with a non-empty value.

    Args:
        changes: OrderedDict where:
                 - Keys: Tuples representing change identifiers, formatted as
                   (source_line_no: int, destination_line_no: int, similarity_cost: float)
                 - Values: Lists of conflicting change keys (matching the key format above);
                   an empty list means no conflicts for that change

    Returns:
        Optional[Tuple[int, int, float]]: The first conflicting change key if found;
        None if no conflicting changes exist in the input OrderedDict.
    """
    for key, value in changes.items():
        if value:
            return key
    return None


def mapping_line_update(
    src_lines_list: List[str],
    dest_lines_list: List[str],
    hunks: List[List[List[int]]],
    ctx_length: int,
    line_sim_weight: float,
    sim_threshold: float
) -> List[Dict]:
    """
    Identify single-line update mappings between source and destination diff hunks.

    Args:
        src_lines_list: Full list of lines from the source file (used for context calculation)
        dest_lines_list: Full list of lines from the destination file (used for context calculation)
        hunks: List of diff hunks, where each hunk is formatted as [[source_removed_lines], [dest_inserted_lines]]
               (lines are 1-indexed line numbers)
        ctx_length: Number of context lines (above/below the target line) to use for similarity evaluation
        line_sim_weight: Weight of line content similarity in the synthetic similarity score
                        (range [0, 1], complement is context similarity weight)
        sim_threshold: Minimum synthetic similarity score (content + context) to qualify a line pair as an update

    Returns:
        List of structured update mapping dictionaries, each containing:
        - 'src_start': 1-indexed start line number in the source file (single line for updates)
        - 'added_start': 1-indexed start line number in the destination file (single line for updates)
        - 'context_similarity': Placeholder for context similarity (set to None, calculated upstream)
        - 'mode': Operation mode ('u' for update)
        - 'block_length': Number of lines in the update block (always 1 for single-line updates)
        - 'weight': Weighted score for the update (1 + normalized similarity cost, lower = more reliable)
    """
    change_diffs = []
    for hunk in hunks:
        if hunk[0] and hunk[1]:
            changes = OrderedDict()
            for r_line_no in hunk[0]:
                for i_line_no in hunk[1]:
                    syn_sim = W_BESTI_LINE(r_line_no, i_line_no, src_lines_list, dest_lines_list, ctx_length,
                                           line_sim_weight,
                                           sim_threshold)
                    if syn_sim[0]:
                        changes[(r_line_no, i_line_no, 1 - syn_sim[1])] = []
            for change1 in changes:
                for change2 in changes:
                    if change1 == change2:
                        continue
                    if (change2[1] - change1[1]) * (change2[0] - change1[0]) < 0:
                        changes[change1].append(change2)
            changes = OrderedDict(sorted(changes.items(), key=lambda x: (len(x[1]), x[0][2])))
            while changes:
                if list(changes.items())[-1][1]:
                    last_item = changes.popitem()
                    for change in changes:
                        if last_item[0] in changes[change]:
                            changes[change].remove(last_item[0])
                if not exists_hunk_inter(changes):
                    break
                changes = OrderedDict(sorted(changes.items(), key=lambda x: (len(x[1]), x[0][2])))
            for src_line_no, dest_line_no, syn_sim in sorted(changes.keys(), key=lambda x: x[0]):
                change_diffs.append(
                    {'src_start': src_line_no, 'added_start': dest_line_no, 'context_similarity': None, 'mode': 'u',
                     'block_length': 1, 'weight': 1 + syn_sim / 10})
    return change_diffs


def identify_splits_per_hunk(
    hunk: List[List[int]],
    src_lines: OrderedDict,
    added_lines: OrderedDict,
    max_split_lines: int = 8
) -> List[List[List[int]]]:
    """
    Detect line splits within a single diff hunk.

    Args:
        hunk: A diff hunk represented as [[removed_source_lines], [added_dest_lines]],
              where each line number is 1-indexed
        src_lines: OrderedDict mapping source line numbers to (content, metadata) tuples
        added_lines: OrderedDict mapping destination line numbers to (content, metadata) tuples
        max_split_lines: Maximum number of destination lines allowed for a valid split (default: 8)

    Returns:
        List of split mappings in the format [[source_line], [dest_lines]], where:
        - source_line: Single 1-indexed line number from the source that was split
        - dest_lines: List of 1-indexed line numbers in the destination forming the split
    """
    results = []
    left_lines = hunk[0]
    right_lines = hunk[1]
    traverse_start = right_lines[0]
    for left_line_no in left_lines:
        blank_first_line = True
        left_line = src_lines[left_line_no][0].strip()
        right_line_no_start = traverse_start
        cur_right_line_no = right_line_no_start
        if cur_right_line_no not in added_lines:
            break
        cur_right_line = added_lines[cur_right_line_no][0].strip()
        lines = 1
        if not right_lines:
            break
        while cur_right_line_no <= right_lines[-1]:
            if cur_right_line == "":
                if blank_first_line:
                    right_line_no_start += 1
                cur_right_line_no += 1
                if cur_right_line_no not in right_lines or cur_right_line_no > right_lines[-1]:
                    break
                cur_right_line = added_lines[cur_right_line_no][0].strip()
                continue
            if cur_right_line == left_line and lines > 1:
                results.append([[left_line_no], list(range(right_line_no_start, cur_right_line_no + 1))])
                for split_line in range(right_line_no_start, cur_right_line_no + 1):
                    right_lines.remove(split_line)
                    del added_lines[split_line]
                del src_lines[left_line_no]
                traverse_start = cur_right_line_no + 1
                break
            elif left_line.startswith(cur_right_line) and lines <= max_split_lines:
                blank_first_line = False
                left_line = left_line[len(cur_right_line):].lstrip()
                cur_right_line_no += 1
                if cur_right_line_no > right_lines[-1]:
                    break
                if cur_right_line_no not in added_lines:
                    while cur_right_line_no not in added_lines and cur_right_line_no <= right_lines[-1]:
                        cur_right_line_no += 1
                    if cur_right_line_no == right_lines[-1]:
                        break
                    else:
                        right_line_no_start = cur_right_line_no
                        cur_right_line = added_lines[right_line_no_start][0].strip()
                        left_line = src_lines[left_line_no][0].strip()
                        lines = 1
                else:
                    cur_right_line = added_lines[cur_right_line_no][0].strip()
                    lines += 1
            else:
                if cur_right_line_no == right_lines[-1]:
                    break
                else:
                    if right_line_no_start == cur_right_line_no:
                        right_line_no_start += 1
                        if right_line_no_start not in added_lines:
                            while right_line_no_start not in added_lines and right_line_no_start <= right_lines[-1]:
                                right_line_no_start += 1
                            if right_line_no_start == right_lines[-1]:
                                break
                        cur_right_line_no = right_line_no_start
                    else:
                        right_line_no_start = cur_right_line_no
                    cur_right_line = added_lines[right_line_no_start][0].strip()
                    left_line = src_lines[left_line_no][0].strip()
                    lines = 1
    for result in results:
        left_lines.remove(result[0][0])
    return results


def identify_merges_per_hunk(
    hunk: List[List[int]],
    src_lines: OrderedDict,
    added_lines: OrderedDict,
    max_merge_lines: int = 8
) -> List[List[List[int]]]:
    """
    Identify line merges within a single diff hunk.

    Args:
        hunk: A diff hunk represented as [[removed_source_lines], [added_dest_lines]],
              where each line number is 1-indexed
        src_lines: OrderedDict mapping source line numbers to (content, metadata) tuples
        added_lines: OrderedDict mapping destination line numbers to (content, metadata) tuples
        max_merge_lines: Maximum number of source lines allowed for a valid merge (default: 8)

    Returns:
        List of merge mappings in the format [[source_lines], [dest_line]], where:
        - source_lines: List of 1-indexed line numbers from the source that were merged
        - dest_line: Single 1-indexed line number in the destination forming the merge result
    """
    results = []
    left_lines = hunk[0]
    right_lines = hunk[1]
    traverse_start = left_lines[0]
    for right_line_no in right_lines:
        right_line = added_lines[right_line_no][0].strip()
        left_line_no_start = traverse_start
        cur_left_line_no = left_line_no_start
        if cur_left_line_no not in src_lines:
            break
        cur_left_line = src_lines[cur_left_line_no][0].strip()
        lines = 1
        if not left_lines:
            break
        while cur_left_line_no <= left_lines[-1]:
            if cur_left_line == "":
                cur_left_line_no += 1
                if cur_left_line_no not in left_lines or cur_left_line_no > left_lines[-1]:
                    break
                cur_left_line = src_lines[cur_left_line_no][0].strip()
                continue
            if cur_left_line == right_line:
                if lines > 1:
                    results.append([list(range(left_line_no_start, cur_left_line_no + 1)), [right_line_no]])
                    for split_line in range(left_line_no_start, cur_left_line_no + 1):
                        left_lines.remove(split_line)
                        del src_lines[split_line]
                    del added_lines[right_line_no]
                    traverse_start = cur_left_line_no + 1
                    break
                else:
                    if left_line_no_start == cur_left_line_no:
                        left_line_no_start += 1
                        cur_left_line_no = left_line_no_start
                    else:
                        left_line_no_start = cur_left_line_no
                    if cur_left_line_no not in src_lines:
                        break
                    cur_left_line = src_lines[cur_left_line_no][0].strip()
                    right_line = added_lines[right_line_no][0].strip()
                    lines = 1
            elif right_line.startswith(cur_left_line) and lines <= max_merge_lines:
                right_line = right_line[len(cur_left_line):].lstrip()
                cur_left_line_no += 1
                if cur_left_line_no > left_lines[-1]:
                    break
                if cur_left_line_no not in src_lines:
                    while cur_left_line_no not in src_lines and cur_left_line_no <= left_lines[-1]:
                        cur_left_line_no += 1
                    if cur_left_line_no == left_lines[-1]:
                        break
                    else:
                        left_line_no_start = cur_left_line_no
                        cur_left_line = src_lines[left_line_no_start][0].strip()
                        right_line = added_lines[right_line_no][0].strip()
                        lines = 1
                else:
                    cur_left_line = src_lines[cur_left_line_no][0].strip()
                    lines += 1
            else:
                if cur_left_line_no == left_lines[-1]:
                    break
                else:
                    if left_line_no_start == cur_left_line_no:
                        left_line_no_start += 1
                        if left_line_no_start not in src_lines:
                            while left_line_no_start not in src_lines and left_line_no_start <= left_lines[-1]:
                                left_line_no_start += 1
                            if left_line_no_start == left_lines[-1]:
                                break
                        cur_left_line_no = left_line_no_start
                    else:
                        left_line_no_start = cur_left_line_no
                    cur_left_line = src_lines[cur_left_line_no][0].strip()
                    right_line = added_lines[right_line_no][0].strip()
                    lines = 1
    for result in results:
        right_lines.remove(result[1][0])
    return results


def mapping_merges(
    hunks: List[List[List[int]]],
    src_lines: OrderedDict,
    added_lines: OrderedDict,
    max_merge_lines: int
) -> List[List[List[int]]]:
    """
    Identify all line merges.

    Args:
        hunks: List of all diff hunks, where each hunk is formatted as
               [[removed_source_lines], [added_dest_lines]] (line numbers are 1-indexed)
        src_lines: OrderedDict mapping source line numbers to (content, metadata) tuples
        added_lines: OrderedDict mapping destination line numbers to (content, metadata) tuples
        max_merge_lines: Maximum number of source lines allowed for a valid merge (applied to all hunks)

    Returns:
        List of aggregated merge mappings, where each mapping follows the format
        [[source_lines], [dest_line]]:
        - source_lines: List of 1-indexed line numbers from the source that were merged
        - dest_line: Single 1-indexed line number in the destination that is the merge result
    """
    merges = []
    for hunk in hunks:
        if hunk[0] and hunk[1]:
            if len(hunk[0]) > 1:
                merges_per_hunk = identify_merges_per_hunk(hunk, src_lines, added_lines, max_merge_lines)
                merges = merges + merges_per_hunk
    return merges


def mapping_splits(
    hunks: List[List[List[int]]],
    src_lines: OrderedDict,
    added_lines: OrderedDict,
    max_split_lines: int
) -> List[List[List[int]]]:
    """
    Identify all line splits.

    Args:
        hunks: List of all diff hunks, where each hunk is structured as
               [[removed_source_lines], [added_dest_lines]] (line numbers are 1-indexed)
        src_lines: OrderedDict mapping source line numbers to tuples of (content, metadata)
        added_lines: OrderedDict mapping destination line numbers to tuples of (content, metadata)
        max_split_lines: Maximum number of destination lines allowed for a valid split (applied consistently to all hunks)

    Returns:
        List of aggregated split mappings, where each mapping follows the format
        [[source_line], [dest_lines]]:
        - source_line: Single 1-indexed line number from the source file that was split
        - dest_lines: List of 1-indexed line numbers from the destination file that form the split result
    """
    splits = []
    for hunk in hunks:
        if hunk[0] and hunk[1]:
            if len(hunk[1]) > 1:
                splits_per_hunk = identify_splits_per_hunk(hunk, src_lines, added_lines, max_split_lines)
                splits = splits + splits_per_hunk
    return splits


def copy_block_in_hunk(
    copy_block: Dict,
    hunks: List[List[List[int]]]
) -> bool:
    """
    Check if a copy block occurs within one hunk.

    Args:
        copy_block: Dictionary describing the copy block, must contain the following keys:
                    - "src_start": 1-indexed start line number of the copy block in the source file
                    - "added_start": 1-indexed start line number of the copy block in the destination file
                    - "block_length": Number of lines in the copy block
        hunks: List of all diff hunks, where each hunk is structured as
               [[removed_source_lines], [added_dest_lines]] (line numbers are 1-indexed, and each sublist
               is sorted such that the first element is the smallest line number and the last is the largest)

    Returns:
        bool: True if the copy block's entire source range and entire destination range are both contained
              within the same hunk; False otherwise (including if no matching hunk is found or ranges span multiple hunks).
    """
    for hunk in hunks:
        src = hunk[0]
        dest = hunk[1]
        if src and dest and copy_block["src_start"] >= src[0] and copy_block["src_start"] + copy_block[
            "block_length"] - 1 <= src[-1] and copy_block["added_start"] >= dest[0] and copy_block["added_start"] + \
                copy_block["block_length"] - 1 <= dest[-1]:
            return True
    return False


def relative_distance(
    src_line: int,
    dest_line: int,
    block_length: int,
    diff_scripts: List[str]
) -> float:
    """
    Calculate the relative distance between a source block and its corresponding destination block.

    Args:
        src_line: 1-indexed start line number of the source block in the source file
        dest_line: 1-indexed start line number of the destination block in the destination file
        block_length: Number of lines in the source/destination block (assumed equal for both)
        diff_scripts: List of raw diff operation strings, where each string starts with:
                      - 'k': Keep (line exists in both source and destination)
                      - 'r': Remove (line exists in source but not destination)
                      - 'i': Insert (line exists in destination but not source)
                      Followed by the line number (e.g., 'k5' = keep line 5, 'i8' = insert line 8)

    Returns:
        float: Relative distance score, calculated as (number of 'k' operations) + max(number of 'i' operations, number of 'r' operations)
               between the end of the source block and the start of the destination block.
    """
    src_index = 0
    while src_index < len(diff_scripts):
        if diff_scripts[src_index] == 'k' + str(src_line) or diff_scripts[src_index] == 'r' + str(src_line):
            break
        src_index += 1
    dest_index = diff_scripts.index('i' + str(dest_line))
    k_num, i_num, r_num = 0, 0, 0
    if src_index <= dest_index:
        for i in range(src_index + block_length, dest_index):
            if diff_scripts[i][0] == 'k':
                k_num += 1
            elif diff_scripts[i][0] == 'i':
                i_num += 1
            elif diff_scripts[i][0] == 'r':
                r_num += 1
    else:
        for i in range(dest_index + block_length, src_index):
            if diff_scripts[i][0] == 'k':
                k_num += 1
            elif diff_scripts[i][0] == 'i':
                i_num += 1
            elif diff_scripts[i][0] == 'r':
                r_num += 1
    return k_num + max(r_num, i_num)


def BDiff(
    src: str,
    dest: str,
    src_lines_list: List[str],
    dest_lines_list: List[str],
    diff_algorithm: str = "Histogram",
    indent_tabs_size: int = 4,
    min_move_block_length: int = 2,
    min_copy_block_length: int = 2,
    ctx_length: int = 4,
    line_sim_weight: float = 0.6,
    sim_threshold: float = 0.5,
    max_merge_lines: int = 8,
    max_split_lines: int = 8,
    pure_mv_block_contain_punc: bool = False,
    pure_cp_block_contain_punc: bool = False,
    count_mv_block_update: bool = True,
    count_cp_block_update: bool = True,
    identify_move: bool = True,
    identify_copy: bool = True,
    identify_update: bool = True,
    identify_split: bool = True,
    identify_merge: bool = True
) -> List[Dict]:
    """
    Main function to generate edit scripts between two files.

    Args:
        src: File path to the source file (original file for comparison)
        dest: File path to the destination file (modified file for comparison)
        src_lines_list: Pre-read list of all lines from the source file (1-indexed content)
        dest_lines_list: Pre-read list of all lines from the destination file (1-indexed content)
        diff_algorithm: Git diff algorithm to use for raw change detection ("Histogram" or "Myers", default: "Histogram")
        indent_tabs_size: Number of spaces a tab character represents (for indentation calculation, default: 4)
        min_move_block_length: Minimum number of lines required for a valid move block (default: 2)
        min_copy_block_length: Minimum number of lines required for a valid copy block (default: 2)
        ctx_length: Number of context lines (above/below target line) to use for similarity evaluation (default: 4)
        line_sim_weight: Weight of line content similarity in synthetic similarity score (0-1, default: 0.6; complement is context weight)
        sim_threshold: Minimum synthetic similarity score to qualify lines as "related" (0-1, default: 0.5)
        max_merge_lines: Maximum number of source lines allowed for a valid merge operation (default: 8)
        max_split_lines: Maximum number of destination lines allowed for a valid split operation (default: 8)
        pure_mv_block_contain_punc: Whether move blocks can consist solely of punctuation lines (default: False)
        pure_cp_block_contain_punc: Whether copy blocks can consist solely of punctuation lines (default: False)
        count_mv_block_update: Whether to count line-level updates within move blocks (default: True)
        count_cp_block_update: Whether to count line-level updates within copy blocks (default: True)
        identify_move: Whether to enable detection of move operations (default: True)
        identify_copy: Whether to enable detection of copy operations (default: True)
        identify_update: Whether to enable detection of single-line update operations (default: True)
        identify_split: Whether to enable detection of line split operations (default: True)
        identify_merge: Whether to enable detection of line merge operations (default: True)

    Returns:
        List[Dict]: Structured list of edit scripts. Each script dict contains:
                    - "mode": Operation type (e.g., "move", "copy", "update", "split", "merge", "insert", "delete")
                    - "src_line": 1-indexed start line in the source file (relevant for source-dependent ops like move/copy)
                    - "dest_line": 1-indexed start line in the destination file (relevant for dest-dependent ops like insert/update)
                    - "block_length": Number of lines in the operation (for block ops like move/copy/split/merge)
                    - "edit_action": Human-readable description of the operation (e.g., "Move 3-line block from line 5 to line 12")
                    - Additional mode-specific fields (e.g., "indent_offset" for indent changes, "updates" for line edits in blocks)
    """
    env = os.environ.copy()
    env["PATH"] = "/usr/bin:" + env["PATH"]
    result = subprocess.run(
        "git diff --no-index --diff-algorithm=%s --unified=0 --numstat %s %s" % (
            diff_algorithm, src, dest), text=True, stdout=subprocess.PIPE,
        encoding='utf-8', env=env, cwd=os.getcwd(), shell=True)
    result_list = str(result.stdout).splitlines()
    git_scripts = []
    for result_line in result_list:
        if result_line.startswith("@@"):
            git_edits = re.match(r'@@(.*)@@', result_line).group().split()
            git_scripts.append([eval(git_edits[1]), eval(git_edits[2])])
    diffs = [['k', src_line] for src_line in src_lines_list]
    ins_total = 0
    hunks = []
    for git_script in git_scripts:
        deletes, adds = git_script
        if isinstance(deletes, int):
            deletes = (deletes, 1)
        if isinstance(adds, int):
            adds = (adds, 1)
        hunks.append(
            [list(range(abs(deletes[0]), abs(deletes[0]) + deletes[1])), list(range(adds[0], adds[0] + adds[1]))])
        for delete in range(abs(deletes[0]), abs(deletes[0]) + deletes[1]):
            diffs[delete - 1 + ins_total][0] = 'r'
        for add in range(abs(adds[0]), abs(adds[0]) + adds[1]):
            if deletes == (0, 0):
                diffs.insert(add - 1, ['i', dest_lines_list[add - 1]])
            elif deletes[1] == 0:
                diffs.insert(abs(deletes[0]) + deletes[1] + ins_total, ['i', dest_lines_list[add - 1]])
            else:
                diffs.insert(abs(deletes[0]) + deletes[1] + ins_total - 1, ['i', dest_lines_list[add - 1]])
            ins_total += 1
    src_lines, added_lines, diff_scripts = construct_line_data(diffs, indent_tabs_size)
    src_lines_copy = src_lines.copy()
    if added_lines:
        move_mappings, copy_mappings, splits, merges, update_mappings = [], [], [], [], []
        hunks_copy = copy.deepcopy(hunks)
        if identify_split:
            splits = mapping_splits(hunks, src_lines, added_lines, max_split_lines)
        if identify_merge:
            merges = mapping_merges(hunks, src_lines, added_lines, max_merge_lines)
        splits_merges = splits + merges
        if identify_move:
            move_mappings = mapping_block_move(src_lines, added_lines, src_lines_list, dest_lines_list,
                                               min_move_block_length, diff_scripts, pure_mv_block_contain_punc,
                                               count_mv_block_update)
        if identify_copy:
            copy_mappings = mapping_block_copy(src_lines_copy, added_lines, src_lines_list, dest_lines_list,
                                               min_copy_block_length, hunks, diff_scripts, pure_cp_block_contain_punc,
                                               count_cp_block_update)
        if identify_update:
            update_mappings = mapping_line_update(src_lines_list, dest_lines_list, hunks, ctx_length, line_sim_weight,
                                                  sim_threshold)
        update_mappings_copy = update_mappings[:]
        for split_merge in splits_merges:
            for update_change in update_mappings_copy:
                if (split_merge[0][0] - update_change['src_start']) * (
                        split_merge[1][0] - update_change['added_start']) < 0 and update_change in update_mappings:
                    update_mappings.remove(update_change)
        all_mappings = move_mappings[:]
        for copy_mapping in copy_mappings:
            for move_mapping in move_mappings:
                if copy_mapping['src_start'] == move_mapping['src_start'] and copy_mapping['added_start'] == \
                        move_mapping['added_start'] and copy_mapping['block_length'] == move_mapping['block_length']:
                    break
            else:
                all_mappings.append(copy_mapping)
        all_mappings = all_mappings + update_mappings
        km_matches = []
        if all_mappings:
            km_matches, remaining_mappings = km_compute(all_mappings, src_lines_list, dest_lines_list,
                                                        min_move_block_length, min_copy_block_length,
                                                        pure_mv_block_contain_punc, pure_cp_block_contain_punc)
            while remaining_mappings:
                additional_matches, remaining_mappings = km_compute(remaining_mappings, src_lines_list, dest_lines_list,
                                                                    min_move_block_length, min_copy_block_length,
                                                                    pure_mv_block_contain_punc,
                                                                    pure_cp_block_contain_punc)
                km_matches = km_matches + additional_matches
            km_matches.sort(key=lambda x: x['src_start'])
        edit_scripts = generate_edit_scripts_from_match(km_matches, diff_scripts, src_lines_copy, added_lines,
                                                        splits_merges, hunks_copy, len(src_lines_list),
                                                        len(dest_lines_list))
        return edit_scripts
    edit_scripts = generate_edit_scripts_from_diff(diff_scripts)
    return edit_scripts


def BDiffFile(src: str, dest: str, **kwargs) -> None:
    """
    Command-line interface (CLI) wrapper to read source/destination files and generate semantic edit scripts.

    Args:
        src: File path to the source file (original file for comparison). Must be a valid, readable file path.
        dest: File path to the destination file (modified file for comparison). Must be a valid, readable file path.

    Returns:
        None: Does not return a value; instead prints the generated edit scripts directly to the console via `pprint`.

    Notes:
        - Uses UTF-8 encoding to read files (ensure input files are encoded in UTF-8 to avoid decoding errors).
        - Closes file handles explicitly after reading to prevent resource leaks.
        - Relies on the `BDiff` function to generate edit scripts with default configuration (e.g., default diff algorithm,
          minimum block lengths, similarity thresholds). For custom configurations, call the `BDiff` function directly.
    """
    src_infile = open(src, 'r', encoding='utf-8')
    dest_infile = open(dest, 'r', encoding='utf-8')
    src_lines_list = src_infile.read().splitlines()
    dest_lines_list = dest_infile.read().splitlines()
    src_infile.close()
    dest_infile.close()

    pprint(BDiff(src, dest, src_lines_list, dest_lines_list, **kwargs))
