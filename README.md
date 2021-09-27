# AIRIEmisisonTracker

## Requirements
It needs to be installed pynvml and apscheduler libraries.
```bash
pip install pynvml
pip install apscheduler
```
Also it is need to have library tzlocal with version >= 2.0(usually, it is installed with apscheduler library)

## Utilization
Download files SberEmissionTrack.py and tools.py right in your directory.

Then, simply import these files(see use example)


## Use example

```python

import SberEmissionTrack.Tracker

tracker = Tracker(project_name=your_project_name,
                      experiment_description=your_experiment_description,
                      save_file_name="you_file_name",
                      measure_period=2,   #measurement will be done every 2 seconds
                      emission_level=your_value   #kg/MWTh
                      base_power=your_gpu_base_power   #power of not working gpu
                      )
tracker.start()

*your gpu calculations*

tracker.stop()
```

## Advices
In order to correctly calculate gpu power consumption you should create Tracker before any gpu or cpu uses as tracker considers background gpu and cpu power

For every new gpu calculation it should be created new tracker