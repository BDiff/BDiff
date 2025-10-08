# Copyright (c) [2025] [Yan Zhikang, Lu YAO]
# BDiff is licensed under Mulan PubL v2.
# You can use this software according to the terms and conditions of the Mulan PubL v2.
# You may obtain a copy of Mulan PubL v2 at:
#         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PubL v2 for more details.

"""BDiff is a block-aware and accurate text-based difference tool."""

__all__ = ["BDiff", "BDiffFile"]

__version__ = "0.1.0"
__author__ = "Lu Yao <839377654@qq.com>"

from .bdiff import BDiff, BDiffFile
