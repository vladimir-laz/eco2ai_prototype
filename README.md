# SberEmisisonTracker

##  Installation
As this project is intensively updating, in order to utilize SberEmisisonTracker correctly it is recommended to run 
```bash
pip uninstall SberEmissionTrack -y
```
before the instalation

Then, all you need to install the package is to run one command in your terminal:
```bash
pip install git+git://github.com/vladimir-laz/AIRIEmisisonTracker.git
```
In some keyses it is also may be needed to restart your kernel after installation
## Use example
For more complite instructions you can explore the guide folder. There is [sber_emission_tracker_guide.ipynd](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - very useful jupyter notebook with code and russian  comments. It is recommended to explore it.

```python

import SberEmissionTrack.Tracker

tracker = Tracker(project_name=your_project_name,
                      experiment_description=your_experiment_description,
                      save_file_name="you_file_name.csv",
                      measure_period=2,   #measurement will be done every 2 seconds
                      cpu_tdp=<you_cpu_tdp_value> 
                      )
tracker.start()

*your gpu & cpu calculations*

tracker.stop()
```

## Advices
In order to correctly calculate gpu power consumption you should create Tracker before any gpu or cpu uses as tracker considers background gpu and cpu power

For every new power calculation it should be created new tracker and taken some 20 sec break.