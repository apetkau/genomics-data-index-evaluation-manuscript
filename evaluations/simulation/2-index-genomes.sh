#!/bin/sh

for simulation in simulation*.yaml;
do
	name=`basename $simulation .yaml`
	d=`date | tr -d '\n'`
	echo "$d: simulating reads for $simulation"
	papermill --log-output template-3-index-genomes.ipynb 3-index-genomes.${name}.ipynb -f $simulation
done
