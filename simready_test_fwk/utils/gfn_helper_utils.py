import os
import sys
import logging
import json
import subprocess
import time
import shlex
from omniui.utils.utility_functions import (
    get_service_account_password,
    read_json_data,
)

from utils.utility_functions import kill_process_by_port

SSH_PUBLIC_KEY = os.sep.join([os.path.expanduser("~"), ".ssh", "id_rsa.pub"])
SSH_PRIVATE_KEY = os.sep.join([os.path.expanduser("~"), ".ssh", "id_rsa"])
from utils.configuration_loader import get_config


class GFNUtil:
    """GFN Session Util Helper Class"""

    gfn_config = read_json_data("gdn_stream_config.json")
    username = get_config().automation_service_account.user02
    log = logging.getLogger()
    streaming_user_id = get_service_account_password(username, "gfn_stream_id")
    seat_description = "omniverse_qa"
    gfn_seat: dict

    def _get_all_instances_info(self):
        command = f"{self.gfn_config['cli_binary']} vdk describe {self.gfn_config['default_configure_parameters']}"
        if sys.platform != "win32":
            command = "./" + command
        parsed_command = shlex.split(command)
        result = None
        try:
            result = subprocess.run(
                parsed_command,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if result.stdout:
                debug_seat_dic = json.loads(result.stdout)
                if "error" in debug_seat_dic:
                    self.log.error(debug_seat_dic)
            else:
                self.log.error(result.stderr)
                raise RuntimeError(f"{result.stderr}")

            return debug_seat_dic

        except Exception as e:
            self.log.error(f"get_all_instances_info: {str(e)}")
            return {"error": str(e)}

    def _fetch_gfn_data(self):
        """Fetches GFN seat connection data"""
        connection_info = self.gfn_seat["connectionInfo"]
        ssh_user_name = connection_info["sshUser"]

        ssh_config = None
        for item in connection_info["portConfiguration"]:
            if item["appLevelProtocol"] == "SSH":
                ssh_config = item
                break

        user_config = None
        for item in connection_info["rdpCredentials"]:
            if item["user"] == ssh_user_name:
                user_config = item
                break

        connection_data = {
            "server_ip": ssh_config["accessIp"],
            "user": user_config["user"],
            "port": ssh_config["externalPort"],
        }
        return connection_data

    def create_instance(self):
        """Creates a new GFN session"""
        command = (
            f"{self.gfn_config['cli_binary']} vdk create --instance-type {self.gfn_config['instance_type']} --seat-description"
            f" {self.seat_description} --streaming-user-id {self.streaming_user_id} --password-key-dir-path '{self.gfn_config['pass_key_dir']}' --ssh --ssh-keys"
            f" '{SSH_PUBLIC_KEY},{SSH_PRIVATE_KEY}' --os-type windows {self.gfn_config['default_configure_parameters']}"
        )
        if sys.platform != "win32":
            subprocess.run(["chmod", "+x", self.gfn_config["cli_binary"]])
            command = "./" + command

        self.log.info(f"Instance cmd: {command}")
        parsed_command = shlex.split(command)

        result_stdout = None
        result_stderr = None
        return_code = None

        try:
            self.log.info(
                f"Try to create instance(est. 180~300sec) - {self.streaming_user_id} {self.seat_description}"
            )

            with subprocess.Popen(
                parsed_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            ) as process:
                start_time = time.time()
                elapsed_time = 0
                while True:
                    if process.poll() is not None:
                        break
                    current_time = time.time() - start_time
                    if current_time - elapsed_time >= 10:
                        elapsed_time = current_time
                        self.log.info(
                            f"Command still running... Elapsed time: {elapsed_time:.1f} seconds"
                        )
                    time.sleep(0.5)

                result_stdout, result_stderr = process.communicate()
                return_code = process.returncode

            self.log.info(f"Process return code{return_code}")

            if process.returncode != 0 or result_stderr:
                raise RuntimeError("Failed to create gfn instance")

            self.gfn_seat = json.loads(result_stdout)
            self.log.info(f"Creation response: {self.gfn_seat}")

            if not (
                self.gfn_seat.get("status", False)
                and self.gfn_seat["status"] != "FAILED"
            ):
                raise RuntimeError("Seat was not created")

        except Exception as e:
            self.log.error(f"create_debug_seat: {str(result_stderr)}")
            raise RuntimeError from e

    def delete_instance(self, seat_id):
        """Deletes the given GFN session"""
        self.log.info(f"Try to delete '{seat_id}'")
        command = f"{self.gfn_config['cli_binary']} vdk delete -i {seat_id} {self.gfn_config['default_configure_parameters']}"
        if sys.platform != "win32":
            command = "./" + command
        parsed_command = shlex.split(command)
        try:
            with subprocess.Popen(
                parsed_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            ) as process:
                start_time = time.time()
                elapsed_time = 0
                while True:
                    if process.poll() is not None:
                        break
                    current_time = time.time() - start_time
                    if current_time - elapsed_time >= 10:
                        elapsed_time = current_time
                        self.log.info(
                            f"Command still running... Elapsed time: {elapsed_time:.1f} seconds"
                        )
                    time.sleep(0.5)

            self.log.info(f"Deleted seat instance {seat_id}")
        except Exception as e:
            self.log.error(f"create_debug_seat: {str(e)}")
            raise RuntimeError from e

    def create_ssh_tunnel(self, ext_port: str):
        """Create SSH tunnel"""
        connection_details = self._fetch_gfn_data()

        tunnel_command = f"-m hmac-sha2-256 -f -N -L 127.0.0.1:8888:127.0.0.1:8888 -L 127.0.0.1:{ext_port}:127.0.0.1:{ext_port}"

        ssh_command = (
            f"ssh {tunnel_command} {connection_details['user']}@{connection_details['server_ip']} -p"
            f" {connection_details['port']} -i {SSH_PRIVATE_KEY} -o LogLevel=error -o StrictHostKeyChecking=no"
        )
        self.log.info(f"Run Local Command: {ssh_command}")

        kill_process_by_port(8888)
        kill_process_by_port(ext_port)

        self.ssh_process = subprocess.Popen(ssh_command, shell=True)
        time.sleep(10)

        if self.ssh_process.poll() is not None:
            self.log.error("SSH tunnel setup failed")
            # raise RuntimeError("SSH tunnel setup failed")
        else:
            self.log.info("SSH tunnel setup successful")

    def delete_all_instance(self):
        """Delete all the GFN sessions"""
        debug_seat_dic = self._get_all_instances_info()
        if "debugSeats" in debug_seat_dic:
            self.log.info(
                f"{len(debug_seat_dic['debugSeats'])} instances will be terminated..."
            )
            for debug_seat in debug_seat_dic["debugSeats"]:
                self.delete_instance(debug_seat["seatId"])
                time.sleep(0.5)  # give few interval between request
