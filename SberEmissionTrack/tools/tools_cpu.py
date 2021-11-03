from cpuinfo import get_cpu_info
import psutil
import time
import re
import os
import pandas as pd
import numpy as np

# cpu benchmarks:
# https://www.notebookcheck.net/Mobile-Processors-Benchmark-List.2436.0.html?
# https://www.cpu-upgrade.com/CPUs/index.html

# parsing tables from wikipedia:
# https://www.youtube.com/watch?v=ICXR9nDbudk&t=52s

CONSTANT_CONSUMPTION = 100
FROM_WATTs_TO_kWATTh = 1000*3600
NUM_CALCULATION = 200

class CPU():
    '''
    This class is interface for tracking cpu consumption.
    All methods are done here on the assumption that all cpus devices are equal.

    When class object is initialized it takes about 10 seconds to measure mean power consumption.

    It is recommended to wait about 20 seconds beetwen different calculations 
    in order to current cpu power consumption dropped to base(background) consumption level
    '''
    def __init__(self, measure_period=0.5):
        self._cpu_dict = get_cpu_info()
        self._measure_period = measure_period
        self._name = self._cpu_dict["brand_raw"]
        print(os.getcwd())
        self._tdp = find_tdp_value(self._name, "data/cpu_names.csv")
        print(self._name)
        print(self._tdp)
        self._consumption = 0
        # self._base_persent_usage = self._calculate_base_percent_usage()
        self._start = time.time()


    def set_consumption_zero(self):
        self._consumption = 0

    def get_consumption(self):
        self.calculate_consumption()
        return self._consumption

    def get_cpu_percent(self):
        percent = sum(psutil.cpu_percent(interval=self._measure_period, percpu=True))
        return percent

    def calculate_consumption(self):
        time_period = time.time() - self._start
        self._start = time.time()
        consumption = self._tdp * (self.get_cpu_percent() - self._base_persent_usage) / 100 * (time_period + self._measure_period) / FROM_WATTs_TO_kWATTh
        if consumption < 0:
            consumption = 0
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


# string = "Intel(R) Xeon(R) Platinum 8168 CPU @ 2.70GHz."
# string = "Intel® Xeon® Platinum 8170M Processor"
# string = "Intel Xeon W3530"
# string = "Intel® Core™ i5-9400T Processor"
# string = "Intel Xeon MP 3.33"
# string = "Intel Core 2 Quad Q6400[10]"
# string = "Intel Pentium 1405 v2"


def transform_cpu_name(f_string):
    # dropping all waste characters:
    # print(f"string before transformation:\n-----{f_string}----")
    f_string = re.sub('(\(R\))|(®)|(™)|(\(TM\))|(@.*)|(\S*GHz\S*)|(\[.*\])', '', f_string)
    # print(f'after dropping waste characters\n----{f_string}----')
    # print(re.findall("(\S*GHz\S*)", string))

    # dropping all waste words:
    array = re.split(" ", f_string)
    # print(f"split string:\n----{array}----")
    for i in array[::-1]:
        # print(i)
        if ("CPU" in i) or ("Processor" in i) or (i == ''):
            array.remove(i)
    # array.remove("@")
    f_string = " ".join(array)
    # print(f"string after transformation:\n----{f_string}----")
    patterns = re.findall("(\S*\d+\S*)", f_string)
    # print("all finded paterns:\n", patterns)
    return f_string, patterns


def find_max_tdp(elements):
    # finds and returns element with maximum TDP
    if len(elements) == 1:
        return float(elements[0][1])

    max_element_number = 0
    max_value = 0
    for index, element in enumerate(elements):
        if float(element[1]) > max_value:
            max_value = float(element[1])
            max_element_number = index
    return max_value


# searching cpu name in cpu table
def find_tdp_value(f_string, f_table_name="data/cpu_names.csv", constant_value=CONSTANT_CONSUMPTION):
    # firstly, we try to find transformed cpu name in cpu table:
    f_table = pd.read_csv(f_table_name)
    f_string, patterns = transform_cpu_name(f_string)
    # print(f_table.shape)
    f_table = f_table[["Model", "TDP"]].values
    suitable_elements = f_table[f_table[:, 0] == f_string].reshape(-1)
    # print(suitable_elements)
    if suitable_elements.shape[0] > 0:
        # print("element is found in the table!")  # OK
        return float(suitable_elements[1])
    # secondly, if needed element isn't found in the table,
    # then we try to find patterns in cpu names and return suitable values:

    # if there is no any patterns in cpu name, we simply return constant consumption value
    if len(patterns) == 0:
        return constant_value

    # appending to array all suitable for at least one of the patterns elements
    suitable_elements = []
    for element in f_table:
        flag = False
        for pattern in patterns:
            if pattern in element[0]:
                flag = True
        if flag:
            suitable_elements.append(element)

    # if there is only one suitable element, we return this element.
    # If there is no suitable elements, we return constant value
    # If there are more than one element, we check existence of elements suitable for all the patterns simultaneously.
    # If there are such elements(one or more), we return the value with maximum TDP among them.
    # If there is no, we return the value with maximum TDP among all the suitable elements
    if len(suitable_elements) == 0:
        # print("return constant consumption")  # OK
        return CONSTANT_CONSUMPTION
    elif len(suitable_elements) == 1:
        # print("there is only one suitable element")  # OK
        return suitable_elements[0][1]
    else:
        # print(f"It is found {len(suitable_elements)} suitable for patterns")   # OK
        tmp_elements = []
        for element in suitable_elements:
            flag = 1
            for pattern in patterns:
                if pattern not in element[0]:
                    flag *= 0
            if flag == 1:
                tmp_elements.append(element)
        if len(tmp_elements) != 0:
            # print(f"It is found {len(tmp_elements)} element(s) suitable for all patterns")  # OK
            return find_max_tdp(tmp_elements)
        else:
            # print(len(suitable_elements))
            # print(f"find element with maximum TDP among all the suitable element")  # OK
            return find_max_tdp(suitable_elements)