import click

from recap import util, signals
from recap.rec import capture_args, run_mp4, run_gif, run_webm
from recap.config import rc
from recap.core import group, command


# import pdb; pdb.set_trace()
@click.group()
@click.option('--fullscreen/--select', default=rc.fullscreen)
@click.option('--clip/--no-clip', default=rc.clip)
@click.option('--open/--no-open', default=rc.open)
@click.option('--slop', default=rc.slop)
@group
def cli(*args, **kwargs):
    """Simple screen recorder and capture tool."""
    pass


@click.command()
@click.option('--destination', default=rc.rec.destination)
@click.option('--filename', default=rc.rec.filename)
@click.option('--fps', default=rc.rec.fps)
@click.option('--bitrate', default=rc.rec.bitrate)
@click.option('--minrate', default=rc.rec.minrate)
@click.option('--maxrate', default=rc.rec.maxrate)
@click.option('--encoding', '-e',
              type=click.Choice(['mp4', 'webm', 'gif']),
              default=rc.rec.encoding)
@command
def rec(rc):
    """Record Video"""
    x, y, w, h = rc.selection
    input_args = capture_args(x, y, w, h)

    handler = dict(mp4=run_mp4, gif=run_gif, webm=run_webm)[rc.rec.encoding]

    handler(rc.target, input_args, rc.rec.fps,
            rc.rec.bitrate, rc.rec.minrate, rc.rec.maxrate)


@click.command()
@click.option('--destination', default=rc.cap.destination)
@click.option('--filename', default=rc.cap.filename)
@click.option('--link', default=rc.cap.link)
@click.option('--webroot', default=rc.cap.webroot)
@click.option('--encoding', '-e',
              type=click.Choice(['png', 'jpg']),
              default=rc.cap.encoding)
@command
def cap(rc):
    """Capture Screenshot"""
    x, y, w, h = rc.selection
    geom = "-g {}x{}-{}+{}".format(w, h, x, y)
    cmd = "maim {} {}".format(geom, rc.target)
    click.echo(cmd)
    util.quiet(cmd, shell=True)


cli.add_command(cap)
cli.add_command(rec)


def main():
    cli()
