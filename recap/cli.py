import sys
import os
import pathlib
from subprocess import check_output, run

import click

from recap import util

def sel(fullscreen=False):
    if fullscreen:
        output = check_output("xdpyinfo | awk '/dimensions/{print $2}'", shell=True)
        output = output.decode('utf-8')
        w,h = output.split("x")
        return 0,0,w,h,None,None
    else:
        output = check_output('slop -b 5 -f "%x,%y,%w,%h,%g,%i"', shell=True)
        return output.decode('utf-8').split(",")

def input_args(source, fmt, size):
    source_arg = "-i {}".format(source)
    format_arg = "-f {}".format(fmt)
    size_arg = "-s {}".format(size)
    return " ".join([format_arg, size_arg, source_arg])

def capture_args(fullscreen):
    x,y,w,h,g,i = sel(fullscreen)
    size = "{}x{}".format(util.even(int(w)), util.even(int(h)))
    source = ":0.0+{},{}".format(util.even(int(x)), util.even(int(y)))
    return input_args(source, "x11grab", size)

def video_args(codec, fmt, framerate, bitrate, minrate, maxrate):
    framerate = "-framerate {}".format(framerate)
    codec = "-c:v {}".format(codec)
    pix_fmt = "-pix_fmt {}".format(fmt)
    bitrates = "-b:v {}k -minrate {}k -maxrate {}k".format(bitrate,
                                                        minrate,
                                                        maxrate)
    return "{} {} {} {}".format(framerate, codec, pix_fmt, bitrates)

def mp4_args(framerate, bitrate, minrate, maxrate):
    return video_args("libx264", "yuv420p", framerate, bitrate, minrate, maxrate)

def webm_args(framerate, bitrate, minrate, maxrate):
    return video_args("libvpx-vp9", "yuv444p", framerate, bitrate, minrate, maxrate)

def filename(ext):
    return os.path.join("~","www","caps", "{}.{}".format(util.timestamp(), ext))

def do(input_args, video_args, filename, extras=""):
    command = "ffmpeg {} {} {} {}".format(input_args, video_args, extras, filename)
    print(command)
    run(command, shell=True)

def do_mp4(input_args, fps, rate, minrate, maxrate):
    file_name = filename(encoding)
    video_args = mp4_args(fps, rate, minrate, maxrate)
    do(input_args, video_args, file_name)

def do_gif(input_args, fps, rate, minrate, maxrate):
    mp4_name = filename("mp4")
    gif_name = filename("gif")
    video_args = mp4_args(fps, rate, minrate, maxrate)
    do(input_args, video_args, mp4_name)
    run('ffmpeg -i {} -filter_complex "[0:v] palettegen" /tmp/palette.png'.format(mp4_name), shell=True)
    run('ffmpeg -i {} -i /tmp/palette.png -filter_complex "[0:v][1:v] paletteuse" {}'.format(mp4_name, gif_name), shell=True)


@click.group()
def cli():
    """Simple screen recorder and capture tool."""
    pass

@click.command()
@click.option('--full', is_flag=True)
@click.option('--fps', default=60)
@click.option('--encoding', '-e', type=click.Choice(['mp4', 'webm', 'gif']), default="mp4")
@click.option('--rate', default=2500)
@click.option('--minrate', default=1000)
@click.option('--maxrate', default=3000)
def rec(full, fps, encoding, rate, minrate, maxrate):
    """Record Video"""
    input_args = capture_args(full)
    file_name = filename(encoding)

    if encoding == "mp4":
        file_name = filename(encoding)
        video_args = mp4_args(fps, rate, minrate, maxrate)
        do(input_args, video_args, file_name)
    elif encoding == "gif":
        pass
    else:
        video_args = webm_args(fps, rate, minrate, maxrate)
        do(input_args, video_args, file_name)
    click.echo(os.path.expanduser(file_name))

@click.command()
@click.option('--full', is_flag=True)
@click.option('--upload', is_flag=True)
def cap(full, upload):
    """Capture Screenshot"""
    file_name = filename("png")
    full_arg = "" if full else "-s"
    run("maim {} {}".format(full_arg, file_name), shell=True)
    if upload:
        run("imgur-screenshot {}".format(file_name))
    click.echo(os.path.expanduser(file_name))

@click.command()
def test():
    file = pathlib.Path(sys.prefix) / pathlib.Path("recap/data/config.toml")
    click.echo(file.read_text("utf-8"))

cli.add_command(cap)
cli.add_command(rec)
cli.add_command(test)
