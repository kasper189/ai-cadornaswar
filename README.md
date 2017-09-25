## AI-CADORNASWAR

### The Goal
Control more planets than your opponent at the end of the game.

### Rules

The game is played on a graph of interconnected planets. Both players attempt to control as many planets as possible by placing units in orbit. If a player has more units around a planet than the opponent, the planet is transformed into a star of that player's color and is considered under their control.

Each player starts out with a few units affected to a planet on opposite sides of the graph.

### Units
Every turn:
You must affect 5 units to planets you can reach. You can reach planets you already have at least one unit on and the neighbors of planets you control.
You may choose to sacrifice 5 units from a planet you control in order to spawn 1 unit on each of that planet's neighbors, regardless of the amount of neighbors. This is called unit spread.
You may choose to sacrifice 5 units from any planet in order to spawn 1 unit on each of that planet's neighbors, regardless of the amount of neighbors. This is called unit spread.
Planet tolerance
However, your warp technology is rather limited:
Each planet has a tolerance value for each player of 5.
Every turn in which you affect units to a planet, that planet's tolerance value is decreased by 1.
You may not affect units to a planet for which your tolerance value is 0.
Tolerance is not affected by unit spread, neither when the planet is losing nor gaining units.

### Turns
At any point in a turn, if you have more units than your opponent affected to a planet, you gain control of that planet.
One game turn is computed in this order:
* Both players affect their units.
* Unit spread occurs.
* Any planet with more neighbors controlled by the opponent than by you will lose 1 of your units.

### Victory Conditions
You control more planets than your opponent at the end of the game.
You control all planets at the end of a turn.

### Lose Conditions
You provide invalid input
You have no units left in play.

### Expert Rules

The game ends after N turns where N is the number of planets in the graph.
Before the game begins, both players are considered to have already assigned 5 units to their starting planet. The starting planet's tolerance for you is thus only 4.
You must output 5 planet ids every turn, even when you have less than 5 valid planets left. Invalid planets will simply be ignored.
### Note

To make debugging easier you can:
Toggle HD mode and Debug mode in the viewer settings
See a planet's tolerances by hovering over it with the mouse, or by counting the bars in its attached boxes.
Set the IDE in Expert Mode in order to manually set the game parameters from the Options tab
Add these keys to the game parameters extra_0_units and extra_1_units followed by a list of space-separated planet indices to change the initial state of the game
Use your left & right keys when the viewer has focus to follow the game one turn at a time.

### Game Input

Initialization input
First line: 2 integers: planetCount for the number of planets in the graph, and edgeCount an integer for the number of links between planets.

Next edgeCount lines: 2 integers planetAand planetB indicating the existence of an link between the two planets. Planets are numbered from 0 to planetCount - 1.

Input for one game turn
Next planetCount lines: 5 integers per line:

myUnits: amount of units you have assigned to this planet.
myTolerance: tolerance value this planet has for you.
otherUnits: amount of units your opponent has assigned to this planet.
otherTolerance: tolerance value this planet has for your opponent.
canAssign: 1 if this is a valid target for assigning units this turn, 0 otherwise.
A valid target has myTolerance > 0 and (myUnits > 0 or neighbor to a planet you control).
Output for one game turn
5 first lines each containing a single integer, the index of the planet to assign a unit to.

On extra line containing the index of the planet to spread your units from, or the keyword NONE to not cause unit spread.

### Constraints
* 16 ≤ planetCount ≤ 90
* 10 ≤ edgeCount ≤ 200
* Response time on the first turn ≤ 1000ms
* Response time per turn ≤ 50ms