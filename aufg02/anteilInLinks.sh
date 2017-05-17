#!/bin/bash

twitter=`cat links.txt | grep -c twitter`
zeilenInsg=`wc -l links.txt | cut -d ' ' -f1`
anteil=`echo "scale=2; $twitter / $zeilenInsg" | bc`

echo $twitter " / " $zeilenInsg " = " $anteil 
