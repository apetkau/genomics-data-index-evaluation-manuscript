#!/bin/sh

for case_file in case*.yaml;
do
	name=`basename $case_file .yaml`
	d=`date | tr -d '\n'`
	echo "$d: query comparison $case_file"
	papermill template-5-query.ipynb 4-query.${name}.ipynb -f $case_file
done
