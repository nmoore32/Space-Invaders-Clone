A space invaders clone that I began by following the tutorial in Python Crash Course by Eric Matthes. 

Press E, N, or H to select difficulty setting and start the game.
Press Q to quit.
Press the left/right arrows to move.
Press space to fire.

As soon as I finished the tutorial I heavily refactored the code. The initial AlienInvasion class pretty much did everthing --- checking for events, checking for collisions, firing bullets, creating the alien fleet...). I moved a lot of the responsibilites from AlienInvasion to other classes (it ended up being half the size it initially was. I created the following classes during my refactoring.

- AlienFleet
- CollisionHandler
- EventHandler
- ProjectileHandler
- Display


Aside from the refactoring I also added a number of things to complete the game.

- Scaling based on user screen size
- My own pixel art aliens and ship
- Fixed an issue in the tutorial where the top row of aliens was partly obscured by the scoring information
- Aliens now fire back at you
- Added projectile class that the alien and ship projectiles could inherit
- Difficulty settings (determing the maximum number of alien bullets on screen)
- Can press E, N, or H to select difficulty/start the game
- Sound effects
- Start screen complete with blinking "Press Any Key to Start" message
- Game over message
- Demo game play (simple ai plays the game if left on the start screen for 30 seconds)
- Capped framerate at 30 FPS

In the process of making these changes I added the following classes

- Explosion
- Projectile
- AlienBullet
- ShipBullet (this one was just me renaming the bullet class and adjusting for the new projectile parent class)
- Demo
