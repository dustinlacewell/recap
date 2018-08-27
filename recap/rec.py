import os
import tempfile
from subprocess import run

from recap import util


def input_args(source, fmt, size):
    source_arg = "-i {}".format(source)
    format_arg = "-f {}".format(fmt)
    size_arg = "-s {}".format(size)
    return " ".join([format_arg, size_arg, source_arg])


def capture_args(x, y, w, h):
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
    return video_args("libx264", "yuv420p", framerate,
                      bitrate, minrate, maxrate)


def webm_args(framerate, bitrate, minrate, maxrate):
    return video_args("libvpx-vp9", "yuv444p", framerate,
                      bitrate, minrate, maxrate)


def run_ffmpeg(input_args, video_args, filename, extras=""):
    command = "ffmpeg -y {} {} {} {}".format(input_args,
                                             video_args,
                                             extras,
                                             filename)
    util.quiet(command, shell=True,
               stdout=open(os.devnull, 'wb'),
               stderr=open(os.devnull, 'wb'))


def run_mp4(filename, input_args, fps, rate, minrate, maxrate):
    video_args = mp4_args(fps, rate, minrate, maxrate)
    run_ffmpeg(input_args, video_args, filename)


def run_webm(filename, input_args, fps, rate, minrate, maxrate):
    video_args = webm_args(fps, rate, minrate, maxrate)
    run_ffmpeg(input_args, video_args, filename)


def run_gif(filename, input_args, fps, rate, minrate, maxrate):
    run_mp4('/tmp/tmp.mp4', input_args, fps, rate, minrate, maxrate)
    run('ffmpeg -y -i /tmp/tmp.mp4 -filter_complex "[0:v] palettegen" /tmp/palette.png', shell=True)
    run('ffmpeg -y -i /tmp/tmp.mp4 -i /tmp/palette.png -filter_complex "[0:v][1:v] paletteuse" {}'.format(filename), shell=True)
