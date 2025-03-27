"""
Network-File-System
===================

A python-library to make moves, copys and writes safer on remote drives.
Writing a file is not atomic. In the worst case the process writing your file
dies while the file is not complete. To at least spot such incomplete files,
all writing-operations (write, move, copy, ...) will be followed by an
atomic move.
"""
from .version import __version__
import uuid
import os
import shutil
import errno
import tempfile
import builtins


def copy(src, dst):
    """
    Tries to copy `src` to `dst`. First `src` is copied to `dst.tmp` and then
    renmaed atomically to `dst`.

    Parameters
    ----------
    src : str
        Path to source.
    dst : str
        Path to destination.
    """
    copy_id = uuid.uuid4().__str__()
    tmp_dst = "{:s}.{:s}.tmp".format(dst, copy_id)
    try:
        shutil.copytree(src, tmp_dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy2(src, tmp_dst)
        else:
            raise
    os.rename(tmp_dst, dst)


def move(src, dst):
    """
    Tries to move `src` to `dst`. In case the move goes across devices,
    `src` is copied first to `dst.tmp` and then renmaed atomically to `dst`.

    Parameters
    ----------
    src : str
        Path to source.
    dst : str
        Path to destination.
    """
    try:
        os.rename(src, dst)
    except OSError as err:
        if err.errno == errno.EXDEV:
            copy(src, dst)
            os.unlink(src)
        else:
            raise


def open(file, mode, use_tmp_dir=False):
    if "r" in str.lower(mode):
        return builtins.open(file=file, mode=mode)
    elif "w" in str.lower(mode):
        return RnwOpen(file=file, mode=mode, use_tmp_dir=use_tmp_dir)
    elif "a" in str.lower(mode):
        return RnwOpen(file=file, mode=mode, use_tmp_dir=use_tmp_dir)
    else:
        raise AttributeError("'mode' must either be 'r', 'w' or  'a'.")


class RnwOpen:
    """
    Write or append to a file.
    """

    def __init__(self, file, mode, use_tmp_dir=False):
        """
        Parameters
        ----------
        file : str
            Path to file.
        mode : str
            Must be either wtite 'w' or append 'a' mode.
        use_tmp_dir : bool, default: False
            Whether to use the '/tmp' directory or not. If False, the temporary
            file is written in the directory where the 'path' is going to be.
            Using '/tmp' can be advantagous when many small write operations
            are expensive in 'path' but efficient in '/tmp'.
        """
        self.file = file
        if use_tmp_dir:
            self.tmp_handle = tempfile.TemporaryDirectory(prefix="rnw_")
            self.tmp_file = os.path.join(self.tmp_handle.name, uuid.uuid4().__str__())
        else:
            self.tmp_handle = None
            self.tmp_file = file + "." + uuid.uuid4().__str__()
        self.mode = mode
        self.ready = False
        self.closed = False

    def close(self):
        self.rc = self.f.close()
        move(src=self.tmp_file, dst=self.file)
        self.closed = True
        self.ready = False

        if self.tmp_handle is not None:
            self.tmp_handle.cleanup()

        return self.rc

    def write(self, payload):
        if not self.ready:
            self.__enter__()
        return self.f.write(payload)

    def __enter__(self):
        if "a" in str.lower(self.mode):
            if os.path.exists(self.file):
                move(src=self.file, dst=self.tmp_file)
        self.f = builtins.open(file=self.tmp_file, mode=self.mode)
        self.ready = True
        return self.f

    def __exit__(self, exc_type, exc_value, exc_tb):
        return self.close()


class Path:
    """
    Adds a uuid to your path and moves 'path.uuid' back to 'path' on exit.
    """

    def __init__(self, path, use_tmp_dir=False):
        """
        Parameters
        ----------
        path : str
            The path to which the temporary path is renamed to after exit.
        use_tmp_dir : bool, default: False
            Whether to use the '/tmp' directory or not. If False, the temporary
            file is written in the directory where the 'path' is going to be.
            Using '/tmp' can be advantagous when many small write operations
            are expensive in 'path' but efficient in '/tmp'.
        """
        self.path = path
        if use_tmp_dir:
            self.tmp_handle = tempfile.TemporaryDirectory(prefix="rnw_")
            self.tmp_path = os.path.join(self.tmp_handle.name, uuid.uuid4().__str__())
        else:
            self.tmp_handle = None
            self.tmp_path = path + "." + uuid.uuid4().__str__()

    def __enter__(self):
        return self.tmp_path

    def __exit__(self, exc_type, exc_value, exc_tb):
        move(src=self.tmp_path, dst=self.path)

        if self.tmp_handle is not None:
            self.tmp_handle.cleanup()
        return

    def __repr__(self):
        return f"{self.__class__.__name__:s}()"
