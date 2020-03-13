# Movement_Simulation

A demonstration of various movement patterns. Originally started as an attempt at ![Boids](https://en.wikipedia.org/wiki/Boids), is an artificial life program, developed by Craig Reynolds in 1986, which simulates the flocking behaviour of birds.

> As with most artificial life simulations, Boids is an example of emergent behavior; that is, the complexity of Boids arises     from the interaction of individual agents (the boids, in this case) adhering to a set of simple rules. The rules applied in the simplest Boids world are as follows:

    Separation: steer to avoid crowding local flockmates
    Alignment: steer towards the average heading of local flockmates
    Cohesion: steer to move towards the average position (center of mass) of local flockmates
    
This is a work in progress. The plan is to add more complex movement patterns in the future.
### Demo:
![Movement AI Demo](resources/demo.gif)

### Requirements:

You must install Python and the Pygame module to run this simulaton.
Install Pygame with the following command:

    pip install pygame
    
Execute World.py to start

### Current Movements:

##### Idle: 
Creature will idle and do nothing

##### Wander: 
Creatures will wander in random directions while also avoiding collision

##### Boid Flocking: 
Simulation of the flocking behaviour of birds. 
    
##### Targeted Movement: 
Creatures will move towards a target (place with T). Creatures will flash gold and emit an aura upon reaching target (I think it looks cool!).
   
##### Stealth: Creatures 
Will hide behind obstacles from Predators (WIP)
    
### Controls:

    1: Set behaviour to Idle    
    2: Set behaviour to Wander    
    3: Set behaviour to Boid Flocking
    4: Set behaviour to Targeted Movement
    5: Set behaviour to Stealth
    
    S: Spawn a pair of creatures
    P: Spawn a predator (WIP)
    T: Place target
    Z: Reset simulation
    
    Keypad 1-4,6-9: Spawn a wall
    Keypad 5: Spawn a pillar
    O: Remove all walls
    
    SPACE: Pause simulation
