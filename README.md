# SberEmisisonTracker

##  Installation
As this project is intensively updating, in order to utilize SberEmisisonTrack correctly it is recommended to run 
```bash
pip uninstall SberEmissionTrack -y
```
before the installation

Then, all you need to install the package is to run this command in your terminal:
```bash
pip install git+git://github.com/vladimir-laz/AIRIEmisisonTracker.git
```
In order to all dependencies to be set correctly you may need to restart your kernel after package installation
## Use example
SberEmiaaionTrack's interface is quite simple. Here is a the most straightforward usage example
```python

import SberEmissionTrack.Tracker

tracker = Tracker()
tracker.start()

*your gpu &(or) cpu calculations*

tracker.stop()
```

You can also explore the guide folder. There is [sber_emission_tracker_guide.ipynd](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - useful jupyter notebook with more complete examples. It is recommended to explore it before usage.

## Advices
In order to calculate gpu & cpu power consumption correctly you should create Tracker before any gpu or cpu usage

For every new calculation it should be created new tracker