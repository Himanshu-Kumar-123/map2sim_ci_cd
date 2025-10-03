import subprocess
import json
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from fwk.shared.variables_util import varc

class VramRecorder():
    """This class is used to capture vram for each test"""
    
    #script ported with some modifications from https://gitlab-master.nvidia.com/autosimulator/drivesim-ov/-/blob/develop/tools/profiling/vram_recorder.py
    def __init__(self,filename,interval,title,test_dict):
        self.filename=filename
        self.interval=interval
        self.title=title
        self.gpu_dict = {}
        self.test_dict=test_dict
        #adding vram 24gb(24576) check
        self.threshold=24576
    
    def kit_exists(self):
        if "--ovc-run" in self.test_dict['automation_suite_flags_dict']:
            try:
                _, processes, _=varc.ssh.execute_command('pgrep -f -l "omni.drivesim.e2e|omni.drivesim.datastudio"')
                for process in processes:
                    if "kit" in process:
                        return True
            except:
                return False
        else:
            processes = subprocess.run(
                ['pgrep -f -l "omni.drivesim.e2e|omni.drivesim.datastudio"'], capture_output=True, shell=True
            )
            for process in processes.stdout.splitlines():
                if "kit" in process.decode():
                    return True
    
    def get_vram_usage(self):
        if "--ovc-run" in self.test_dict['automation_suite_flags_dict']:
            smi_cmd = "nvidia-smi --query-gpu=gpu_name,memory.used,pci.bus_id --format=csv,noheader"
            _, output, _=varc.ssh.execute_command(smi_cmd)
            report = output.read().splitlines()
        else:
            smi_cmd = "nvidia-smi --query-gpu=gpu_name,memory.used,pci.bus_id --format=csv,noheader"
            smi_cmd = smi_cmd.split()
            report = subprocess.run(smi_cmd, capture_output=True)
            report = report.stdout.splitlines()
        for gpu in report:
            gpu_data = gpu.decode().split(",")
            name = gpu_data[0]
            bus_id = gpu_data[2]
            vram, vram_units = gpu_data[1].split()
            unique_name = name + " " + bus_id
            if not unique_name in self.gpu_dict:
                self.gpu_dict[unique_name] = []
            self.gpu_dict[unique_name].append(int(vram))
            
        #threshold check
        peaked_gpu_info = []
        for gpu, vram_values in self.gpu_dict.items():
            max_vram = max(vram_values)
            if max_vram >= self.threshold:
                peaked_gpu_info.append(f'For {gpu}, vram peaked {math.ceil(max_vram/1000)} GB\n')
        if peaked_gpu_info:
            peaked_gpu_info.append("Please check vram_data directory of this testcase to know more on trends")
            peaked_gpu_info_str="".join(peaked_gpu_info)
            self.test_dict['subtest_dict']['vram-test']=peaked_gpu_info_str
                
    def save(self):
        with open(self.filename + ".json", "w") as json_file:
            json.dump(self.gpu_dict, json_file)

    def plot(self):
        num_entries = len(next(iter(self.gpu_dict.values())))
        endTime = num_entries * self.interval
        time = np.arange(0, endTime, self.interval)

        gpu_names = []
        maxMemory = 0
        for gpu_data in self.gpu_dict.items():
            name, memory = gpu_data
            if len(time) != len(memory):
                print("Incorrect number of GPU entries. Found " + str(len(memory)) + " but expected " + str(len(time)))

            maxMemory = max(math.ceil(max(memory) / 1000) * 1000, maxMemory)
            # The plt.scatter() method doesn’t start the plotting process visually. It just prepares the data to be displayed.
            plt.scatter(time, memory)
            gpu_names.append(name)
        # When plt.legend(gpu_names, fontsize="5") is called, it uses the list gpu_names to label the plotted scatter points in the order in which they were plotted.
        plt.legend(gpu_names,fontsize="5")
        plt.yticks(np.arange(0, maxMemory + 1000, 1000))
        plt.title(self.title)
        plt.xlabel("Time (s)")
        plt.ylabel("Memory (MB)")
        plt.grid()
        print(self.filename + ".png")
        plt.savefig(self.filename + ".png", dpi=300)
        plt.close()
    
    def run(self):
        print("[SDG_BATCH_RUNNER] : VRAMRecorder: Waiting for Kit process to start.")
        while not self.kit_exists():
            time.sleep(self.interval)
            
            #when kit process does not get started due to some issue in startup, process should not hang
            event_set = varc.analysis_event.wait(timeout=0)
            if event_set:
                print("Event received, releasing thread of vram recorder...")
                return

        print("[SDG_BATCH_RUNNER] : VRAMRecorder: Kit process detected, starting VRAM recording.")
        while self.kit_exists():
            self.get_vram_usage()
            time.sleep(self.interval)
            
        #no need of adding event here, as docker or kit process will be killed before test end
            
        print("[SDG_BATCH_RUNNER] : VRAMRecorder: Kit process finished, stopping VRAM recording.")

        print("VRAMRecorder: Saving data to json.")
        self.save()
        print("VRAMRecorder: Plotting data.")
        self.plot()