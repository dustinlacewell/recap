from time import gmtime, strftime


def even(i):
    return i + (i % 2)

def timestamp():
    return strftime("%Y-%m-%d-%H-%M-%S", gmtime())
