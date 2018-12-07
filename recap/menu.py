import sys
from collections import OrderedDict as OD
from subprocess import run


from recap.config import rc

from rofi import Rofi


def quit(ui):
    ui.rofi.exit_with_error("Bye!")


def toggle_fullscreen(ui):
    rc.fullscreen = not rc.fullscreen


def toggle_clip(ui):
    rc.clip = not rc.clip


def toggle_open(ui):
    rc.open = not rc.open


def run_recap(ui, command):
    sys.argv = ['recap', command]
    from recap.cli import cli
    cli()


def do_rec(ui, **kwargs):
    rc.rec.update(kwargs)
    run_recap(ui, 'rec')


def do_cap(ui, **kwargs):
    rc.cap.update(kwargs)
    run_recap(ui, 'cap')


def set_fps(ui):
    rc.rec.fps = ui.rofi.integer_entry('Set FPS')

def choose(ui, title, items):
    index, key = ui.rofi.select(title, items)
    if key == 0:
        return items[index]

def set_rec_destination(ui):
    rc.rec.destination = ui.rofi.prompt("Destination")

def set_rec_filename(ui):
    rc.rec.filename = ui.rofi.prompt("Filename")

def set_rec_bitrate(ui):
    msg = "between {} and {}".format(rc.rec.minrate, rc.rec.maxrate)
    response = ui.rofi.integer_entry("Bitrate", msg,
                                     min=int(rc.rec.minrate),
                                     max=int(rc.rec.maxrate))
    rc.rec.bitrate = response or rc.rec.bitrate

def set_rec_minrate(ui):
    msg = "between 0 and {}".format(rc.rec.bitrate)
    rc.rec.minrate = ui.rofi.integer_entry("Minrate", msg,
                                           min=0, max=int(rc.rec.bitrate))

def set_rec_maxrate(ui):
    rc.rec.maxrate = ui.rofi.integer_entry("Maxrate", min=int(rc.rec.bitrate))


def set_rec_encoding(ui):
    encodings = ["mp4", "webm", "gif"]
    rc.rec.encoding = choose(ui, "Video Encoding", encodings) or rc.rec.encoding

def set_cap_encoding(ui):
    encodings = ["png", "jpg"]
    rc.rec.encoding = choose(ui, "Video Encoding", encodings) or rc.rec.encoding

class RecapRofi(Rofi):
    def _message(self, message, display_bindings):
        message = message or ""
        if display_bindings:
            message += "\n".join(display_bindings)
        return message


class RofiBinding:
    def __init__(self, key, label, handler, condition=None):
        self.key = key
        self.label = label
        self.handler = handler
        self.condition = condition


class RofiEntry:
    def __init__(self, key, label, handler, condition=None):
        self.key = key
        self.label = label
        self.handler = handler
        self.condition = condition


class RecapMenu:
    def __init__(self, prompt, entries, bindings, **options):
        self.prompt = prompt
        self.entries = entries
        self.bindings = bindings
        self.options = options


class RecapUI:
    def __init__(self, bindings, **kwargs):
        self.rofi = RecapRofi(**kwargs)
        self.current = None
        self.stack = []
        self.root_bindings = bindings


    def process_binding(self, index, binding):
        key_name = 'key{}'.format(index)
        key = {key_name: (binding.key, binding.label.format(rc=rc))}
        handler = {index: binding.handler}
        return key, handler


    def collect_bindings(self):
        bindings = [RofiBinding('q', 'quit', exit)]
        if self.stack:
            bindings.append(RofiBinding('b', 'back', RecapUI.pop_menu))
        bindings = bindings + self.root_bindings
        bindings = bindings + self.current.bindings
        keys = {}
        handlers = {}
        for index, binding in enumerate(bindings):
            if binding.condition and (not binding.condition()):
                continue
            key, handler = self.process_binding(index + 1, binding)
            keys.update(key)
            handlers.update(handler)
        return keys, handlers


    def collect_entries(self):
        choices = []
        handlers = {}
        index = 0
        for entry in self.current.entries:
            if entry.condition and (not entry.condition()):
                continue

            choices.append("{e.key}. {e.label}".format(e=entry))
            handlers[index] = entry.handler
            index += 1
        return choices, handlers


    def push_menu(self, menu):
        if self.current:
            self.stack.append(self.current)
        self.current = menu


    def pop_menu(self):
        self.current = self.stack.pop() if self.stack else None


    def run(self):
        while self.current:
            current = self.current
            entries, entry_handlers = self.collect_entries()
            key = 1
            while self.current == current and (key == -1 or key > 0):
                if key == -1:
                    key = 1
                options = {}
                options.update(current.options)
                options['rofi_args'] = options.get('rofi_args', []) + ['-lines', str(len(entries))]
                binds, binding_handlers = self.collect_bindings()
                options.update(binds)
                index, key = self.rofi.select(current.prompt,
                                              entries,
                                              **options)

                if key in binding_handlers:
                    binding_handlers[key](self)

            if self.current == current:
                entry_handlers[index](self)

rec_menu = RecapMenu("Record video", [], [
    RofiBinding('p', 'FPS: {rc.rec.fps}', set_fps),
    RofiBinding('e', 'encoding: {rc.rec.encoding}', set_rec_encoding),
    RofiBinding('r', 'bitrate: {rc.rec.bitrate}', set_rec_bitrate),
    RofiBinding('m', 'minrate: {rc.rec.minrate}', set_rec_minrate),
    RofiBinding('M', 'maxrate: {rc.rec.maxrate}', set_rec_maxrate),
    RofiBinding('S', 'stop', lambda ui: run("pkill -n -SIGINT -f ffmpeg", shell=True),
              lambda: run("pgrep -lf ffmpeg", shell=True, check=False).returncode==0),
    RofiBinding('s', 'start', do_rec),
])

cap_menu = RecapMenu("Capture image", [], [
    RofiBinding('e', 'encoding: {rc.cap.encoding}', set_cap_encoding),
    RofiBinding('c', 'capture', do_cap),
])

main_menu = RecapMenu("Main menu", [
    RofiEntry('r', 'RECORD VIDEO', lambda self: self.push_menu(rec_menu)),
    RofiEntry('c', 'CAPTURE IMAGE', lambda self: self.push_menu(cap_menu)),
], [])


def main():
    ui = RecapUI([
            RofiBinding('f', 'Fullscreen: {rc.fullscreen}', toggle_fullscreen),
            RofiBinding('C', 'Copy after: {rc.clip}', toggle_clip),
            RofiBinding('o', 'Open after: {rc.open}', toggle_open),
        ], rofi_args=['-auto-select'])
    ui.push_menu(main_menu)
    ui.run()


