#!/bin/sh

for case_file in case-04.yaml case-08.yaml case-16.yaml case-full.yaml case-full-si.yaml;
do
	name=`basename $case_file .yaml`
	d=`date | tr -d '\n'`
	echo "$d: analysis for $case_file"
	papermill --log-output template-3-index-genomes.ipynb 3-index-genomes.${name}.ipynb -f $case_file
done
