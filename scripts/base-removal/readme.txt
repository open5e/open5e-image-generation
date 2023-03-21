This script will remove any object that contains the word "Creature" (which is used for the name of bases in this collection).
It will iterate over an entire directory of .blend files, removing that object from each one then saving the result.

-------- Usage

Copy the script to a convenient place on your system. 

Open the script & replace "REPLACE_ME" with the directory of .blend files you wish to clean up

Go to the location of your Blender executable. 

Run blender -b -P "[SCRIPT LOCATION]\remove_bases.py"


The resulting .blend files will be the cleaned up files. The .blend1 files are the originals.