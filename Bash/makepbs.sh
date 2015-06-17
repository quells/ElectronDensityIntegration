#!/bin/bash

DIR='/full/directory/path'

find $DIR -name '*.cub' -exec sh -c 'echo "#!/bin/bash
#PBS -l walltime=02:00:00
#PBS -l nodes=1:ppn=1
#PSD -N spherical_edensity
cd \$PBS_O_WORKDIR;
/full/directory/path/integral.py -lz \"$0\";" > "$0.pbs"' {} \;
exit;