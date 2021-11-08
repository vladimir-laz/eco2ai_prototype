# SberEmisisonTracker

##  Installation
As this project is intensively updating, in order to utilize SberEmisisonTracker correctly it is recommended to run 
```bash
pip uninstall SberEmissionTrack -y
```
before the installation

Then, all you need to install the package is to run this command in your terminal:
```bash
pip install git+git://github.com/vladimir-laz/AIRIEmisisonTracker.git
```
In order to all dependencies were set you may need to restart your kernel after package installation
## Use example
SberEmiaaionTrack's interface is quite simple. Here is a the most straightforward usage example
```python

import SberEmissionTrack.Tracker

tracker = Tracker()
tracker.start()

*your gpu &(or) cpu calculations*

tracker.stop()
```

For more complete instructions you can explore the guide folder. There is [sber_emission_tracker_guide.ipynd](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - useful jupyter notebook with code and russian comments. It is recommended to explore it.

## Advices
In order to correctly calculate gpu power consumption you should create Tracker before any gpu or cpu uses

For every new power calculation it should be created new tracker