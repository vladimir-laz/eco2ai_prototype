# AIRIEmisisonTracker

## Installation
You should download files AIRIEmissionTrack.py and tools.py right in your directory.

Then, you can simply import these files

## Use example

```python

import AIRIEmissionTrack.AIRITracker

tracker = AIRITracker(project_name=your_project_name,
                      experiment_description=your_experiment_description,
                      save_file_name="you_file_name",
                      measure_period=2,   #measurement will be done every 2 seconds
                      emission_level=your_value   #kg/kWTh
                      base_power=your_gou_base_power   #power of not working gpu
                      )
tracker.start()

*your gpu calculations*

tracker.stop()
```
