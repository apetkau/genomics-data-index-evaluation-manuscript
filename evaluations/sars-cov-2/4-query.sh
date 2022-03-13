#!/bin/sh

for case_dir in cases/case-*;
do        
	name=`basename $case_dir`
	case_file=${name}.yaml
	index_info=$case_dir/index-info.tsv
	query_cli=$case_dir/query-cli.tsv

	if [ -e $index_info ];
	then
		if [ -e $query_cli ];
		then
			echo "Already ran queries for case $case_dir, skipping"
		else
			d=`date | tr -d '\n'`
			echo "$d: query comparison $case_file"
			papermill --log-output template-4-query.ipynb 4-query.${name}.ipynb -f $case_file
		fi
	else
		echo "case $case_dir is not completed yet"
	fi
done
