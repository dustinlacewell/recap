import signal
from signal import signal as sigreg


def grace(signum, frame):
    pass


sigreg(signal.SIGTERM, grace)
sigreg(signal.SIGINT, grace)
