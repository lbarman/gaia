import subprocess


class System:

    @staticmethod
    def get_system_status():

        res = dict()
        res['uptime'] = System.__try_get_shell_output(["uptime", "-p"])
        res['memory'] = System.__try_get_shell_output(["free", "-h"])
        res['disk_usage'] = System.__try_get_shell_output(["df", "-hT"])
        ps = System.__try_get_shell_output(["ps", "-Ao", "%cpu,%mem,user,comm", "--sort", "-rss"])
        ps = ps.split('\n')[:10]  # equals | head -n 10
        res['processes'] = '\n'.join(ps)
        return res

    @staticmethod
    def __try_get_shell_output(cmd):
        # eg. cmd = ["ps", "-u"]
        output = "NULL"
        try:
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            output = output.decode('utf-8').strip()
        except Exception:
            pass

        return output

    @staticmethod
    def reboot():
        command = "/usr/bin/sudo /sbin/shutdown -r now".split()
        subprocess.Popen(command)

    @staticmethod
    def shutdown():
        command = "/usr/bin/sudo /sbin/shutdown -h now".split()
        subprocess.Popen(command)

class MockSystem(System):

    reboot_called = False
    shutdown_called = False

    @staticmethod
    def get_system_status():
        res = dict()
        res['uptime'] = "uptime"
        res['memory'] = "memory"
        res['disk_usage'] = "disk_usage"
        res['processes'] = "processes"
        return res

    def reboot(self):
        self.reboot_called = True

    def shutdown(self):
        self.shutdown_called = True