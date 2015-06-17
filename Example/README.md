## Example

`$ python gen_sphere_cub.py`

This will generate a set of sample `.cub` files with a single aluminum atom, a single hydrogen atom, and qualitative electron density distributions. This may take some time to generate and will use about 120MB of disk space when finished.

_If you load these files into VisIt, open them as the `Cube` file type. Ensure that the `default open options` are changed so that `ExtendVolumeByOneCell` is deselected._

Run [`Python/integrate.py`](Python#integratepy) on each `.cub` file in both spherical and linear-z modes. For example, assuming you are in the Example directory,

```bash
$ python ../Python/integrate.py -s density0000.cub;
$ python ../Python/integrate.py -lz density0000.cub;
```

Then edit line 6 of [`Python/combine.py`](Python#combinepy) to point to the absolute path of the Examples folder. Run it, piping standard out into a file. For example,

```bash
$ python ../Python/combine.py > combined.csv;
```

[`Python/seegrapher.py`](Python#seegrapherpy) and [`Python/graph-lin.py`](Python#graphlinpy) can be run on this CSV file to generate graphs.

[`Python/shadowfinder.py`](Python#shadowfinderpy) can be run on each `.cub` file to generate a CSV file. Note that the values generated will be the $\mathrm{log}_{10}$ of the original value. [`Python/shadowgrapher.py`](Python#shadowgrapherpy) can be run on these CSV files to generate shadow graphs.