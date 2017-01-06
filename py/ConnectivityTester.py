import socket
from collections import deque
import threading
import time

class Tester:
    """ Takes a given ip / hostname and optionally a port that is expected
    to be open (i.e. accepts connections) and one that's expected to be
    closed (i.e. refuses connections) and provides a fast synchronous API
    for determinig if the host is up.
    """
    def __init__(self, ip, closed_port=80, open_port=62078):
        self.ip = ip
        self.closedPort = closed_port
        self.openPort = open_port

        self.lastN = deque(maxlen=15)
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        while True:
            try:
                self.lastN.append(_is_up(self.ip, self.closedPort, self.openPort))
            except Exception as e:
                print("Error checking is_up on ip {ip}: {e}".format(
                    ip=self.ip, e=e))
            time.sleep(0.5)

    def isUp(self):
        while len(self.lastN) == 0:
            pass
        return any(self.lastN)


def _is_up(host:str, closed_port:int, open_port:int):
    """ Take a hostname to check and a port that should send a
    connection reset if the device is up.  Return a boolean about
    whether it's up.
    If the answer is True, it's definitely up.
    If False, it could be up or not.
    """
    s = _getsocket()
    try:
        s.connect((host, closed_port))
    except ConnectionRefusedError:
        return True
    except OSError:
        return False
    except socket.timeout:
        s2 = _getsocket()
        s2.settimeout(2)
        try:
            s2.connect((host, open_port))
        except socket.timeout:
            return False
        except OSError:
            return False
        return True

def _getsocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    return s
