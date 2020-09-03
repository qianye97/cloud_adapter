import os


def can_ping(ip):
    res = os.system("ping {0} -c 2".format(ip))
    if res == 0:
        return True
    return False
