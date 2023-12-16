import rename_after_writing as rnw
import tempfile
import os


def test_open_manually():
    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, "123.txt")
        assert not os.path.exists(file)
        f = rnw.open(file, "wt")
        assert not os.path.exists(file)
        f.write("omg\n")
        assert not os.path.exists(file)
        f.close()
        assert os.path.exists(file)


def test_open_context():
    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, "123.txt")

        with rnw.open(file, "wt") as f:
            f.write("ralerale")

        with rnw.open(file, "rt") as f:
            assert f.read() == "ralerale"


def test_open_context_append():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "123.txt")

        with rnw.open(path, "wt") as f:
            f.write("123")

        with rnw.open(path, "at") as f:
            f.write("456")

        with rnw.open(path, "rt") as f:
            assert f.read() == "123456"


def test_open_context_append_file_does_not_exist_yet():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "123.txt")

        with rnw.open(path, "at") as f:
            f.write("456")

        with rnw.open(path, "rt") as f:
            assert f.read() == "456"
