# Connectors (Wires)

## Raspi <-> Feeder

5-pin wire:
```
_____-_____
|.1.2.345..|
```

Details:
```
1. brown wire: GND
2. red wire: +5VDC
3. orange wire: Servo control
4. yellow: LED +3.3VDC
5. green: unused
```

To be connected as follow:
```
Raspberry
____________________________________________...
| 2 4 6 8 ...
| 1 3 5 7 ...
.
.
```

Details:
```
1. +3.3VDC
2. +5VDC
3. GPIO BCM pin 2   <---- connect wire 4 yellow "LED control"
4. +5VDC            <---- connect wire 2 red
5. GPIO BCM pin 3   <---- connect wire 3 orange "Servo control"
6. GND              <---- connect wire 1 brown
```

## Raspi <-> Pumps

7-pin wire:
```
_____-_____
|1.2.3456.7|
```

Details:
```
1. black wire: GND
2. white wire: +5VDC
3. grey wire: Pump 1 Control
4. purple wire: Pump 2 Control
5. blue wire: Pump 3 Control
6. green wire: Pump 4 Control
7. yellow/red wire: LED
```

To be connected as follow:
```
Raspberry
____________________________________________...
| 2 ....................... 36 38 40 |
| 1 ....................... 35 37 39 |
.
.
```

Details:
```
1. +3.3VDC
2. +5VDC             <---- connect wire 2 white +5VDC
35. GPIO BCM pin 19  <---- connect wire 3 grey       "Pump 1 control"
36. GPIO BCM pin 16  <---- connect wire 4 purple     "Pump 2 control"
37. GPIO BCM pin 26  <---- connect wire 5 blue       "Pump 3 control"
38. GPIO BCM pin 20  <---- connect wire 6 green      "Pump 4 control"
39. GND              <---- connect wire 1 black GND
40. GPIO BCM pin 21  <---- connect wire 7 yellow/red "LED control"
```


## 12VDC <-> Pumps

2-pin wire:
```
_____-_____
|1.2.......|
```

Details:
```
1. wire: GND
2. wire: +12VDC
```