import signal
# Source idea from https://gist.github.com/nonZero/2907502
# Handles console strg + c to exit script properly


class InterruptHandler(object):
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig
        self.released = None

    def __enter__(self):
        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)
        self.released = True
        return True
