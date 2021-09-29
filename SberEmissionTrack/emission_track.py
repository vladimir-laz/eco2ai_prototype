import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

from SberEmissionTrack.tools.tools_gpu import *
from SberEmissionTrack.tools.tools_cpu import *

EMISSION_PER_MWT = 511.7942
FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000


class Tracker:
    """
    In order to correctly calculate gpu or cpu ppower consumption you should create
    Tracker before any gpu and cpu uses as tracker considers background gpu and cpu power

    For every new gpu calculation it should be created new tracker

    ----------------------------------------------------------------------
    Use example:

    import SberEmissionTrack.Tracker
    tracker = Tracker(project_name=your_project_name,
                      experiment_description=your_experiment_description,
                      save_file_name="you_file_name",
                      measure_period=2,   #measurement will be done every 2 seconds
                      )
    tracker.start()
    *your gpu calculations*
    tracker.stop()

    ----------------------------------------------------------------------
    """
    def __init__(self,
                 project_name,
                 experiment_description,
                 save_file_name="emission.csv",
                 measure_period=2,
                 emission_level=EMISSION_PER_MWT,
                 cpu_tdp=None
                 ):
                #  добавить проверку на наличие видимых гпу
        self.project_name = project_name
        self.experiment_description = experiment_description
        self.save_file_name = save_file_name
        if (type(measure_period) == int or type(measure_period) == float) and measure_period <= 0:
            raise ValueError("measure_period should be positive number")
        self._measure_period = measure_period
        self._emission_level = emission_level
        self._scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
        self._start_time = None
        self._cpu_tdp = cpu_tdp
        self._cpu = None
        self._gpu = None
        self._consumption = 0

    def consumption(self):
        return self._consumption
    
    def emission_level(self):
        return self._emission_level
    
    def measure_period(self):
        return self._measure_period

    def _write_to_csv(self):
        duration = time.time() - self._start_time
        emissions = self._consumption * self._emission_level / FROM_kWATTH_TO_MWATTH
        if not os.path.isfile(self.save_file_name):
            with open(self.save_file_name, 'w') as file:
                file.write("project_name,experiment_description,time(s),power_consumption(kWTh),CO2_emissions(kg)\n")
                file.write(f"{self.project_name},{self.experiment_description},{duration},{self._consumption},{emissions}\n")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(f"{self.project_name},{self.experiment_description},{duration},{self._consumption},{emissions}\n")

    def _func_for_sched(self):
        # print(self.start_time, time.time())
        duration = time.time() - self._start_time
        cpu_consumption = self._cpu.calculate_consumption()
        if self._gpu.is_gpu_available:
            gpu_consumption = self._gpu.calculate_consumption()
        else:
            gpu_consumption = 0
        self._consumption += cpu_consumption
        self._consumption += gpu_consumption
        # print("self._func_for_sched's consumption = ", self._consumption)

    def start(self):
        # print("scheduler was activated")
        # print(self._cpu_tdp, self._measure_period)
        self._cpu = CPU(self._cpu_tdp, self._measure_period)
        self._gpu = GPU()
        self._start_time = time.time()
        self._scheduler.add_job(self._func_for_sched, "interval", seconds=self._measure_period)
        self._scheduler.start()

    def stop(self, ):
        if self._start_time is None:
            raise Exception("Need to first start the tracker by running tracker.start()")
        # print("self._stop was run")
        self._scheduler.shutdown()
        self._func_for_sched() 
        self._write_to_csv()

def available_devices():
    '''
    prints all available and seeable devices and their powers
    '''
    print("changes added")
    all_available_cpu()
    all_available_gpu()
    # need to add RAM
