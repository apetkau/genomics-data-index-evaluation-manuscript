#!/bin/sh

for simulation in simulation*.yaml;
do
	name=`basename $simulation .yaml`
	d=`date | tr -d '\n'`
	echo "$d: query comparison $simulation"
	papermill template-5-query.ipynb 5-query.${name}.ipynb -f $simulation
done
