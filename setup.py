from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

DEPENDENCIES = [
    "APScheduler",
    "pynvml>=5.6.2",
    "psutil",
    "py-cpuinfo",
]

setup(
    name = 'SberEmissionTrack',
    version = '1.0.0',
    author="Vladimir Lazarev",
    # py_modules=['SberEmissionTrack',
    #             'tools_gpu'],
    url = 'https://github.com/vladimir-laz/AIRIEmisisonTracker.git',
    description = long_description,
    packages = find_packages(),
    install_requires=DEPENDENCIES,
    # package_data={
    #     "SberEmissionTrack": [
    #         "data/cpu_names.csv"
    #     ]
    # }
)