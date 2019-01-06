import time
import string
import random
import locale
import os
from datetime import datetime
from datetime import timedelta
from ConfigParser import SafeConfigParser

datefmt = "%a, %d %b %Y %H:%M:%S"
datefmt = "%Y-%m-%d %H:%M:%S.%f"


def str2datetime(s, format=datefmt):
    try:
        dt = datetime.strptime(s, format)
    except (ValueError):
        dt = None
    finally:
        return dt


def wait_response_inlog(starttime, timeoutsecs, resp_kword, validation=False):
    keepwaiting = 1
    toseek = 0
    result = {'resp': None, 'validated': None}
    timeout = datetime.now() + timedelta(seconds=timeoutsecs)
    locale.setlocale(locale.LC_TIME, 'en_US')
    while keepwaiting == 1:
        with open("/var/log/faked_nfvo.log") as f:
            for line in f:
                str = line[0:23].replace(",", ".")
                dtlog = str2datetime(str, datefmt)
                # to find the begging of the log
                if dtlog:
                    if (dtlog > starttime):
                        if dtlog < timeout:
                            currtime = datetime.now()
                            if timeout < currtime:
                                print("Timeout is %s, now is %s" % (
                                timeout, currtime))
                                keepwaiting = 0
                                break
                            else:
                                toseek = 1
                        else:
                            print("latest time in log is %s, timeout is %s" % (
                            dtlog, timeout))
                            keepwaiting = 0
                            break
                    else:
                        pass
                # to seek the keyword
                if toseek == 1:
                    if line.find(resp_kword) >= 0:
                        result['resp'] = True
                    if validation:
                        if line.find('Schema validated') >= 0:
                            result['validated'] = True
                        elif line.find('Failed validating') >= 0:
                            result['validated'] = False
                if validation:
                    if (result['resp'] != None) and (
                        result['validated'] != None):
                        keepwaiting = 0
                else:
                    if result['resp'] != None:
                        keepwaiting = 0
            toseek = 0
        print("Timeout is %s, now is %s, just wait response for a while." % (
        timeout, datetime.now()))
        time.sleep(1)
        if timeout <= datetime.now():
            keepwaiting = 0
    return result


def generate_random_string(length, ignore_str=string.punctuation,
                           convert_str=""):
    """
    Return a random string using alphanumeric characters.

    :param length: Length of the string that will be generated.
    :param ignore_str: Characters that will not include in generated string.
    :param convert_str: Characters that need to be escaped (prepend "\\").

    :return: The generated random string.
    """
    r = random.SystemRandom()
    sr = ""
    chars = string.letters + string.digits + string.punctuation
    if not ignore_str:
        ignore_str = ""
    for i in ignore_str:
        chars = chars.replace(i, "")

    while length > 0:
        tmp = r.choice(chars)
        if convert_str and (tmp in convert_str):
            tmp = "\\%s" % tmp
        sr += tmp
        length -= 1
    return sr


def get_nfvo_server_ip_port():
    parser = SafeConfigParser()
    parser.read("/etc/faked_nfvo/cfg.ini")
    log_path = parser.get('DEFAULT', 'LOG')
    cmd = "grep 'Starting faked NFVO server at:' %s | awk {'print $10'}" % log_path
    tmp_str = os.popen(cmd).read().split('\n')[0].split('//')[1]
    nfvo_server_ip = tmp_str.split(':')[0]
    nfvo_server_port = tmp_str.split(':')[1]
    print "NFVO server ip: %s, port: %s" % (nfvo_server_ip, nfvo_server_port)

    return nfvo_server_ip, nfvo_server_port


def generate_random_string(length, ignore_str=string.punctuation,
                           convert_str=""):
    """
    Return a random string using alphanumeric characters.

    :param length: Length of the string that will be generated.
    :param ignore_str: Characters that will not include in generated string.
    :param convert_str: Characters that need to be escaped (prepend "\\").

    :return: The generated random string.
    """
    r = random.SystemRandom()
    sr = ""
    chars = string.letters + string.digits + string.punctuation
    if not ignore_str:
        ignore_str = ""
    for i in ignore_str:
        chars = chars.replace(i, "")

    while length > 0:
        tmp = r.choice(chars)
        if convert_str and (tmp in convert_str):
            tmp = "\\%s" % tmp
        sr += tmp
        length -= 1
    return sr
