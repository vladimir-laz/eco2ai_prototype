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
    name = 'SberEmissionTracker',
    version = '0.1.0',
    url = 'https://github.com/vladimir-laz/AIRIEmisisonTracker.git',
    description = long_description,
    packages = find_packages(),
    install_requires=DEPENDENCIES,
    # install_requires = [
    #     # Github Private Repository
    #     'ExampleRepo @ git+ssh://git@github.com/example_organization/ExampleRepo.git#egg=ExampleRepo-0.1'
    # ]
)