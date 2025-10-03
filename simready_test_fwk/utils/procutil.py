# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Process helper class

This module is a extension of psutil module or you can just add some process helpers.
Please notice that only cross-platform codes can be put here.

The following is a simple usage example:
None

The module contains the following public classes:
    ProcUtil

Reference:
    1. python psutil module.
    2. please install vc compiler in windows to get psutil support.

"""
import logging
import re
import sys
import time
import subprocess
import psutil


class ProcUtil(object):
    """
    Process helpers.

    public methods:
        grep_pids: grep and return pid list.
        kill_pids: kill process by pid.
        relaunch_process: restart process.
    """

    log = logging.getLogger()  # auto added class log instance

    def __init__(self):
        pass

    @classmethod
    def get_command_line_by_pid(cls, pid):
        """
        get command line by pid
        please call with admin right.
        """
        proc_cmd_line = psutil.Process(pid).cmdline()
        if proc_cmd_line:
            proc_cmd_line = " ".join([str(x) for x in proc_cmd_line])
            cls.log.info("pid({0}) command line : {1}".format(pid, proc_cmd_line))
        return proc_cmd_line

    @classmethod
    def get_local_port_owner_pid(cls, port, kind="inet", timeout=1):
        """
        get pid which own the local port number
        please call with admin right.
        """
        pid = None
        con = None
        is_found = False
        start_time = time.time()
        end_time = time.time() + timeout
        while is_found is False and time.time() < end_time:
            try:
                local_connections = psutil.net_connections(kind=kind)
                for conn in local_connections:
                    (lip, lport) = conn.laddr
                    if port == lport and conn.pid != 0:
                        con = conn
                        is_found = True
                        pid = con.pid
                        break
            except psutil.AccessDenied:
                # On MACOS, system-wide connections are retrieved by iterating
                # over all processes
                if sys.platform in ("darwin", "linux", "linux2"):
                    cmd_line = "lsof -nP -iTCP:" + str(port) + " | awk 'NR > 1 {print $2}'"
                    pid = subprocess.check_output(cmd_line, shell=True).decode().rstrip()
                    if pid:
                        pid = int(pid.split()[0])  # get the first pid
                        is_found = True
                else:
                    raise
        if is_found:
            time_duration = time.time() - start_time
            cls.log.info("Take {0} seconds to wait for looking for connection.".format(str(time_duration)))
        else:
            cls.log.info("Timeout ({0} seconds) to look for connection.".format(str(timeout)))

        cls.log.info("[grep_port_pid] port {0} is occupied by {1}.".format(port, con))
        return pid if is_found else None

    @classmethod
    def grep_pids(cls, pattern, flags=0, show_log=False, exclude_list=None, exact_match=False):
        """
        filter current process list by command line string using regular expression.

        Args:
            pattern (string): regular expression matching string.
            flags (string): re compile options. (see https://docs.python.org/2/library/re.html)
            exclude_list (string list): exclude process status.
                (see https://psutil.readthedocs.io/en/latest/#process-status-constants)
            exact_match (bool): If True, return PIDs matching the exact pattern.

        Returns:
            matched process list
        """
        pid_list = []
        exclude_list = [psutil.STATUS_STOPPED] if not isinstance(exclude_list, (list, tuple, str)) else exclude_list
        for proc in psutil.process_iter():
            try:
                if proc.status() not in exclude_list:
                    proc_cmdline = " ".join(proc.cmdline())
                    match_pattern = re.compile(pattern, flags)
                    if exact_match:
                        if match_pattern.fullmatch(proc_cmdline) is not None or match_pattern.fullmatch(proc.name()) is not None:
                            if show_log:
                                cls.log.info(
                                    "[grep_pids] found proc.status() = {0} ; proc_cmdline = {1}".format(
                                        proc.status(), proc_cmdline
                                    )
                                )
                            pid_list.append(proc.pid)
                    else:
                        if match_pattern.search(proc_cmdline) is not None:
                            if show_log:
                                cls.log.info(
                                    "[grep_pids] found proc.status() = {0} ; proc_cmdline = {1}".format(
                                        proc.status(), proc_cmdline
                                    )
                                )
                            pid_list.append(proc.pid)
                        elif match_pattern.search(proc.name()) is not None:
                            if show_log:
                                cls.log.info(
                                    "[grep_pids] found proc.status() = {0} ; proc.name() = {1}".format(
                                        proc.status(), proc.name()
                                    )
                                )
                            pid_list.append(proc.pid)
            except:
                pass
        return pid_list

    @classmethod
    def kill_pids(cls, pids=()):
        """
        kill process with provided pids.

        Args:
            pids (tuple): pids to be killed.

        Returns:
            True if there is no exception happened else False.
        """
        ret = True
        for pid in pids:
            try:
                if psutil.pid_exists(pid):
                    proc = psutil.Process(pid=pid)
                    if not proc.name() == "cmd.exe":
                        ppid = proc.ppid()
                        cmd = "tskill" if sys.platform == "win32" else "pkill"
                        cls.log.info(f"Kill {proc.name()} with PID: {pid} and PPID: {ppid}")
                        subprocess.Popen(f"{cmd} {ppid}", shell=True, stdout=subprocess.PIPE)
                        subprocess.Popen(f"{cmd} {pid}", shell=True, stdout=subprocess.PIPE)
                        proc.kill()
                        proc.wait(timeout=5)
            except psutil.NoSuchProcess:
                cls.log.info("Kill process PID: {0}, {1}".format(pid, "already killed."))
            except Exception as ex:
                ret = False
                cls.log.info("Exception : Cannot kill process %s.", str(ex))
        return ret

    @classmethod
    def kill_omni_ui_pids(cls, pids=()):
        """
        kill process with provided pids.
        This function is used for killing OmniUI apps

        Args:
            pids (tuple): pids to be killed.

        Returns:
            True if there is no exception happened else False.
        """
        ret = True
        for pid in pids:
            try:
                proc = psutil.Process(pid=pid)
                cls.log.info("Kill process PID: {0}, NAME: {1}".format(proc.pid, proc.name()))
                proc.kill()
                proc.wait(timeout=20)
            except psutil.NoSuchProcess:
                cls.log.info("Kill process PID: {0}, {1}".format(pid, "already killed."))
            except Exception as ex:
                ret = False
                cls.log.info("Exception : Cannot kill process %s.", str(ex))
        return ret

    @classmethod
    def kill_process(cls, proc_name, flags=0, show_log=False):
        """kill process with provided process name"""
        count_pids = len(ProcUtil.grep_pids(proc_name, flags=flags, show_log=show_log))
        if count_pids > 0:
            ProcUtil.kill_pids(ProcUtil.grep_pids(proc_name))
            time.sleep(2)
            count_pids = len(ProcUtil.grep_pids(proc_name, flags=flags, show_log=show_log))
            return count_pids == 0

        cls.log.info("{0} is not alive, skip ...".format(proc_name))
        return True

    @staticmethod
    def get_background_processes(search: str = None):
        """retrieves all the process running
        :param search: to filter results
        for eg, to find omni processes, proc = 'omni'
        """
        procs = []
        for conn in psutil.net_connections():
            pid = conn.pid
            if psutil.pid_exists(pid):
                proc_name = psutil.Process(pid).name()
                procs.append((pid, proc_name))
        if search:
            return [proc for proc in procs if search in proc[1].lower()]
        return procs

    @classmethod
    def relaunch_process(cls, pattern, flags=0):
        """
        restart process with pattern matching
        """
        ret = True
        for pid in cls.grep_pids(pattern, flags=flags):
            try:
                proc = psutil.Process(pid=pid)
                original_cmdline = proc.cmdline()
                cls.log.info("kill %s." % original_cmdline)
                proc.kill()
                time.sleep(1)
            except psutil.NoSuchProcess:
                cls.log.info("Kill process PID: {0}, {1}".format(pid, "already killed."))
            cls.log.info("start %s", original_cmdline)
            if subprocess.Popen(original_cmdline, close_fds=True, shell=True) is None:
                ret = False
                cls.log.info("fail to launch %s." % original_cmdline)
        return ret

    @classmethod
    def check_cpu_percent(cls, pid_name, account=20, goal=60, duration=2):
        """
        :param pid_name: pid_name is the pid which costs cpu usage percent.
        :param account:  sampling frequency
        :param goal: the cpu usage should be under 60% (by default)
        :param duration: sampling duration in seconds
        :return: true or false
        """
        cpu_usage_list_all = ProcUtil.get_cpu_usage_by_pid(pid_name, account, duration)

        return sum(cpu_usage_list_all) / len(cpu_usage_list_all) < goal

    @classmethod
    def get_cpu_usage_by_pid(cls, pid_name, account=20, duration=2):
        """
        :param pid_name: pid_name is the pid which costs cpu usage percent.
        :param account:  sampling frequency
        :param duration: sampling duration in seconds
        :return: the list of all cpu usage values
        """
        target_pid = None
        cpu_usage_list = []
        all_pids = psutil.pids()
        for pid in all_pids:
            if psutil.Process(pid).name() == pid_name:
                target_pid = pid
                break
        assert target_pid is not None, "Error Occurred! PID cannot be None"
        cls.log.info("[INFO] PID name to monitor : {0}".format(pid_name))
        cls.log.info("[INFO] Monitoring duration : {0}x{1}={2} seconds".format(account, duration, account * duration))
        for _ in range(account):
            time.sleep(duration)
            current_cpu_usage = psutil.Process(target_pid).cpu_percent(interval=1)
            cpu_usage_list.append(current_cpu_usage)

        cls.log.info("[INFO] All CPU usage values in percentage : ")
        cls.log.info(cpu_usage_list)

        return cpu_usage_list

    @classmethod
    def get_average_cpu_usage_value(cls, pid_name, account=20, duration=2):
        """
        :param cpu_usage_list_all: a list contant cpu usage values
        :return: return the average of middle 1/3 values (After sorting list)
        """
        cpu_usage_list_all = ProcUtil.get_cpu_usage_by_pid(pid_name, account, duration)

        cpu_usage_list_all.sort(reverse=True)
        count_all = len(cpu_usage_list_all)
        cpu_usage_list_mid = cpu_usage_list_all
        cpu_usage_mid_avg = 0
        count_mid = 0
        count_skip = 0

        if count_all >= 3:
            count_skip = int(count_all / 3)
        for _ in range(count_skip):
            del cpu_usage_list_mid[0]  # Remove value from front of the list
            del cpu_usage_list_mid[-1]  # Remove value from rear of the list

        count_mid = len(cpu_usage_list_mid)
        cpu_usage_mid_avg = sum(cpu_usage_list_mid) / count_mid
        sampling_str = "(Sampling {0} of {1} values in the middle)".format(count_mid, count_all)
        cls.log.info("[INFO] Middle CPU usage values in percentage{0} : ".format(sampling_str))
        cls.log.info(cpu_usage_list_mid)
        cls.log.info("[INFO] Average of CPU usage values{0} : {1} %".format(sampling_str, cpu_usage_mid_avg))

        return cpu_usage_mid_avg

    @classmethod
    def execute_shell_command(cls, cmd):
        """
        Executes the command passed in under shell
        Parameters:
        Returns:
             N/A
        """
        child = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        ret_value = True
        info = []
        while True:
            err = child.stderr.read()
            out = child.stdout.read()
            if out != "":
                cls.log.info(out)
                ret_value = ret_value and True
                info.append(out)
            if err == "" and child.poll() != None:
                break
            if err != "":
                ret_value = ret_value and False
                info.append(err)
                cls.log.info(err)
                sys.stdout.write(err)
                sys.stdout.flush()
        child.stderr.close()
        child.stdout.close()
        return ret_value, info

    @classmethod
    def execute_command(cls, command, print_output=True):
        """Run the command and return stdout
        !!! CAUTION - DO NOT RUN COMMAND THAT WILL GENERATE
                      HUGE AMOUNT OF CONSOLE OUTPUT.
        !!! IT WILL CAUSE UNKNOW PROGRAM HANG UP WHEN IT'S
            RUN OUT OF BUFFER BY CONSOLE OUT.
        """
        p_out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p_out.communicate()
        if print_output:
            cls.log.info("<<<=============================================================>>>")
            cls.log.info("Command output : %s", stdout)
            cls.log.info("<<<=============================================================>>>")
            cls.log.info("stderr : %s", (stderr))
        return stdout

    @classmethod
    def check_process_killed(cls, proc_name, flags=0, show_log=False):
        """check process with provided process name and return true if precess is alive else false"""

        count_pids = len(ProcUtil.grep_pids(proc_name, flags=flags, show_log=show_log))
        if count_pids == 0:
            cls.log.info("{0} is not alive".format(proc_name))
            return True
        else:
            cls.log.info("{0} is alive".format(proc_name))
            return False

    @classmethod
    def count_running_instances_of_proc(cls, process_name):
        """
        Function to count all running instances of given process
        """
        instances_count = 0

        all_processes = list(psutil.process_iter(['pid', 'name']))
        cls.log.info(f"Trying to extract all running instances of proc: {process_name}")

        # Count the number of instances of the specified process name
        instances_count = sum(1 for process in all_processes if process.info['name'] == process_name)
        cls.log.info(f"Running instances of process {process_name}: {instances_count}")

        return instances_count
