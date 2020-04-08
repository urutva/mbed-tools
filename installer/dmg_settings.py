from pathlib import Path

home = str(Path.home())

# The list of files to package
files = ['./dist/mbed-tools']

# Locations where this installation should go
symlinks = {'UsrLocal': '/usr/local',
            'Home': home}

# Background image
background = 'builtin-arrow'

# Where to put the icons
icon_locations = {
    'mbed-tools':   (140, 120),
    'Home': (500, 120)
    }
