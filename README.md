# Electron Density Integration Tools

A suite of tools that read `.cub` files and integrate electron density data.

## reuseable.py

Contains several utility functions for parsing `.cub` files to extract information. Does nothing on its own.

#### Functions

`findAl(filename)` extracts the number of atoms, the positions of non-hydrogen atoms (aluminum in this case), and supercell dimension information. It returns a tuple with this information.

`parseFile(filename)` extracts electron density data and hydrogen position in addition to all that `findAl()` does. It returns a tuple with this information.

`distanceFromProton(point)` calculates the distance between the hydrogen projectile and an arbitrary point in space, assuming periodic boundary conditions. It requires the output from `parseFile()` to exist as global variables - see the spherical routine in `integrate.py` for a usage example.

## integrate.py

Can be used to integrate data spherically around a hydrogen projectile or linearly across the entire supercell. Outputs a `.csv` file in the same directory as the input file. Requires `reusable.py` in the same directory to function.

### Spherical Integration

Usage: `$ python integrate.py -s [-r x] filename`

#### Options

`-s, --spherical` indicates that spherical integration around a hydrogen projectile is requested.

`-r x, --radius x` indicates that a maximum radius of _x_ Bohr radii is requested, where x is an integer. If this option is not used, then a default of half the width of the supercell is used.

### Linear Integration

Usage: `$ python integrate.py -l -z[xy] filename`

#### Options

`-l, --linear` indicates that linear integration across the whole supercell is requested.

`-z[xy]` indicates which direction is requested. Exactly 1 argument is required.

### Help

Usage: `$ python integrate.py -h`

`-h, --help` displays information about each flag.

## shadowfinder.py

Integrates a thin sheet through the hydrogen projectile in the x-z plane. Outputs a `.csv` file in the same directory as the input file. Requires `reusable.py` in the same directory to function.