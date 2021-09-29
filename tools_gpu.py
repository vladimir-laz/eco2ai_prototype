import pynvml

class NoAvailableGpuDevicesError(Exception):
    def __init__(self, message):
        self.message = message


class GPU():
    def __init__(self):
        self._gpu_available() = self.is_gpu_evailable()

    def is_gpu_available(self):
        """Returns True if the GPU details are available."""
        try:
            pynvml.nvmlInit()
            return True
        except pynvml.NVMLError:
            return False
    
    def gpu_memory(self):
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
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_limits = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("power limit:", pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
            gpus_limits.append(pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
        pynvml.nvmlShutdown()
        return gpus_limits

def all_available_gpu():
    '''
    This function are done on the assumption that all qpus devices are the same model
    '''
    try:
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        gpus_name = []
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            # print("names:", pynvml.nvmlDeviceGetName(handle))
            gpus_name.append(pynvml.nvmlDeviceGetName(handle))
        string = f"""Seeable qpu devices:
        {gpus_name[0].decode("UTF-8")}: {deviceCount} devices"""
        print(string)
        pynvml.nvmlShutdown()
    except:
        raise NoAvailableGpuDevicesError("There is no any available gpu devices!")

all_available_gpu()