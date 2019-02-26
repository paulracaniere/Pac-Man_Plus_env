# Pac-Man Plus (1982) Environment

## TL;DR

This repository contains Python scripts using the MAME emulator as well as the MAME RL Toolkit made by M-J-Murray. It's an environment to train a algorithm to beat Pac-Man Plus.

## Requirements

### MAME

First you need to download a binary for MAME that fits your Operating System.

### MAMEToolkit

This can be installed via `pip install MAMEToolkit`.

Although, I made a few modifications in the `Console.py` file. The program won't act correctly if it does not already know if the console will output something or not. I added these two lines after reading the output of the console:

```python
        if expect_output == None:
            return output
```

This allows to set the parameter `expect_output` to `None` whenever the output is non-mandatory.

### Pac-Man Plus ROM

For this environment to run, you need to have a folder containing the ROM of the Pac-Man Plus game. This can easily be found on the internet.

## Usage

An example script is provided in `example.py`.

This environment is meant to be close to the Open.AI Gym API.

The possible actions are from 0 to 4, accordingly to this function:

```python
def index_to_move_action(action):
    return {
        0: [Actions.P1_LEFT],
        1: [Actions.P1_UP],
        2: [Actions.P1_RIGHT],
        3: [Actions.P1_DOWN],
        4: []
    }[action]
```

The reward is computed as the difference between the actual score and the former one.