#!/bin/sh

for simulation in simulation*.yaml;
do
	name=`basename $simulation .yaml`
	d=`date | tr -d '\n'`
	echo "$d: variants comparison $simulation"
	papermill --log-output template-4-variants-comparison.ipynb 4-variants-comparison.${name}.ipynb -f $simulation
done
