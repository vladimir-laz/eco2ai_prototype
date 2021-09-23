import os
import time
from tools import *

EMISSION_PER_KWT = 511.7942


class AIRITracker():
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
        self.measure_period = measure_period
        self.emission_level = emission_level
        self.base_power_consumption = base_power if base_power else gpu_power()
        self.start = None
        self.stop = None

    def _write_to_csv(self, power_consumption, duration):
        emissions = power_consumption * duration
        if not os.path.is_file(self.save_file_name):
            with open(self.save_file_name, 'w') as file:
                file.write("project_name,experiment_description,time,power_consumption,CO2_emissions\n")
                file.write(
                    f"{self.project_name},{self.experiment_description},{time},{power_consumption},{emissions}\n")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(
                    f"{self.project_name},{self.experiment_description},{time},{power_consumption},{emissions}\n")

    def _none_period_start(self):
        self.start = time.time()
        self.base_power_consumption = gpu_power()

    def _none_period_stop(self):
        if self.start is None:
            raise Exception("Need to first start the tracker by tracker.start()")
        self.stop = time.time()
        power_consumption = 0
        current_powers = gpu_power()
        duration = self.stop - self.start
        for base_power, current_power in zip(self.base_power_consumption, current_powers):
            power_consumption += (current_power - base_power) * (duration)

        self._write_to_csv(power_consumption, duration)
        return power_consumption

    def start(self, ):
        if self.measure_period is None:
            return self._none_period_start()
        else:
            raise Exception("code is not finished")

    def stop(self, ):
        if self.measure_period is None:
            return self._none_period_stop()
        else:
            raise Exception("code is not finished")



# print(time.time())
# print(is_gpu_available())
