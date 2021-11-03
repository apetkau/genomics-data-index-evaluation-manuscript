#!/bin/sh

SNAPSHOT_DIR=snapshots
INDEX=index
ncores=32

gdi --version

counter=0
for i in input/input-split/*.tsv
do
	b=`basename $i .tsv`

	echo "\n"
        if [ $(($counter % 5)) -eq 2 ]
	then
		snapshot="${SNAPSHOT_DIR}/index_${b}"
		echo "Making snapshot $snapshot on `date | tr -d '\n'`"
		cp -r "$INDEX" "$snapshot"
		echo "Finished making snapshot $snapshot on `date | tr -d '\n'`"
	else
		echo "Skipping snapshot for $i on `date | tr -d '\n'`"
	fi
	echo
	
	gdi --project-dir $INDEX --ncores $ncores analysis --reference-file references/NC_045512.gbk.gz --sample-batch-size 2000 --use-conda --input-structured-genomes-file $i
	ret_value=$?
	if [ $ret_value -ne 0 ]
	then
		echo "Error indexing $i. Previous snapshot is $snapshot"
		exit 1
	else
		echo "Successfully indexed $i"
	fi

	counter=$((counter+1))
done

echo "Finished indexing all genomes in $index"
