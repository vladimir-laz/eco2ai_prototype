import pynvml
import time

FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000


class GPU():
    '''
    This class is interface for tracking gpu consumption.
    All methods are done here on the assumption that all gpu devices are of equal model.
    The GPU class is not intended for separate usage
    '''
    def __init__(self,):
        self._consumption = 0
        self.is_gpu_available = is_gpu_available()
        if self.is_gpu_available:
            self._start = time.time()            
    
    def set_consumption_zero(self):
        self._consumption = 0
    
    def calculate_consumption(self):
        if not self.is_gpu_available:
            return 0
        duration = time.time() - self._start
        self._start = time.time()
        consumption = 0
        for current_power in self.gpu_power():
            consumption += current_power / FROM_mWATTS_TO_kWATTH * duration
        if consumption < 0:
            consumption = 0
        self._consumption += consumption
        return consumption
    
    def get_consumption(self):
        if not self.is_gpu_available:
            return 0
        return self._consumption
    
    def gpu_memory(self):
        if not self.is_gpu_available:
            return None
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_memory = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("memory:", pynvml.nvmlDeviceGetMemoryInfo(handle))
            gpus_memory.append(pynvml.nvmlDeviceGetMemoryInfo(handle))
        pynvml.nvmlShutdown()
        return gpus_memory

    def gpu_temperature(self):
        if not self.is_gpu_available:
            return None
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_temps = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("temperature:", pynvml.nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU))
            gpus_temps.append(pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU))
        pynvml.nvmlShutdown()
        return gpus_temps

    def gpu_power(self):
        if not self.is_gpu_available:
            return None
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_powers = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("power:", pynvml.nvmlDeviceGetPowerUsage(handle))
            gpus_powers.append(pynvml.nvmlDeviceGetPowerUsage(handle))
        pynvml.nvmlShutdown()
        return gpus_powers

    def gpu_power_limit(self):
        if not self.is_gpu_available:
            return None
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_limits = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("power limit:", pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
            gpus_limits.append(pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
        pynvml.nvmlShutdown()
        return gpus_limits
    
    def name(self,):
        try:
            pynvml.nvmlInit()
            deviceCount = pynvml.nvmlDeviceGetCount()
            gpus_name = []
            for i in range(deviceCount):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                gpus_name.append(pynvml.nvmlDeviceGetName(handle))
            pynvml.nvmlShutdown()
            return gpus_name[0].decode("UTF-8")
        except:
            return "no available GPU device"

def is_gpu_available():
    '''
    Returns True if the GPU details are available.
    '''
    try:
        pynvml.nvmlInit()
        return True
    except pynvml.NVMLError:
        return False

def all_available_gpu():
    '''
    Prints all seeable gpu devices
    All the devices should be of the same model
    '''
    try:
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_name = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("names:", pynvml.nvmlDeviceGetName(handle))
            gpus_name.append(pynvml.nvmlDeviceGetName(handle))
        string = f"""Seeable gpu device(s):
        {gpus_name[0].decode("UTF-8")}: {deviceCount} device(s)"""
        print(string)
        pynvml.nvmlShutdown()
    except:
        print("There is no any available gpu device(s)")