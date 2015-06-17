# Electron Density Integration Tools

A suite of tools that read `.cub` files and integrates electron density data.

## Python/reuseable.py

Contains several utility functions for parsing `.cub` files to extract information. Does nothing on its own.

#### Functions

`findAl(filename)` extracts the number of atoms, the positions of non-hydrogen atoms (aluminum in this case), and supercell dimension information. It returns a tuple with this information.

`parseFile(filename)` extracts electron density data and hydrogen position in addition to all that `findAl()` does. It returns a tuple with this information.

`distanceBetween(a, b)` calculates the distance between two arbitrary points in space, assuming periodic boundary conditions. Each point must be expressed as a list of floats with a length of 3. It requires the output from `parseFile()` to exist as global variables - see the spherical routine in `integrate.py` for a usage example.

## Python/integrate.py

Can be used to integrate data spherically around a hydrogen projectile or linearly across the entire supercell in a `.cub` file. Outputs a `.csv` file in the same directory as the input file. **Requires** `reusable.py` in the same directory to function.

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

## Python/combine.py

Combines the output of multiple `integrate.py` runs of the same simulation at different timesteps into a single `.csv` file. **Must be edited** to change the `rootFolder` variable on line 6 to the location of the folder containing the `.csv` files to be combined.

Output is written to standard out, so it can be piped into a file.

Usage: `$ python combine.py > output.csv`

## Python/seegrapher.py

Reads the output of `combine.py` and outputs plots that graph the electron density distribution at different timesteps.

**Requires** the `matplotlib` and `numpy` modules to be installed.

Usage: `$ python seegrapher.py filename`

## Python/shadowfinder.py

Integrates a thin sheet through the hydrogen projectile in the x-z plane in a `.cub` file. Outputs a `.csv` file in the same directory as the input file. **Requires** `reusable.py` in the same directory to function.

Usage: `$ python shadowfinder.py filename`

## Python/shadowgrapher.py

Reads the output of `shadowgrapher.py` and outputs a contour map of the log10 of electron density through that slice.

**Requires** the `matplotlib` and `numpy` modules to be installed.

Usage: `$ python shadowgrapher.py filename`

# Convenience Scripts

## Bash/makepbs.sh

Makes batch files to be run with `qsub`. Creates a file for each `.cub` file in the directory `DIR`. Currently set to run linear integration; edit line 10 to change this.

**Must be edited** to change the `DIR` variable on lines 3 and 10 to the correct directory path.

## Bash/runpbs.sh

Runs each `.pbs` file found in the `DIR` directory. Allows manual inspection of one or more `.pbs` files before they are enqueued.

**Must be edited** to change the `DIR` variable on line 3 to the correct directory path.