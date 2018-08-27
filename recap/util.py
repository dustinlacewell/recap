import os
from subprocess import check_output, CalledProcessError, run
from time import gmtime, strftime

import click


def even(i):
    return i + (i % 2)


def select(fullscreen=False, extra=""):
    if fullscreen:
        output = check_output(
            "xdpyinfo | awk '/dimensions/{print $2}'", shell=True)
        output = output.decode('utf-8').strip()
        w, h = output.split("x")
        return 0, 0, w, h
    else:
        try:
            command = 'slop -b 5 -f "%x,%y,%w,%h,%g,%i" {}'.format(extra)
            output = check_output(command, shell=True)
            return output.decode('utf-8').split(",")[:4]
        except CalledProcessError:
            click.echo("slop bailed because you pressed a key or something")
            exit()


def rcfmt(rc, string):
    return strftime(string, gmtime()).format(**rc)


def quiet(*args, **kwargs):
    kwargs.update(dict(
        stdout=open(os.devnull, 'wb'),
        stderr=open(os.devnull, 'wb')))
    return run(*args, **kwargs)


def quiet_output(*args, **kwargs):
    kwargs.update(dict(
        stdout=open(os.devnull, 'wb'),
        stderr=open(os.devnull, 'wb')))
    return check_output(*args, **kwargs)
