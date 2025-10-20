import os
import pathlib

import bdiff


def test_bdiff() -> None:
    base_diff_path = pathlib.Path(__file__).parent / "diff-cases"
    left_files = sorted(os.listdir(base_diff_path / "left_files"))
    right_files = sorted(os.listdir(base_diff_path / "right_files"))
    with open(base_diff_path / "edit_scripts", 'r', encoding="utf8") as es_file:
        edit_scripts = eval(es_file.read())
    for left_file, right_file, expected_es in zip(left_files, right_files, list(edit_scripts.values())):
        print(left_file)
        computed_es = bdiff.bdiff(base_diff_path / "left_files" / left_file, base_diff_path / "right_files" / right_file)
        assert computed_es == expected_es, left_file + ": " + str(computed_es)
