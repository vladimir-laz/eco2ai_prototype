import os
import time
import platform
import pandas as pd
import requests
import numpy as np
from re import sub
from pkg_resources import resource_stream
from apscheduler.schedulers.background import BackgroundScheduler

from SberEmissionTrack.tools.tools_gpu import *
from SberEmissionTrack.tools.tools_cpu import *

EMISSION_PER_MWT = 511.7942
FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000
# JSON_FILE_NAME = resource_stream('SberEmissionTrack', 'config.json').name
# with open(JSON_FILE_NAME, 'w') as file:
#     pass

# PROJECT_NAME = "Deafult project name"
# EXPERIMENT_DESCRIPTION = "no experiment description"
# FILE_NAME = "emission.csv"

class Tracker:
    """
    This class calculates CO2 emissions during cpu or gpu calculations 
    In order to calculate gpu & cpu power consumption correctly you should create the 'Tracker' before any gpu or cpu usage
    For every new calculation create a new “Tracker.”

    ----------------------------------------------------------------------
    Use example:

    import SberEmissionTrack.Tracker
    tracker = SberEmissionTrack.Tracker()

    tracker.start()

    *your gpu calculations*
    
    tracker.stop()
    ----------------------------------------------------------------------
    """
    def __init__(self,
                 project_name=PROJECT_NAME,
                 experiment_description=EXPERIMENT_DESCRIPTION,
                 save_file_name=FILE_NAME,
                 measure_period=10,
                 emission_level=EMISSION_PER_MWT,
                 ):
        print(PROJECT_NAME, EXPERIMENT_DESCRIPTION, FILE_NAME)
        self.project_name = project_name
        self.experiment_description = experiment_description
        self.save_file_name = save_file_name
        if (type(measure_period) == int or type(measure_period) == float) and measure_period <= 0:
            raise ValueError("measure_period should be positive number")
        self._measure_period = measure_period
        self._emission_level = emission_level
        self._scheduler = BackgroundScheduler(job_defaults={'max_instances': 4}, misfire_grace_time=None)
        self._start_time = None
        self._cpu = None
        self._gpu = None
        self._consumption = 0
        self._os = platform.system()
        if self._os == "Darwin":
            self._os = "MacOS"
        self._country = self.define_country()
        # self._mode == "first_time" means that CO2 emissions is written to .csv file first time
        # self._mode == "runtime" means that CO2 emissions is written to file periodically during runtime 
        self._mode = "first_time"
        

    def consumption(self):
        return self._consumption
    
    def emission_level(self):
        return self._emission_level
    
    def measure_period(self):
        return self._measure_period

    def _write_to_csv(self):
        # if user used older versions, it may be needed to upgrade his .csv file
        # but after all, such verification should be deleted
        self.check_for_older_versions()
        duration = time.time() - self._start_time
        emissions = self._consumption * self._emission_level / FROM_kWATTH_TO_MWATTH
        if not os.path.isfile(self.save_file_name):
            with open(self.save_file_name, 'w') as file:
                file.write("project_name,experiment_description,start_time,duration(s),power_consumption(kWTh),CO2_emissions(kg),CPU_name,GPU_name,OS,country\n")
                file.write(f"{self.project_name},{self.experiment_description},{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._start_time))},{duration},{self._consumption},{emissions},{self._cpu.name()},{self._gpu.name()},{self._os},{self._country}\n")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(f"{self.project_name},{self.experiment_description},{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._start_time))},{duration},{self._consumption},{emissions},{self._cpu.name()},{self._gpu.name()},{self._os},{self._country}\n")
        if self._mode == "runtime":
            self._merge_CO2_emissions()
        self._mode = "runtime"

    # merges 2 CO2 emissions calculations together
    def _merge_CO2_emissions(self,):
        dataframe = pd.read_csv(self.save_file_name)
        columns, values = dataframe.columns, dataframe.values
        row = values[-2]
        row[3:6] += values[-1][3:6]
        values = np.concatenate((values[:-2], row.reshape(1, -1)))
        pd.DataFrame(values, columns=columns).to_csv(self.save_file_name, index=False)


    # but after all, such verification should be deleted
    def check_for_older_versions(self,):
        # upgrades older emission.csv file up to new one
        if os.path.isfile(self.save_file_name):
            dataframe = pd.read_csv(self.save_file_name)
            columns = "project_name,experiment_description,start_time,duration(s),power_consumption(kWTh),CO2_emissions(kg),CPU_name,GPU_name,OS,country".split(',')
            if list(dataframe.columns.values) != columns:
                dataframe = dataframe.assign(**{"CPU_name":"no cpu name", "GPU_name": "no gpu name","OS": "no os name", "country": "no country", "start_time": "no start time"})
                dataframe = pd.concat(
                    [
                    dataframe[["project_name", "experiment_description"]],
                    dataframe[["start_time"]],
                    dataframe[['time(s)', 
                                'power_consumption(kWTh)', 
                                'CO2_emissions(kg)',
                                'CPU_name',
                                'GPU_name',
                                'OS',
                                'country']],
                    ],
                    axis=1
                    )
                dataframe.columns = columns
                dataframe.to_csv(self.save_file_name, index=False)


    def _func_for_sched(self):
        cpu_consumption = self._cpu.calculate_consumption()
        if self._gpu.is_gpu_available:
            gpu_consumption = self._gpu.calculate_consumption()
        else:
            gpu_consumption = 0
        self._consumption += cpu_consumption
        self._consumption += gpu_consumption
        self._write_to_csv()
        self._start_time = time.time()

    def start(self):
        self._cpu = CPU()
        self._gpu = GPU()
        self._start_time = time.time()
        self._scheduler.add_job(self._func_for_sched, "interval", seconds=self._measure_period, id="job")
        self._scheduler.start()
        print(self._cpu.name())
        print(self._gpu.name())

    def stop(self, ):
        if self._start_time is None:
            raise Exception("Need to first start the tracker by running tracker.start()")
        self._scheduler.remove_job("job")
        self._scheduler.shutdown()
        self._func_for_sched() 
        self._write_to_csv()

    def define_country(self,):
        region = sub(",", '',eval(requests.get("https://ipinfo.io/").content.decode('ascii'))['region'])
        country = sub(",", '',eval(requests.get("https://ipinfo.io/").content.decode('ascii'))['country'])
        return f"{region}/{country}"

# def from_json(json_file=JSON_FILE_NAME):
#     with open(JSON_FILE_NAME, 'r') as json_file:
#         pass
#     pass

def available_devices():
    '''
    Prints all available and seeable cpu & gpu devices and their number
    '''
    all_available_cpu()
    all_available_gpu()
    # need to add RAM


