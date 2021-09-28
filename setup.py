from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

DEPENDENCIES = [
    "APScheduler",
    "pynvml",
    "psutil",
    "py-cpuinfo",
]

setup(
    name = 'SberEmissionTrack',
    version = '0.1.0',
    author="Vladimir Lazarev",
    py_modules=['SberEmissionTrack'],
    # url = 'https://github.com/vladimir-laz/AIRIEmisisonTracker.git',
    description = long_description,
    packages = find_packages(),
    install_requires=DEPENDENCIES,
)