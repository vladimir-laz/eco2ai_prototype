from cpuinfo import get_cpu_info
import psutil

# cpu benchmarks:
# https://www.notebookcheck.net/Mobile-Processors-Benchmark-List.2436.0.html?
# https://www.cpu-upgrade.com/CPUs/index.html

class CPU():
    '''
    description will be written soon
    1) All methods are done on the assumption that all cpus are equal
    2) it takes time to calculate base percent usage, - 10 seconds
    '''
    def __init__(self, tdp=None):
        self._cpu_dict = get_cpu_info()
        self.name = self._cpu_dict["brand_raw"]

        if tdp is None:
            self.tdp = self._get_cpu_tdp()
        else:
            self.tdp = tdp
        if type(self.tdp) is not int and type(self.tdp) is not float:
            raise Exception("tdp parameter must be int or float number")
        self.num_cpu = self._cpu_dict["count"]
        self.consumption = 0
        self.base_persent_usage = self._calculate_base_percent_usage()

    def _get_cpu_tdp(self):
        # prints to user cpu model and expect from him(her) to input cpu tdp
        tdp = input(f"Name os your cpu is: {self.name}.\nPlease, enter it's TDP: ")
        return tdp

    def _calculate_base_percent_usage(self):
        percents = []
        for _ in range(20): #calculating base percent usage for 10 sec
             percents.append(self.get_cpu_percent())
        return sum(percents) / 20
        

    def get_cpu_percent(self):
        percent = sum(psutil.cpu_percent(interval=0.5, percpu=True))
        return percent

    def get_consumption(self):
        consumption = self.tdp * (self.get_cpu_percent - self.base_persent_usage) / 100
        self.consumption += consumption
        return consumption

def all_available_gpu():
    cpu_dict = get_cpu_info()
    string = f"""Seeable devices cpu devices:
    {cpu_dict["brand_war"]}: {cpu_dict["count"]} devices"""
    print(string)

