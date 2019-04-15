# Movement_AI

Demonstration of various Movement AI

Current Movements:

Idle: Creature will idle and do nothing

Wander: Creatures will wander in random directions while also avoiding collision

Boid Flocking: Simulation of flocking behaviour based on the artificial life program developed by Craig Reynolds. A demonstration of Emergent behaviour that follows a set of three rules:
    
    Separation: steer to avoid crowding local flockmates
    Alignment: steer towards the average heading of local flockmates
    Cohesion: steer to move towards the average position (center of mass) of local flockmates
    
Controls:

    1: Set behaviour to Idle    
    2: Set behaviour to Wander    
    3: Set behaviour to Boid Flocking
    
    S: Spawn a pair of creatures
    P: Spawn a predator (WIP)
    Keypad 1-9: Spawn a wall
    O: Remove all walls
    Z: Reset simulation
    
    SPACE: Pause simulation