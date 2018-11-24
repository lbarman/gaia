import subprocess


def get_system_status():

    res = dict()
    res['uptime'] = __try_get_shell_output(["uptime", "-p"])
    res['free'] = __try_get_shell_output(["free", "-h"])
    res['df'] = __try_get_shell_output(["df", "-hT"])
    ps = __try_get_shell_output(["ps", "-Ao", "%cpu,%mem,user,comm", "--sort", "-rss"])
    ps = ps.split('\n')[:10]  # equals | head -n 10
    res['ps'] = '\n'.join(ps)
    return res


def __try_get_shell_output(cmd):
    # eg. cmd = ["ps", "-u"]
    output = "NULL"
    try:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        output = output.decode('utf-8').strip()
    except Exception:
        pass

    return output


def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now".split()
    subprocess.Popen(command)


def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now".split()
    subprocess.Popen(command)