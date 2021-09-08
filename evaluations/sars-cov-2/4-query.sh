#!/bin/sh

#for case_file in case-10.yaml case-20.yaml case-50.yaml case-100.yaml case-200.yaml case-500.yaml case-1000.yaml case-2000.yaml case-5000.yaml case-10000.yaml;
#for case_file in case-10.yaml case-20.yaml case-50.yaml;
for case_file in case-200.yaml;
do
	name=`basename $case_file .yaml`
	d=`date | tr -d '\n'`
	echo "$d: query comparison $case_file"
	papermill template-4-query.ipynb 4-query.${name}.ipynb -f $case_file
done
