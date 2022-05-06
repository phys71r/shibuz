# Reacher Sim
Simulation and Reinforcement Learning for Reacher Robot

## System setup
### Operating system requirements
* Mac
* Linux
* Windows (untested, not recommended)

### Mac-only setup
Install xcode command line tools.
```bash
xcode-select --install
```
If you already have the tools installed you'll get an error saying so, which you can ignore.

### Conda setup
Install [miniconda](https://docs.conda.io/en/latest/miniconda.html), then
```
conda create --name reacher python=3.8
conda activate reacher
pip install ray arspb
```

## Getting the code ready
```bash
git clone https://github.com/stanfordroboticsclub/reacher-lab.git
cd reacher-lab
pip install -e .
```

## Running simulation on computer
```bash
python reacher/reacher_manual_control.py
```
You should see the PyBullet GUI pop up and see Reacher doing an exercise.

## Deploying to robot
### Upload reacher lab firmware to Teensy
1. Open vscode and upload your lab 1 / 2 code. The Teensy application should open in the background.

2. Click the open hex file button in the application window (left side) and choose the `firmware.hex` THAT'S IN THIS FOLDER (not from the lab 1/2 code).

3. Click the green auto button if it's not already highlighted

4. Press the button on the Teensy to program it with the hex file

### Run simulator and robot simultaneously
Run the python code:
```bash
python3 reacher/reacher_manual_control.py --run_on_robot
```
<br/>
