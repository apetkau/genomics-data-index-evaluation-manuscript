#!/bin/sh

for simulation in simulation*.yaml;
do
	name=`basename $simulation .yaml`
	d=`date | tr -d '\n'`
	echo "$d: simulating reads for $simulation"
	papermill template-1-simulate-reads.ipynb 1-simulate-reads.${name}.ipynb -f $simulation
	echo "$d: fixing reads for $simulation"
	papermill template-2-fix-simulated-files.ipynb 2-fix-simulated-files.${name}.ipynb -f $simulation
done
