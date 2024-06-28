#!/bin/bash

filepath1="/media/gerard/LIBRARY/movies"
filepath2="/media/gerard/library/movies"

#find ~/Videos/movies -type f -exec ls -h {} \; | sed 's|^/home/gerard/Videos/movies/||' | sort > ~/Videos/movies_listing/list1.txt
find "$filepath1" -type f -exec ls -h {} \; | sed "s|^$filepath1/||" | sort > ~/Videos/movies_listing/list1.txt
find "$filepath2" -type f -exec ls -h {} \; | sed "s|^$filepath2/||" | sort > ~/Videos/movies_listing/list2.txt

#find ~/Videos/movies -type f -exec ls -h {} \; | sed 's|^/home/gerard/Videos/movies/||' | sort > ~/Videos/movies_listing/list2.txt

#ssh gerard@192.168.0.145 "find /mnt/movies -name lost+found -prune -o -type f -exec ls -h {} \; | sed 's|^/mnt/movies/||' | sort" > ~/Videos/movies_listing/list_2.txt
diff -u ~/Videos/movies_listing/list1.txt ~/Videos/movies_listing/list2.txt | grep '^-' | sed 's/^-//' > ~/Videos/movies_listing/differences.txt
#remove first line of the ~/Videos/movies_listing/differences2_corr.txt file
sed -i '1d' ~/Videos/movies_listing/differences.txt
# remove lines with .part, .zip and .rar
#sed -i -e '/.part/d' -e '/.zip/d' -e '/.rar/d' ~/Videos/movies_listing/differences.txt
sed -i -e '/.zip/d' -e '/.rar/d' ~/Videos/movies_listing/differences.txt