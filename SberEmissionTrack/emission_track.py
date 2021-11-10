import os
import time
import platform
from apscheduler.schedulers.background import BackgroundScheduler

from SberEmissionTrack.tools.tools_gpu import *
from SberEmissionTrack.tools.tools_cpu import *

EMISSION_PER_MWT = 511.7942
FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000


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
                 project_name="Deafult project name",
                 experiment_description="no experiment description",
                 save_file_name="emission.csv",
                 measure_period=2,
                 emission_level=EMISSION_PER_MWT,
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
        self._cpu = None
        self._gpu = None
        self._consumption = 0
        self._os = platform.system()
        if self._os == "Darwin":
            self._os = "MacOS"
        

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
                file.write("project_name,experiment_description,start_time(s),duration(s),power_consumption(kWTh),CO2_emissions(kg),CPU_name,GPU_name,OS\n")
                file.write(f"{self.project_name},{self.experiment_description},{self._start_time},{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(duration))},{self._consumption},{emissions},{self._cpu.name()},{self._gpu.name()},{self._os}\n")
        else:
            with open(self.save_file_name, "a") as file:
                file.write(f"{self.project_name},{self.experiment_description},{self._start_time},{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(duration))},{self._consumption},{emissions},{self._cpu.name()},{self._gpu.name()},{self._os}\n")

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
        # print("self._stop was run")
        self._scheduler.remove_job("job")
        self._scheduler.shutdown()
        self._func_for_sched() 
        self._write_to_csv()

def available_devices():
    '''
    Prints all available and seeable cpu & gpu devices and their number
    '''
    all_available_cpu()
    all_available_gpu()
    # need to add RAM
