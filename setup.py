import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Alien Invasion",
      version="0.9",
      description="Space Invaders Clone",
      options={"build_exe": {"packages": ["pygame", "os"],
                             "excludes": ["tkinter", "numpy", "test", "distutils"],
                             "include_files": ["images/alien1a.bmp", "images/alien1b.bmp", "images/shipa.bmp",
                                               "sound_effects/explosion.wav", "sound_effects/game_over.wav",
                                               "sound_effects/game_start.wav", "sound_effects/laser.wav",
                                               "sound_effects/lose_life.wav"]}},
      executables=[Executable("alien_invasion.py", base=base)]
      )
