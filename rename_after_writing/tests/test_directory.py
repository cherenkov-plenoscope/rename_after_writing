import rename_after_writing as rnw
import tempfile
import os
import pytest


def test_contextmanager():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            dir_path = os.path.join(tmp, "123.dir")
            assert not os.path.exists(dir_path)
            filename = "456.txt"

            with rnw.Directory(
                path=dir_path, use_tmp_dir=use_tmp_dir
            ) as rnw_dir:
                with open(os.path.join(rnw_dir, filename), "wt") as foo:
                    foo.write("omg\n")

            assert not os.path.exists(rnw_dir)
            assert os.path.exists(dir_path)

            with open(os.path.join(dir_path, filename), "rt") as foo:
                back = foo.read()

            assert back == "omg\n"


def test_do_not_rename_in_case_of_exception():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            dir_path = os.path.join(tmp, "123.dir")
            assert not os.path.exists(dir_path)

            with pytest.raises(RuntimeError) as on_purpose:
                with rnw.Directory(
                    path=dir_path, use_tmp_dir=use_tmp_dir
                ) as rnw_dir:
                    raise RuntimeError("Break on purpose!")

            assert not os.path.exists(dir_path)
