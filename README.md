A space invaders clone that I began by following the tutorial in Python Crash Course by Eric Matthes. 


Controls

Press E, N, or H to select difficulty setting and start the game.
Press Q to quit.
Press the left/right arrows to move.
Press space to fire.


Starting the game:

To start the game you'd run "python alien_invasion.py"


Building an executable:

To build an executable you need to download cx_Freeze "python -m pip install cx_Freeze --upgrade"
Then run "python setup.py build"

Two issues with cx_Freexe.

(i) It's not always good at finding game assets, which is why I specified where to find each one. But cx_Freeze will put them all in the same directory as the executable. You'll have to create folders in the directory with the executable called "images" and "sound_effects" and move the images and sound files, respectively, to those folders. This is because the executable will look for the game assets in those subfolders.

(ii) It's also not very good at determining what modules from the python standard library are needed. When creating the executable you'll a "lib" folder that contains a lot of unnecessary modules. You can exclude modules in setup.py (I've excluded some of the larger unneccessary modules that cx_Freeze was initially including).


Non-Windows systems:

If you're not using a windows system, then you may need to comment out line 19 of screen.py.
The line that reads "ctypes.windll.user32.SetProcessDPIAware()"



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
- Added, and then removed, background music (I think background music can sometimes be distracting and I just didn't like it here)
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
