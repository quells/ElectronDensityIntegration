# Convenience Scripts

## makepbs.sh

Makes batch files to be run with `qsub`. Creates a file for each `.cub` file in the directory `DIR`. Currently set to run linear integration; edit line 10 to change this.

**Must be edited** to change the `DIR` variable on lines 3 and 10 to the correct directory path.

## runpbs.sh

Runs each `.pbs` file found in the `DIR` directory. Allows manual inspection of one or more `.pbs` files before they are enqueued.

**Must be edited** to change the `DIR` variable on line 3 to the correct directory path.