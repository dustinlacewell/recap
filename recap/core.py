from functools import update_wrapper
from os.path import expanduser
from pathlib import Path as P
from subprocess import run, Popen, PIPE, check_output, DEVNULL

import click
from click.globals import get_current_context

from attrdict import AttrDict as A

from recap.config import rc
from recap.merge import dict_merge
from recap.util import select, rcfmt


def group(f):
    def wrapper(*args, **kwargs):
        ctx = get_current_context()
        ctx.obj = A(dict_merge(rc, kwargs))

        return f(*args, **kwargs)
    return update_wrapper(wrapper, f)


def command(f):
    def wrapper(*args, **kwargs):
        ctx = get_current_context()
        # figure out what command we're running
        cmd_name = ctx.command.name
        # get the current rc
        rc = ctx.obj
        # and the subrc for the current command
        subrc = rc.get('cmd_name', {})
        # merge the click cli args with the subrc
        rc[cmd_name] = subrc = A(dict_merge(subrc, kwargs))

        rc.selection = select(rc.fullscreen, rc.slop)

        # compute the target filename
        destination = P(rcfmt(rc, expanduser(subrc.destination)))
        filename = (rcfmt(rc, subrc.filename) + "." + subrc.encoding)
        rc.target = destination / filename

        # ensure target path exists
        destination.mkdir(parents=True, exist_ok=True)

        # execute the command
        f(rc)

        click.echo(rc.target)

        if rc.cap.upload:
            cmd = "imgur-screenshot --open false {}".format(rc.target)
            # cmd = ["zsh", "-c",
            #        "'imgur-screenshot --open false {}'".format(rc.target)]
            output = Popen(cmd, shell=True, stdout=PIPE)

            for line in output.stdout:
                if line.startswith(b"image"):
                    parts = line.split()
                    rc.target = parts[-1]
                    break

        if rc.clip:
            # "primary"
            xsel_proc = Popen(['xclip', '-i', '-sel', 'p'], stdin=PIPE)
            xsel_proc.communicate(str(rc.target).encode('utf-8'))
            # "clipboard"
            xsel_proc = Popen(['xclip', '-i', '-sel', 'c'], stdin=PIPE)
            xsel_proc.communicate(str(rc.target).encode('utf-8'))

        if rc.open:
            run("xdg-open {}".format(rc.target), shell=True)

    return update_wrapper(wrapper, f)
