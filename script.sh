#! /usr/bin/bash

mkdir -p split_in/ split_out/
split -l 20 input.txt split_in/

for f in $(ls split_in); do
	python3 main.py < split_in/$f > split_out/$f &
done

wait

cat split_out/* >> output.csv
