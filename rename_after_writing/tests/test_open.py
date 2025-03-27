import rename_after_writing as rnw
import tempfile
import os


def test_open_manually():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            file = os.path.join(tmp, "123.txt")
            assert not os.path.exists(file)
            f = rnw.open(file, "wt", use_tmp_dir=use_tmp_dir)
            assert not os.path.exists(file)
            f.write("omg\n")
            assert not os.path.exists(file)
            f.close()
            assert os.path.exists(file)


def test_open_context():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            file = os.path.join(tmp, "123.txt")

            with rnw.open(file, "wt", use_tmp_dir=use_tmp_dir) as f:
                f.write("ralerale")

            with rnw.open(file, "rt", use_tmp_dir=use_tmp_dir) as f:
                assert f.read() == "ralerale"


def test_open_context_append():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "123.txt")

            with rnw.open(path, "wt", use_tmp_dir=use_tmp_dir) as f:
                f.write("123")

            with rnw.open(path, "at", use_tmp_dir=use_tmp_dir) as f:
                f.write("456")

            with rnw.open(path, "rt", use_tmp_dir=use_tmp_dir) as f:
                assert f.read() == "123456"


def test_open_context_append_file_does_not_exist_yet():
    for use_tmp_dir in [False, True, None]:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "123.txt")

            with rnw.open(path, "at", use_tmp_dir=use_tmp_dir) as f:
                f.write("456")

            with rnw.open(path, "rt", use_tmp_dir=use_tmp_dir) as f:
                assert f.read() == "456"
