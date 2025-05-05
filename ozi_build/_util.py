import contextlib
import os
import re
import subprocess
import sys
from fileinput import filename

from ._redos import find
from ._sre import SreOpParser
from ._text import TextOutput
from .pep425tags import get_abbr_impl
from .pep425tags import get_abi_tag
from .pep425tags import get_impl_ver
from .pep425tags import get_platform_tag

GET_CHECK = """
from ozi_build import pep425tags
tag = pep425tags.get_abbr_impl() + pep425tags.get_impl_ver()
if tag != pep425tags.get_abi_tag():
    print("{0}-{1}".format(tag, pep425tags.get_abi_tag()))
else:
    print("{0}-none".format(tag))
"""


@contextlib.contextmanager
def cd(path):
    CWD = os.getcwd()

    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(CWD)


wheel_file_template = """\
Wheel-Version: 1.0
Generator: ozi_build
Root-Is-Purelib: {}
"""


def _write_wheel_file(f, supports_py2, is_pure):
    f.write(wheel_file_template.format(str(is_pure).lower()))
    if is_pure:
        if supports_py2:
            f.write("Tag: py2-none-any\n")
        f.write("Tag: py3-none-any\n")
    else:
        f.write(
            "Tag: {0}{1}-{2}-{3}\n".format(
                get_abbr_impl(),
                get_impl_ver(),
                get_abi_tag(),
                get_platform_tag(),
            )
        )


def install_files_path(installpath, target):
    while os.path.basename(installpath) != target:
        installpath = os.path.dirname(installpath)
    return installpath


def meson(*args, builddir=''):
    try:
        return subprocess.check_output(['meson'] + list(args))
    except subprocess.CalledProcessError as e:
        stdout = ''
        stderr = ''
        if e.stdout:
            stdout = e.stdout.decode()
        if e.stderr:
            stderr = e.stderr.decode()
        print("Could not run meson: %s\n%s" % (stdout, stderr), file=sys.stderr)
        try:
            fulllog = os.path.join(builddir, 'meson-logs', 'meson-log.txt')
            with open(fulllog) as f:
                print("Full log: %s" % f.read())
        except IOError:
            print("Could not open %s" % fulllog)  # type: ignore
            pass
        raise e


def meson_configure(*args):
    if 'MESON_ARGS' in os.environ:
        args = os.environ.get('MESON_ARGS').split(' ') + list(args)  # type: ignore
        print("USING MESON_ARGS: %s" % args)
    args = list(args)
    args.append('-Dlibdir=lib')

    meson(*args, builddir=args[0])
