from setuptools import setup, find_packages

setup(
    name = 'SberEmissionTracker',
    version = '0.1.0',
    url = 'https://github.com/vladimir-laz/AIRIEmisisonTracker.git',
    description = 'Tracks emission of CO2',
    packages = find_packages(),
    # install_requires = [
    #     # Github Private Repository
    #     'ExampleRepo @ git+ssh://git@github.com/example_organization/ExampleRepo.git#egg=ExampleRepo-0.1'
    # ]
)