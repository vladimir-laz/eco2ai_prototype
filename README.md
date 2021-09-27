# AIRIEmisisonTracker

## Installation
Download files SberEmissionTrack.py and tools.py right in your directory.

Then, simply import these files(see use example)

## Requirements
It needs to be installed pynvml and apscheduler libraries

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
