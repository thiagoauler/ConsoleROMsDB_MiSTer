#!/bin/sh

for directory in MiSTer/*
do
   echo
   echo Processing new system
   echo ... $directory ...
   for filename in "$directory"/*
   do
      header=$(hexdump -e '16/1 "%02x"' -n 4 "$filename")
      if [ $header == 4e45531a ]
      then
         filehash=$(tail -c +17 "$filename" | md5 -q)
      else
         filehash=$(md5 -q "$filename")
      fi
      newfilename="$directory"/"$filehash".rom

      if [ "$filename" != "$newfilename" ]
      then
         if test -f "$newfilename"
         then
            echo "Conflict: " $filename
         else
            mv "$filename" "$newfilename"
         fi
      else
         echo Skip $filename
      fi
   done
done
