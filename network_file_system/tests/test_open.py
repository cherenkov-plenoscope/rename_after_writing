import network_file_system as nfs
import tempfile
import os


def test_open_manually():
    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, "123.txt")
        assert not os.path.exists(file)
        f = nfs.open(file, "wt")
        assert not os.path.exists(file)
        f.write("omg\n")
        assert not os.path.exists(file)
        f.close()
        assert os.path.exists(file)


def test_open_context():
    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, "123.txt")

        with nfs.open(file, "wt") as f:
            f.write("ralerale")

        with nfs.open(file, "rt") as f:
            assert f.read() == "ralerale"
