### *WardrobeGarden*

Plant environment control system on RasberryPi.
GpioController, Gardener, and a GardenApp.

**Gpio controller** controls GPIO pins on RPi

**Gardener** does the environment control based on
plant and lifeline id

**GardenApp** is the usable REST server for clients

#### *Endpoints of GardenApp*

/garden - all plant
/garden/{plant_id} - specific plant config
/garden/{plant_id}/lifelines - lifelines of specific plant

/control/start  - to post id of lifeline to start

/control/stop - to post id of lifeline to stop