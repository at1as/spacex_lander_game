# SpaceX Lander Game
Land the Falcon v9.1 first stage on sea droneship without tipping over, missing the target, or landing too hard.

![screenshot](https://github.com/at1as/at1as.github.io/blob/master/github_repo_assets/rocket_lander.jpg)

## Installation

```bash
$ git clone https://github.com/at1as/spacex_lander_game
$ sudo pip install hg+http://bitbucket.org/pygame/pygame
$ python launch_game.py
```

Note that PyGame installation will vary depending on your OS

## Controls

'A' or Left Arrow:
* Steer Left

'D' or Right Arrow:
* Steer Right

'W' or Up Arrow:
* Trottle

## Constraints
* Limited Fuel
* Drone ship sways on the water from left to right
* Wind is constant throughout descent, but varies with direction and intensity during each round
* Start position and angle of rocket varies between rounds
* Must land with rocket angle of less than -10 to 10 degrees
* Must land with rate of descent of 5 or less
