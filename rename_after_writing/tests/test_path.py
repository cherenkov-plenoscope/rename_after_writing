import rename_after_writing as rnw
import tempfile
import copy
import os
import glob
import pytest


def test_do_not_rename_in_case_of_exception():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            file = os.path.join(tmp, "123.txt")
            assert not os.path.exists(file)

            with pytest.raises(RuntimeError) as on_purpose:
                with rnw.Path(path=file, use_tmp_dir=use_tmp_dir) as rnw_file:
                    with open(rnw_file, "wt") as foo:
                        foo.write("omg\n")
                    raise RuntimeError("Break on purpose!")

            assert not os.path.exists(file)


def test_contextmanager():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            file = os.path.join(tmp, "123.txt")
            assert not os.path.exists(file)

            with rnw.Path(path=file, use_tmp_dir=use_tmp_dir) as rnw_file:
                with open(rnw_file, "wt") as foo:
                    foo.write("omg\n")

            assert not os.path.exists(rnw_file)
            assert os.path.exists(file)

            with open(file, "rt") as foo:
                back = foo.read()

            assert back == "omg\n"


def test_do_not_alter_input_path():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:

            original_path = os.path.join(tmp, "123.txt")
            original_path_copy = copy.copy(original_path)

            with rnw.Path(
                path=original_path, use_tmp_dir=use_tmp_dir
            ) as rnw_path:
                with open(rnw_path, "wt") as foo:
                    foo.write("omg\n")

            num_files_in_outdir = len(glob.glob(os.path.join(tmp, "*")))
            assert num_files_in_outdir == 1

            assert os.path.exists(original_path_copy)
            assert original_path == original_path_copy
