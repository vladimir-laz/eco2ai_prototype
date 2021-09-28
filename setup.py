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
    # py_modules=['SberEmissionTrack'],
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    # url = 'https://github.com/vladimir-laz/AIRIEmisisonTracker.git',
    description = long_description,
    packages = find_packages(),
    install_requires=DEPENDENCIES,
)