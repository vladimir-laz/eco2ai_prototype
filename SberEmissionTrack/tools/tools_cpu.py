from cpuinfo import get_cpu_info
import psutil
import time

# cpu benchmarks:
# https://www.notebookcheck.net/Mobile-Processors-Benchmark-List.2436.0.html?
# https://www.cpu-upgrade.com/CPUs/index.html

FROM_WATTs_TO_kWATTh = 1000*3600


class CPU():
    '''
    description will be written soon
    1) All methods are done on the assumption that all cpus are equal
    2) it takes time to calculate base percent usage, - 10 seconds
    '''
    def __init__(self, tdp=None, measure_period=0.5):
        self._cpu_dict = get_cpu_info()
        self._measure_period = measure_period
        self.name = self._cpu_dict["brand_raw"]

        if tdp is None:
            self.tdp = self._set_cpu_tdp()
        else:
            self.tdp = tdp
        # self._num_cpu = self._cpu_dict["count"]
        self._consumption = 0
        self._base_persent_usage = self._calculate_base_percent_usage()
        self._start = time.time()

    def set_consumption_zero(self):
        self._consumption = 0

    def get_consumption(self):
        self.calculate_consumption()
        return self._consumption

    def get_base_usage(self):
        return self._base_persent_usage

    def _set_cpu_tdp(self):
        # prints to user cpu model and expect from him(her) to input cpu tdp
        tdp = float(input(f"Name of your cpu: {self.name}.\nPlease, enter it's TDP: "))
        return tdp

    def _calculate_base_percent_usage(self):
        percents = []
        for _ in range(10): #calculating base percent usage for 10*measure_period sec
             percents.append(self.get_cpu_percent())
        return sum(percents) / 10

    def get_cpu_percent(self):
        percent = sum(psutil.cpu_percent(interval=self._measure_period, percpu=True))
        return percent

    def calculate_consumption(self):
        time_period = time.time() - self._start
        self._start = time.time()
        consumption = self.tdp * (self.get_cpu_percent() - self._base_persent_usage) / 100 * (time_period + self._measure_period) / FROM_WATTs_TO_kWATTh
        self._consumption += consumption
        return consumption

def all_available_cpu():
    try:
        cpu_dict = get_cpu_info()
        string = f"""Seeable cpu devices:
        {cpu_dict["brand_raw"]}: {cpu_dict["count"]} devices"""
        print(string)
    except:
        print("There is no any available cpu devices")