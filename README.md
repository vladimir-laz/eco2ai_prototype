# SberEmisisonTracker

##  Installation
As this project is still under development, in order to utilize SberEmisisonTrack correctly please run 
```bash
pip uninstall SberEmissionTrack -y
```
before the installation

Next step to install the package is to run the following command in your terminal:
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

There is [sber_emission_tracker_guide.ipynd](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - useful jupyter notebook with more examples and notes. We highly recommend to check it out beforehand.
## Important note
In order to calculate gpu & cpu power consumption correctly you should create the 'Tracker' before any gpu or cpu usage

For every new calculation create a new “Tracker.”