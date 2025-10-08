# Copyright (c) [2025] [Yan Zhikang, Lu YAO]
# BDiff is licensed under Mulan PubL v2.
# You can use this software according to the terms and conditions of the Mulan PubL v2.
# You may obtain a copy of Mulan PubL v2 at:
#         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PubL v2 for more details.

"""Entry point for the BDiff application."""

import argparse

import bdiff

_parser = argparse.ArgumentParser(
    prog="bdiff",
    description=bdiff.__doc__,
    epilog="For more information, visit https://github.com/BDiff/BDiff",
)

_parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"%(prog)s v{bdiff.__version__}",
)

_parser.add_argument(
    type=str,
    dest="src",
    help="specify the file path to the source file",
)

_parser.add_argument(
    type=str,
    dest="dest",
    help="specify the file path to the destination file",
)

_parser.add_argument(
    "--diff-algorithm",
    type=str,
    default=argparse.SUPPRESS,
    choices=["Histogram", "Myers"],
    help="git diff algorithm to use for raw change detection",
)

_parser.add_argument(
    "--indent-tabs-size",
    type=int,
    default=argparse.SUPPRESS,
    help="number of spaces a tab character represents",
)

_parser.add_argument(
    "--min-move-block-length",
    type=int,
    default=argparse.SUPPRESS,
    help="minimum number of lines required for a valid move block",
)

_parser.add_argument(
    "--min-copy-block-length",
    type=int,
    default=argparse.SUPPRESS,
    help="minimum number of lines required for a valid copy block",
)

_parser.add_argument(
    "--ctx-length",
    type=int,
    default=argparse.SUPPRESS,
    help="number of context lines (above/below target line) to use for similarity evaluation",
)

_parser.add_argument(
    "--line-sim-weight",
    type=float,
    default=argparse.SUPPRESS,
    help="weight of line content similarity in synthetic similarity score",
)

_parser.add_argument(
    "--sim-threshold",
    type=float,
    default=argparse.SUPPRESS,
    help="minimum synthetic similarity score to qualify lines as 'related'",
)

_parser.add_argument(
    "--max-merge-lines",
    type=int,
    default=argparse.SUPPRESS,
    help="maximum number of source lines allowed for a valid merge operation",
)

_parser.add_argument(
    "--max-split-lines",
    type=int,
    default=argparse.SUPPRESS,
    help="maximum number of destination lines allowed for a valid split operation",
)

_parser.add_argument(
    "--pure-mv-block-contain-punc",
    action="store_true",
    default=argparse.SUPPRESS,
    help="whether move blocks can consist solely of punctuation lines",
)

_parser.add_argument(
    "--pure-cp-block-contain-punc",
    action="store_true",
    default=argparse.SUPPRESS,
    help="whether copy blocks can consist solely of punctuation lines",
)

_parser.add_argument(
    "--disable-counting-mv-block-update",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="count_mv_block_update",
    help="whether to disable counting line-level updates within move blocks",
)

_parser.add_argument(
    "--disable-counting-cp-block-update",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="count_cp_block_update",
    help="whether to disable counting line-level updates within copy blocks",
)

_parser.add_argument(
    "--disable-identifying-move",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="identify_move",
    help="whether to disable detection of move operations",
)

_parser.add_argument(
    "--disable-identifying-copy",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="identify_copy",
    help="whether to disable detection of copy operations",
)

_parser.add_argument(
    "--disable-identifying-update",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="identify_update",
    help="whether to disable detection of single-line update operations",
)

_parser.add_argument(
    "--disable-identifying-split",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="identify_split",
    help="whether to disable detection of line split operations",
)

_parser.add_argument(
    "--disable-identifying-merge",
    action="store_false",
    default=argparse.SUPPRESS,
    dest="identify_merge",
    help="whether to disable detection of line merge operations",
)


if __name__ == "__main__":
    bdiff.BDiffFile(**vars(_parser.parse_args()))
