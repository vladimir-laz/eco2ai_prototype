import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tools_gpu import *

EMISSION_PER_KWT = 511.7942
FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000


class Tracker:
    """
    In order to correctly calculate gpu power consumption you should create
    Tracker before any gpu and cpu uses as tracker considers background gpu and cpu power

    For every new gpu calculation it should be created new tracker

    ----------------------------------------------------------------------
    Use example:

    import SberEmissionTrack.Tracker
    tracker = Tracker(project_name=your_project_name,
                      experiment_description=your_experiment_description,
                      save_file_name="you_file_name",
                      measure_period=2,   #measurement will be done every 2 seconds
                      emission_level=your_value   #kg/MWTh
                      base_power=your_gpu_base_power   #power of not working gpu
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
                 measure_period=None,
                 emission_level=EMISSION_PER_KWT,
                 base_power=None
                 ):
                #  добавить проверку на наличие видимых гпу
        self.project_name = project_name
        self.experiment_description = experiment_description
        self.save_file_name = save_file_name
        if (type(measure_period) == int or type(measure_period) == int) and measure_period <= 0:
            raise ValueError("measure_period should be positive number")
        self.measure_period = measure_period
        self.emission_level = emission_level
        self.base_power_consumption = base_power if base_power else gpu_power()
        self.start_time = None
        self._scheduler = BackgroundScheduler()
        self._consumption = 0

    def _write_to_csv(self):
        duration = time.time() - self.start_time
        emissions = self._consumption * duration / FROM_kWATTH_TO_MWATTH
        if not os.path.isfile(self.save_file_name):
            with open(self.save_file_name, 'w') as file:
                file.write("project_name,experiment_description,time(s),power_consumption(kWTh),CO2_emissions(kg)\n")
                file.write(f"{self.project_name},{self.experiment_description},{duration},{self._consumption},{emissions}\n")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(f"{self.project_name},{self.experiment_description},{duration},{self._consumption},{emissions}\n")

    def _func_for_sched(self):
        current_powers = gpu_power()
        # print(self.start_time, time.time())
        duration = time.time() - self.start_time
        for base_power, current_power in zip(self.base_power_consumption, current_powers):
            self._consumption += (current_power - base_power) / FROM_mWATTS_TO_kWATTH * duration
        
        # print("self._func_for_sched's consumption = ", self._consumption)

    def start(self):
        self.start_time = time.time()
        if self.measure_period is not None:
            # print("scheduler was activated")
            self._scheduler.add_job(self._func_for_sched, "interval", seconds=self.measure_period)
            self._scheduler.start()

    def stop(self, ):
        if self.start_time is None:
            raise Exception("Need to first start the tracker by tracker.start()")
        # print("self._stop was run")
        self._func_for_sched()
        if self.measure_period is not None:
            self._scheduler.shutdown()
        self._write_to_csv()


