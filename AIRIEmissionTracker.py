import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tools import *

EMISSION_PER_KWT = 511.7942


class AIRITracker:
    """
    in order to right gpu power consumption calculation you'd better to create
    EmissionTracker before any gpu uses
    """
    def __init__(self,
                 project_name,
                 experiment_description,
                 save_file_name="emission.csv",
                 measure_period=None,
                 emission_level=EMISSION_PER_KWT,
                 base_power=None
                 ):
        self.project_name = project_name
        self.experiment_description = experiment_description
        self.save_file_name = save_file_name
        if measure_period <= 0:
            raise ValueError("measure_period should be positive number")
        self.measure_period = measure_period
        self.emission_level = emission_level
        self.base_power_consumption = base_power if base_power else gpu_power()
        self.start = None
        self._scheduler = BackgroundScheduler()
        self._consumption = 0

    def _write_to_csv(self):
        duration = self.stop - self.start
        emissions = self._consumption * duration
        if not os.path.is_file(self.save_file_name):
            with open(self.save_file_name, 'w') as file:
                file.write("project_name,experiment_description,time,power_consumption,CO2_emissions\n")
                file.write(f"{self.project_name},{self.experiment_description},{time},{self._consumption},{emissions}")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(f"{self.project_name},{self.experiment_description},{time},{self._consumption},{emissions}\n")

    def func_for_sched(self):
        current_powers = gpu_power()
        duration = time.time - self.start
        for base_power, current_power in zip(self.base_power_consumption, current_powers):
            self._consumption += (current_power - base_power) * duration
        
        print(self._consumption)

    def start(self):
        self.start = time.time()
        self.base_power_consumption = gpu_power()
        if self.measure_period is not None:
            self._scheduler.add_job(self.func_for_sched, "interval", seconds=self.measure_period)
            self._scheduler.start()

    def stop(self, ):
        if self.start is None:
            raise Exception("Need to first start the tracker by tracker.start()")
        self.func_for_sched()
        if self.measure_period is not None:
            self._scheduler.shutdown()
        self._write_to_csv()
        print(self._consumption)



print(time.time())
print(is_gpu_available())
