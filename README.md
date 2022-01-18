# SberEmisisonTracker
 
## Requirements

You should have installed git on your computer or server.
If you are running your code in Linux, you will need to get util-linux installed to woork correctly(usually, it is installed by default)


##  Installation
As this project is still under development, in order to utilize SberEmisisonTrack correctly please run 
```bash
pip uninstall SberEmissionTrack -y
```
before the installation

Next step to install the package is to run the following command in your terminal:
```bash
pip install --user git+git://github.com/vladimir-laz/SberEmissionTrack.git
```
In order to all dependencies to be set correctly you may need to restart your kernel after package installation
## Use examples
SberEmissionTrack's interface is quite simple. Here is a the most straightforward usage example:
```python

import SberEmissionTrack

tracker = SberEmissionTrack.Tracker(project_name="YourProjectName", experiment_description="training the <your model> model")

tracker.start()

<your gpu &(or) cpu calculations>

tracker.stop()
```

SberEmissionTrack also supports decorators. Once decorated function executed, emissions info will be written to the file. See example below:
```python
from SberEmissionTrack import track

@track
def train_func(model, dataset, optimizer, epochs):
    ...

train_func(your_model, your_dataset, your_optimizer, your_epochs)
```


For your convenience every time you initilize a Tracker object with your custom parameters, this settings will be saved until library is uninstalled, and then every new tracker will be created with your custom settings(if you will create new tracker with new parameters, then they will be saved instead of old ones). For example:

```python

import SberEmissionTrack

tracker = SberEmissionTrack.Tracker(
    project_name="YourProjectName", 
    experiment_description="training <your model> model",
    file_name="emission.csv"
    )

tracker.start()
<your gpu &(or) cpu calculations>
tracker.stop()

...

# now, we want to create a new tracker for new calculations
tracker = SberEmissionTrack.Tracker()
# it's equivelent to:
# tracker = SberEmissionTrack.Tracker(
#     project_name="YourProjectName", 
#     experiment_description="training the <your model> model",
#     file_name="emission.csv"
# )
tracker.start()
<your gpu &(or) cpu calculations>
tracker.stop()

```

You can also set parameters using set_params() function, like in the example below:

```python
from SberEmissionTrack import set_params, Tracker

set_params(
    project_name="My_default_project_name",
    experiment_description="We trained...",
    file_name="my_emission_file.csv"
)

tracker = Tracker()
# now, it's equivelent to:
# tracker = Tracker(
#     project_name="My_default_project_name",
#     experiment_description="We trained...",
#     file_name="my_emission_file.csv"
# )
tracker.start()
<your code>
tracker.stop()
```



<!-- There is [sber_emission_tracker_guide.ipynb](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - useful jupyter notebook with more examples and notes. We highly recommend to check it out beforehand. -->
## Important note
In order to calculate gpu & cpu power consumption correctly you should create the 'Tracker' before any gpu or cpu usage

For every new calculation create a new “Tracker.”

# Feedback
If you had some problems while working with our tracker, please, give us a feedback comments in [document](https://docs.google.com/spreadsheets/d/1927TwoFaW7R_IFC6-4xKG_sjlPUaYCX9vLqzrOsASB4/edit#gid=0)
