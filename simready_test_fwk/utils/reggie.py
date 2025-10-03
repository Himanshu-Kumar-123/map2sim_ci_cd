"""
Reggie class for Regression detection
"""
import json
import os
import platform
import GPUtil


class Reggie:
    """
    Base class for Reggie to generate json artifacts.
    """
    fingerprint = {}
    metadata = {}
    project = "OVQA"
    benchmark_suite = "AppSanity"
    metadata = {
        "app_version": "app_version"
    }
    metrics = {}  # dictionary of metrics
    benchmark = {}
    json_name = ""
    json_ext = "_reggie.json"

    def __init__(self) -> None:
        self.fingerprint = self.lock_fingerprint()

    def lock_fingerprint(self) -> dict:
        """fingerprint"""
        fingerprint = {}
        fingerprint["platform"] = platform.system()

        # fingerprint["cpu"] = platform.processor() # Ignoring CPU for now

        # Gathering GPU details for fingerprint

        gpu_details = self.get_gpu_details()
        fingerprint.update(gpu_details)

        return fingerprint

    def get_gpu_details(self) -> dict:
        """
        This method extracts the gpu information and returns a dictionary
        """

        gpus = GPUtil.getGPUs()

        if len(gpus) == 0:
            return ""

        elif len(gpus) == 1:
            for gpu in gpus:
                gpu_name = gpu.name
                gpu_driver_version = gpu.driver

                return {
                    "gpu": gpu_name,
                    "driver_version": gpu_driver_version
                }
        else:
            gpu_name = ""
            gpu_dict = {}
            index = 0
            # [RTX100, RTX3000, RTX5000]
            for gpu in gpus:
                gpu_dict[f"gpu{str(index)}"] = gpu.name
                index += 1

            gpu_dict["driver_version"] = gpus[0].driver
            return gpu_dict

    def lock_metadata(self, app, app_version) -> None:
        """
        Lock metadata locks the app-version as metadata for current json file.
        Args:
            app (str): Name of the Application
            app_version: Version of the application
        """
        self.metadata = {
            "app": app,
            "app_version": app_version
        }

    def append_metrics(
            self, 
            benchmark: str,
            metric_name: str, 
            metric_value,
            metric_unit: str = '',
            timestamp_value: bool = False
    ):
        """Method to append metrics
        """
        metric = {}
        if timestamp_value:
            metric[metric_name] = {
                "values": list(next(iter(metric_value.values()))),
                "unit": metric_unit,
                "timestamps": {
                    "values": list(metric_value["timestamp"]),
                    "unit": "ms"
                }
            }
        else:
            metric[metric_name] = {
                "value": metric_value,
                "unit": metric_unit
            }

        if benchmark not in self.benchmark.keys():
            self.benchmark[benchmark] = metric
        else:
            self.benchmark[benchmark].update(metric)

    def print_data_debug(self):
        """Print all data of Reggie.
        """
        print("Project: ", self.project)
        print("Benchmark: ", self.benchmark)
        print("Benchmark_suite: ", self.benchmark_suite)
        print("Fingerprint: ", self.fingerprint)
        print("Metadata: ", self.metadata)
        print("Metrics:", self.metrics)

    def update_benchmark_fields(
            self,
            project='',
            benchmark_suite=''):
        """Method to update the project, benchmark and benchmark_suite fields.
        """
        if project:
            self.project = project
        if benchmark_suite:
            self.benchmark_suite = benchmark_suite

    def dump_reggie_json(
            self,
            json_name='',
            json_dir=f"{os.getcwd()}/results/reggie"):
        """
        Method to Create a Reggie JSON file in desired location
        """
        if not os.path.exists(json_dir):  # Handling dir not exists condition
            os.makedirs(json_dir)

        for benchmark, metrics in self.benchmark.items():
            if not benchmark or not metrics:
                continue
            data = {
                "project": self.project,
                "benchmark_suite": self.benchmark_suite,
                "benchmark": benchmark,
                "fingerprint": self.fingerprint,
                "session_metadata": self.metadata,
                "samples": metrics
            }
            json_file_name = json_name + "_" + benchmark.lower().replace(' ', '_') + self.json_ext

            with open(os.path.join(json_dir, json_file_name), "w") as reggie_file:
                json.dump(data, reggie_file, indent=4)
