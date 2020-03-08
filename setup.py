import cx_Freeze
executables = [cx_Freeze.Executable("alien_invasion.py")]
cx_Freeze.setup(
    name="Alien Invasion",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["images/alien1a.bmp", "images/alien1b.bmp", "images/shipa.bmp",
                                             "sound_effects/explosion.wav", "sound_effects/game_over.wav",
                                             "sound_effects/game_start.wav", "sound_effects/laser.wav",
                                             "sound_effects/lose_life.wav"]}},
    executables=executables
)
