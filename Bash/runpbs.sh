#!/bin/bash

DIR='/full/directory/path'

find $DIR -name "*.pbs" -exec sh -c 'qsub "$0"' {} \;
exit;