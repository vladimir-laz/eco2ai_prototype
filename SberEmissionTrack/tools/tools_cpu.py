from cpuinfo import get_cpu_info
import psutil

# cpu benchmarks:
# https://www.notebookcheck.net/Mobile-Processors-Benchmark-List.2436.0.html?
# https://www.cpu-upgrade.com/CPUs/index.html

class CPU():
    '''
    description will be written soon
    '''
    def __init__(self, tdp=None):
        self._cpu_dict = get_cpu_info()
        self.name = self._cpu_dict["brand_raw"]

        if type(tdp) is not int and type(tdp) is not float:
            raise Exception("tdp parameter must be int or float number")

        if tdp is None:
            self.tdp = self.get_cpu_tdp()
        else:
            self.tdp = tdp
        self.num_cpu = self._cpu_dict["count"]
        self.consumption = 0
        self.base_persent_usage = self.calculate_base_percent_usage()

    def get_cpu_tdp():
        # prints to user cpu model and expect from him(her) to input cpu tdp
        
        pass

    def calculate_base_percent_usage():
        pass

    def get_cpu_percent(self):
        pass

    def get_consumption(self):
        pass


