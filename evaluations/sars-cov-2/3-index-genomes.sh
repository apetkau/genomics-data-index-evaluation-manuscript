#!/bin/sh

#for case_file in *.yaml; 
for case_file in case-10000-batch-10000.yaml case-20000-batch-10000.yaml case-2000-batch-10000.yaml case-5000-batch-10000.yaml;
do
	name=`basename $case_file .yaml`
	d=`date | tr -d '\n'`
	echo "$d: analysis for $case_file"
	papermill --log-output template-3-index-genomes.ipynb 3-index-genomes.${name}.ipynb -f $case_file
done
