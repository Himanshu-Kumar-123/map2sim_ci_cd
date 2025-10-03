import re
import json
import math
import time
import threading
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import psutil

from fwk.shared.variables_util import varc
from cloudevents.http import CloudEvent
from kratos_pycloudevents.client import TelemetryClient

class DSRecorder:
    def __init__(self,filename,interval,title,plot,test_dict,upload=False):
        """
        Initializes the DSRecorder class
        
        Args:
            filename (str): Path to save the captured data in JSON format and png format(Graph plot)
            interval (int): Time interval between captures in seconds
            title (str): Title to be added in plot if user opted for it
            plot (bool): to plot a graph and save as png 
            test_dict (dict): A dictionary consisting of ATF test information
            upload (bool): To trigger upload logic
        """
        self.filename=filename
        self.interval=interval
        self.title=title
        self.test_dict=test_dict
        self.upload=upload
        self.plot=plot
        
        self.recording = False
        self.vram_recorder_thread = None
        self.process_memory_recorder_thread = None
        
        #below vars are for vram recording
        self.gpu_dict = {}
        self.threshold=24576 #adding vram 24gb(24576) check
        self.kratos_dict={}

        # For process memory tracking
        self.process_memory = []
        self.kit_pid = None

    def _get_vram_usage(self):
        """
        Gets the current VRAM usage using nvidia-smi
        """
        if "--ovc-run" in self.test_dict['automation_suite_flags_dict']:
            smi_cmd = "nvidia-smi --query-gpu=gpu_name,memory.used,pci.bus_id,memory.total,index --format=csv,noheader"
            _, output, _=varc.ssh.execute_command(smi_cmd)
            report = output.read().splitlines()
        else:
            smi_cmd = "nvidia-smi --query-gpu=gpu_name,memory.used,pci.bus_id,memory.total,index --format=csv,noheader"
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
            self.kratos_dict[f'total_vram_{gpu_data[4].strip()}']=int(gpu_data[3].split()[0])
            
        #threshold check
        peaked_gpu_info = []
        index=0
        vram_peak_usage = {}

        for gpu, vram_values in self.gpu_dict.items():
            max_vram = max(vram_values)
            self.kratos_dict[f'max_vram_{index}']=max_vram
            self.kratos_dict[f'gpu_{index}']=' '.join(gpu.split(' ')[:3])
            if max_vram >= self.threshold:
                peaked_gpu_info.append(f'For {gpu}, vram peaked {math.ceil(max_vram/1000)} GB\n')
            if "--perf-data-record" in self.test_dict['automation_flags_dict'] or "--perf-data-record" in self.test_dict['automation_suite_flags_dict']:
                vram_peak_usage[gpu] = math.ceil(max_vram/1000)
            index=index+1

        if peaked_gpu_info:
            peaked_gpu_info.append("Please check vram_data directory of this testcase to know more on trends")
            peaked_gpu_info_str="".join(peaked_gpu_info)
            self.test_dict['subtest_dict']['vram-test']=peaked_gpu_info_str

        if vram_peak_usage:
            if 'perf-test' in self.test_dict['subtest_dict']:
                self.test_dict['subtest_dict']['perf-test'].update({"vram-peak-usage-gb": vram_peak_usage})
            else:
                self.test_dict['subtest_dict']['perf-test'] = {"vram-peak-usage-gb": vram_peak_usage}

    def _get_process_memory(self):
        """
        Gets the current memory usage of the kit process
        """
        # Find kit process PID
        processes = subprocess.run(['pgrep', '-f', 'omni.drivesim.e2e|omni.drivesim.datastudio'], 
                                capture_output=True, text=True)
        for process in processes.stdout.splitlines():
            try:
                proc = psutil.Process(int(process))
                if "kit" in proc.cmdline()[0]:
                    self.kit_pid = proc.pid
                    break
            except (psutil.NoSuchProcess, IndexError):
                continue

        if self.kit_pid:
            try:
                process = psutil.Process(self.kit_pid)
                memory_info = process.memory_info()
                # Record RSS (Resident Set Size) in GB
                self.process_memory.append(round(memory_info.rss / 1024 / 1024 / 1024, 2))
                #print(f"Process Memory: {self.process_memory[-1]} GB") 
            except psutil.NoSuchProcess:
                print("Kit process no longer exists")
        
        if "--perf-data-record" in self.test_dict['automation_flags_dict'] or "--perf-data-record" in self.test_dict['automation_suite_flags_dict']:
            max_process_memory = max(self.process_memory)
            if 'perf-test' in self.test_dict['subtest_dict']:
                self.test_dict['subtest_dict']['perf-test'].update({"process-memory-peak-gb": max_process_memory})
            else:
                self.test_dict['subtest_dict']['perf-test'] = {"process-memory-peak-gb": max_process_memory}

    def _kit_exists(self):
        """
        Check if kit process exists
        """
        if "--ovc-run" in self.test_dict['automation_suite_flags_dict']:
            try:
                _, processes, _=varc.ssh.execute_command('pgrep -f -l "omni.drivesim.e2e|omni.drivesim.datastudio"')
                for process in processes:
                    if "kit" in process:
                        return True
            except:
                return False
        else:
            try:
                processes = subprocess.run(
                    ['pgrep -f -l "omni.drivesim.e2e|omni.drivesim.datastudio"'], capture_output=True, shell=True
                )
                for process in processes.stdout.splitlines():
                    if "kit" in process.decode():
                        return True
            except:
                return False
    
    def _pre_check(self):
        """
        Checking some conditions before starting record, for this tool it checks if kit process exists
        """
        print("[SDG_BATCH_RUNNER] : DSecorder: Waiting for Kit process to start")
        while not self._kit_exists():
            time.sleep(self.interval)
            
            #when kit process does not get started due to some issue in startup, process should not hang
            event_set = varc.analysis_event.wait(timeout=0)
            if event_set:
                print("Event received, releasing thread of vram recorder...")
                return False
        print("[SDG_BATCH_RUNNER] : DSecorder: Kit process detected, starting recording")
        return True
    
    def _record_vram(self):
        """
        Function that runs in a separate thread to continuously capture data - VRAM Usage
        """
        if not self._pre_check():
            return
        while self.recording and self._kit_exists():
            self._get_vram_usage()
            time.sleep(self.interval)
            #no need of adding event here, as docker or kit process will be killed before test end
            #adding event for docker develop mode of ui test development
            event_set = varc.analysis_event.wait(timeout=0)
            if event_set:
                print("Event received, releasing thread of vram recorder...")
                break
            
        # can be called seperately from outside the class if one does have method like _kit_exists, 
        # and an event can be added in recorder loop which can raised in stop to make it come out of it
        # or self.recording can be made false in stop to avoid going into event stuff
        self.stop('vram')
    
    def _record_process_memory(self):
        """
        Function that runs in a separate thread to continuously capture data - PROCESS MEMORY Usage
        """
        if not self._pre_check():
            return
        while self.recording and self._kit_exists():
            self._get_process_memory()
            time.sleep(self.interval)
            #no need of adding event here, as docker or kit process will be killed before test end
            #adding event for docker develop mode of ui test development
            event_set = varc.analysis_event.wait(timeout=0)
            if event_set:
                print("Event received, releasing thread of process memory recorder...")
                break
            
        # can be called seperately from outside the class if one does have method like _kit_exists, 
        # and an event can be added in recorder loop which can raised in stop to make it come out of it
        # or self.recording can be made false in stop to avoid going into event stuff
        self.stop('process_memory')
    
    def start(self):
        """
        Starts the recording in a parallel thread
        """
        if not self.recording:
            self.recording = True
            self.vram_recorder_thread = threading.Thread(target=self._record_vram)
            varc.thread_list.append(self.vram_recorder_thread)
            self.vram_recorder_thread.start()
            print("VRAM Recording started...")

            self.process_memory_recorder_thread = threading.Thread(target=self._record_process_memory)
            varc.thread_list.append(self.process_memory_recorder_thread)
            self.process_memory_recorder_thread.start()
            print("Process Memory Recording started...")
            
            #for any additional params which has different recording process, can start another thread here

    def _save_data(self,type):
        """
        Saves the captured data
        
        Args:
            type (str): For what data this function is called
        """
        
        if type=='vram':
            print("[SDG_BATCH_RUNNER] : DSecorder : Saving VRAM data")
            with open(self.filename + "_vram_data.json", "w") as json_file:
                json.dump(self.gpu_dict, json_file)
        
        if type=='process_memory':
            print("[SDG_BATCH_RUNNER] : DSecorder : Saving Process Memory data")
            with open(self.filename + "_process_memory.json", "w") as json_file:
                json.dump(self.process_memory, json_file)
        
    def _plot(self,type):
        """
        plots the captured data in a graph and saves it as png file
        
        Args:
            type (str): For what data this function is called
        """
        if type=='vram':
            print("[SDG_BATCH_RUNNER] : DSecorder : Plotting VRAM data")
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
    
    def _kratos_json_create(self,type):
        """
        creates json file which will be uploaded to kratos
        
        Args:
            type (str): For what data this function is called
        """
        
        if type=='vram':
            
            print("[SDG_BATCH_RUNNER] : DSecorder : Preparing VRAM data for kratos upload")
            
            #json for pushing data to kratos if user opts for it
            self.kratos_dict['gpu_count'] = varc.final_dict['System Details']['GPU Count']
            self.kratos_dict['driver_version'] = varc.final_dict['System Details']['Driver Version']
            self.kratos_dict['cuda_version'] = varc.final_dict['System Details']['Cuda Version']
            self.kratos_dict['platform'] = varc.final_dict['System Details']['Platform']
            self.kratos_dict['build'] =  varc.final_dict['Build']
            self.kratos_dict['server'] = varc.final_dict['Nucleus']
                
            def clean_string(test_name):
                frame_count = None      
                # Check and remove the prefix if it starts with 'test' followed by a number and '_'
                if test_name.startswith("test") and '_' in test_name:
                    test_name = test_name.split('_', 1)[1]  # Split at the first '_' and take the part after it
                # Check and remove the suffix if it ends with '_' followed by a number
                if '_' in test_name and test_name.split('_')[-1].isdigit():
                    parts = test_name.rsplit('_', 1)  # Remove the last part after the '_'
                    frame_count = parts[1] # Capture the suffix number
                    test_name = parts[0]  # Remove the suffix part
                return test_name,frame_count
                
            test_name,frame_count = clean_string(self.test_dict['name'])
            
            self.kratos_dict['test_name'] = test_name
            self.kratos_dict['frame_count'] = int(frame_count) if frame_count is not None else None
            
            if not "--docker-run" in varc.toml_dict['AUTOMATION_SUITE']['automation_suite_flags'] and not "--ovc-run" in varc.toml_dict['AUTOMATION_SUITE']['automation_suite_flags']:
                self.kratos_dict['test_env_type'] = "ci_cd"
                parts = self.kratos_dict['build'].split('_')
                if len(parts) == 2:
                    branch = parts[0]
                    commit_id = parts[1][:7]
                else:
                    branch, commit_id = None
                self.kratos_dict['dsBuildBranch'] = branch
                self.kratos_dict['dsDockerPermutation'] = None
                self.kratos_dict['dsBuildHash'] = commit_id  
            else:
                if "--docker-run" in varc.toml_dict['AUTOMATION_SUITE']['automation_suite_flags']:
                    self.kratos_dict['test_env_type'] = "local"
                elif "--ovc-run" in varc.toml_dict['AUTOMATION_SUITE']['automation_suite_flags']:
                    self.kratos_dict['test_env_type'] = "ovc"
                
                pattern = r"([a-f0-9]{7})(?=[a-f0-9]*$)"
                match = re.search(pattern, self.kratos_dict['build'])
                if match:
                    commit_id = match.group(1)
                else:
                    commit_id = None
                
                self.kratos_dict['dsBuildHash'] = commit_id
                
                branch_keywords = ["production", "staging", "develop"]
                for keyword in branch_keywords:
                    if keyword in self.kratos_dict['build']:
                        self.kratos_dict['dsBuildBranch'] = keyword
                        break
                    else:
                        self.kratos_dict['dsBuildBranch'] = None
                
                Permutation_keywords = ["minimal", "internal", "generic", "hyperion", "jlr", "mercedes", "internal-ovc"]
                for keyword in Permutation_keywords:
                    if keyword in self.kratos_dict['build']:
                        self.kratos_dict['dsDockerPermutation'] = keyword
                        break
                    else:
                        self.kratos_dict['dsDockerPermutation'] = None
            
            if self.test_dict['type']=='UI':
                self.kratos_dict['run_type'] = "e2e_ui"
            elif self.test_dict['type']=='HEADLESS':
                self.kratos_dict['run_type'] = "headless"
                     
            with open(self.filename + "_vram_kratos_data.json", "w") as json_file:
                json.dump(self.kratos_dict, json_file)
    
    def _upload_data(self,type):
        """
        Placeholder function for uploading the data
        User can specify the upload logic (e.g., upload to a server, cloud storage, etc.)
        
        Args:
            type (str): For what data this function is called
        """
        if type=='vram':
            print("[SDG_BATCH_RUNNER] : DSRecorder: Uploading VRAM data")

            self._kratos_json_create(type)            
            # Upload data to the Kratos telemetry collector endpoint
            telemetry_client = TelemetryClient(
                # Required Parameters
                ssaUrl="hvgfdxorrc6-em5mhrg7o3lr5skadstwarphmyuy4lg.ssa.nvidia.com",
                ssaClientId="nvssa-prd-D-ThEB4BECGzrTEa5S29rYpmgMG69bw9u7_1QjDa5i0",
                ssaClientSecret="ssap-qofRN3x8zhC3nOYFiNC",
                telemetryUrl="https://prod.analytics.nvidiagrid.net",
                # Optional Parameters
                telemetryConnectTimeout=5,
                telemetryReadTimeout=10,
            )

            attributes = {
                "type": "vram-perf-data",
                "source": "sdg-batch-runner",
                "schemaid": "omniverse-team.telemetry.ds-perf-recorder"
            }

            cloudevents = []
            cloudevent = CloudEvent(attributes=attributes, data=self.kratos_dict)
            cloudevents.append(cloudevent)

            response = telemetry_client.send(collectorId="omniverse-team.telemetry.ds-perf-recorder",
                                             cloudevents=cloudevents)
            
            if response.status_code == 200:
                print(f"[SDG_BATCH_RUNNER] : DSRecorder: VRAM data successfully uploaded to Kratos Telemetry")
            else:
                print(f"[SDG_BATCH_RUNNER] : DSRecorder:  Failed to upload VRAM data to Kratos Telemetry - {response.json()}")
                
            #save repsonse in a file
            with open(self.filename + "_vram_kratos_response.json", "w") as json_file:
                json.dump(response.json(), json_file)
    
    def stop(self,type):
        """
        Stops the recording, saves the data, and uploads if specified
        
        Args:
            type (str): For what data this function is called
        """
        print("[SDG_BATCH_RUNNER] : DSRecorder: Kit process finished, stopping recording")
        self.recording = False
        self._save_data(type)
        if self.plot:
            self._plot(type)
        if self.upload:
            self._upload_data(type)
        print("[SDG_BATCH_RUNNER] : DSRecorder: Recording stopped and data is saved and uploaded (if specified)")
        
        #if threads.join() is not available in tool, here it can be added and stop can be called from outside class