import pynvml


def is_gpu_available():
    """Returns True if the GPU details are available."""
    try:
        pynvml.nvmlInit()
        return True
    except pynvml.NVMLError:
        return False

def gpu_memory():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    gpus_memory = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        # print("memory:", pynvml.nvmlDeviceGetMemoryInfo(handle))
        gpus_memory.append(pynvml.nvmlDeviceGetMemoryInfo(handle))
    pynvml.nvmlShutdown()
    return gpus_memory

def gpu_temperature():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    gpus_temps = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        # print("memory:", pynvml.nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU))
        gpus_temps.append(pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU))
    pynvml.nvmlShutdown()
    return gpus_temps

def gpu_power():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    gpus_powers = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        # print("memory:", pynvml.nvmlDeviceGetPowerUsage(handle))
        gpus_powers.append(pynvml.nvmlDeviceGetPowerUsage(handle))
    pynvml.nvmlShutdown()
    return gpus_powers

def gpu_power_limit():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    gpus_limits = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        # print("memory:", pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
        gpus_limits.append(pynvml.nvmlDeviceGetEnforcedPowerLimit(handle))
    pynvml.nvmlShutdown()
    return gpus_limits