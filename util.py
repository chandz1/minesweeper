import time


def start_clock():
    return time.monotonic()


def time_elapsed(start_time):
    return int(time.monotonic() - start_time)
