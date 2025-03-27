import rename_after_writing as rnw
import tempfile
import os


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
