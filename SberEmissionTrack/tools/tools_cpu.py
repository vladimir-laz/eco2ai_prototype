from cpuinfo import get_cpu_info
import psutil
import time
import re
import os
import pandas as pd
import numpy as np
import warnings
import platform
from pkg_resources import resource_stream


CONSTANT_CONSUMPTION = 100.1
FROM_WATTs_TO_kWATTh = 1000*3600
NUM_CALCULATION = 200
CPU_TABLE_NAME = resource_stream('SberEmissionTrack', 'data/cpu_names.csv').name

class NoCPUinTableWarning(Warning):
    pass

class NoNeededLibrary(Warning):
    pass

class CPU():
    '''
    This class is interface for tracking cpu consumption.
    All methods are done here on the assumption that all cpu devices are of equal model.
    The CPU class is not intended for separate usage
    '''
    def __init__(self, measure_period=0.5):
        self._cpu_dict = get_cpu_info()
        self._measure_period = measure_period
        self._name = self._cpu_dict["brand_raw"]
        self._tdp = find_tdp_value(self._name, CPU_TABLE_NAME)
        self._consumption = 0
        self._cpu_num = number_of_cpu()
        self._start = time.time()

    def tdp(self):
        return self._tdp

    def set_consumption_zero(self):
        self._consumption = 0

    def get_consumption(self):
        self.calculate_consumption()
        return self._consumption

    def get_cpu_percent(self):
        tmp_array = psutil.cpu_percent(interval=self._measure_period, percpu=True)
        percent = sum(tmp_array) / len(tmp_array)
        return percent

    def calculate_consumption(self):
        time_period = time.time() - self._start
        self._start = time.time()
        consumption = self._tdp * self.get_cpu_percent() / 100 * self._cpu_num * time_period / FROM_WATTs_TO_kWATTh
        if consumption < 0:
            consumption = 0
        self._consumption += consumption
        return consumption

    def name(self,):
        return self._name

    def cpu_num(self,):
        return self._cpu_num

def all_available_cpu():
    '''
    Prints all seeable cpu devices
    All the devices should be of the same model
    '''
    try:
        cpu_dict = get_cpu_info()
        string = f"""Seeable cpu device(s):
        {cpu_dict["brand_raw"]}: {number_of_cpu()} device(s)"""
        print(string)
    except:
        print("There is no any available cpu device(s)")


def number_of_cpu():
    '''
    Returns number of cpu sockets(physical cpu processors)
    If the body the function runs with error, it will return 1, which means there is only one cpu device
    '''
    operating_system = platform.system()
    result = None
    if operating_system == "Darwin":
        operating_system = "MacOS"

    if operating_system == "Linux":
        try:
            # returns cpu sockets number
            # running terminal command, getting output
            string = os.popen("lscpu")
            output = string.read()
            output
            # dictionary creation
            dictionary = dict()
            for i in output.split('\n'):
                tmp = i.split(':')
                if len(tmp) == 2:
                    dictionary[tmp[0]] = tmp[1]
            result = min(int(dictionary["Socket(s)"]), int(dictionary["NUMA node(s)"]))
        except:
            warnings.warn(message="\nYou probably should have installed 'util-linux' to deretmine cpu number correctly\n\n", 
                          category=NoNeededLibrary)
            result = 1
    else: 
        result = 1
    return result


def transform_cpu_name(f_string):
    '''
    Drops all the waste tokens, patterns and words from a cpu name
    '''
    # dropping all the waste tokens and patterns:
    f_string = re.sub('(\(R\))|(®)|(™)|(\(TM\))|(@.*)|(\S*GHz\S*)|(\[.*\])|( \d-Core)|(\(.*\))', '', f_string)

    # dropping all the waste words:
    array = re.split(" ", f_string)
    for i in array[::-1]:
        if ("CPU" in i) or ("Processor" in i) or (i == ''):
            array.remove(i)
    f_string = " ".join(array)
    patterns = re.findall("(\S*\d+\S*)", f_string)
    return f_string, patterns


def find_max_tdp(elements):
    '''
    Takes cpu names as input
    Returns cpu with maximum TDP value
    '''
    # finds and returns element with maximum TDP
    if len(elements) == 1:
        return float(elements[0][1])

    max_value = 0
    for index in range(len(elements)):
        if float(elements[index][1]) > max_value:
            max_value = float(elements[index][1])
    return max_value

def get_patterns(cpu_name):
    return re.findall("(\S*\d+\S*)", cpu_name)

# searching cpu name in cpu table
def find_tdp_value(f_string, f_table_name=CPU_TABLE_NAME, constant_value=CONSTANT_CONSUMPTION):
    # firstly, we try to find transformed cpu name in the cpu table:
    f_table = pd.read_csv(f_table_name)
    f_string, patterns = transform_cpu_name(f_string)
    f_table = f_table[["Model", "TDP"]].values
    suitable_elements = f_table[f_table[:, 0] == f_string]

    if suitable_elements.shape[0] > 0:
        # print("suitable elements: ", suitable_elements)
        # print("element is found in the table!")  # OK
        # if there are more than one suitable elements, return one with maximum TDP value
        return find_max_tdp(suitable_elements)
    # secondly, if needed element isn't found in the table,
    # then we try to find patterns in cpu names and return suitable values:
    # if there is no any patterns in cpu name, we simply return constant consumption value
    if len(patterns) == 0:
        warnings.warn(message="\n\nYour CPU device is not found in our database\nCPU TDP is set to constant value 100\n", 
                      category=NoCPUinTableWarning)
        return constant_value

    # appending to array all suitable for at least one of the patterns elements
    suitable_elements = []
    for element in f_table:
        flag = False
        for pattern in patterns:
            if pattern in get_patterns(element[0]):
                flag = True
        if flag:
            suitable_elements.append(element)

    # if there is only one suitable element, we return this element.
    # If there is no suitable elements, we return constant value
    # If there are more than one element, we check existence of elements suitable for all the patterns simultaneously.
    # If there are such elements(one or more), we return the value with maximum TDP among them.
    # If there is no, we return the value with maximum TDP among all the suitable elements
    if len(suitable_elements) == 0:
        warnings.warn(message="\n\nYour CPU device is not found in our database\nCPU TDP is set to constant value 100\n", 
                      category=NoCPUinTableWarning)
        return CONSTANT_CONSUMPTION
    elif len(suitable_elements) == 1:
        return suitable_elements[0][1]
    else:
        tmp_elements = []
        for element in suitable_elements:
            flag = 1
            for pattern in patterns:
                if pattern not in element[0]:
                    flag *= 0
            if flag == 1:
                tmp_elements.append(element)
        if len(tmp_elements) != 0:
            return find_max_tdp(tmp_elements)
        else:
            return find_max_tdp(suitable_elements)