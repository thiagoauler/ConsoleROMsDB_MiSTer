#!/bin/sh

for directory in MiSTer/*
do
   if test -d "$directory"
   then
      echo
      echo Processing new system
      echo ... $directory ...
      skipped=0
      for filename in "$directory"/*
      do
         header=$(hexdump -e '16/1 "%02x"' -n 4 "$filename")
         if [ $header == 4e45531a ]
         then
            filehash=$(tail -c +17 "$filename" | md5 -q)"."$(md5 -q "$filename")
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
            skipped=$((skipped + 1))
         fi
      done
      echo Skipped $skipped files.
   fi
done
