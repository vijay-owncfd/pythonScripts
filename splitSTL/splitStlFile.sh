#!/bin/bash

echo "Info: Make sure that the different patches are named."
arrayA=($(awk '/^solid/ && !/endsolid/ {print NR}' $1))
arrayB=($(awk '/endsolid/ {print NR}' $1))

if [ ${#arrayA[@]} -ne ${#arrayB[@]} ]; then
    echo "Error: The number of solid and endsolid in this file do not match. Check your STL."
    exit 1
fi

# Store the size of arrayA to a variable numSTLs
numSTLs=${#arrayA[@]}

# Loop from i=0 to numSTLs
for ((i=0; i<numSTLs; i++)); do
    startLine=${arrayA[i]}
    endLine=${arrayB[i]}

	# Create a new file name based on the content of the line
    solidLine=$(sed -n "${startLine}p" $1)
    name=$(echo "$solidLine" | awk '{print $2}' | tr -d '\r')

	if [ -z "$name" ] || [ -z "$(echo "$name" | tr -d '[:space:]')" ]; then
        name="file_$i"
		echo "WARNING: No patch name is found next to the keyword solid. Giving it a automatic name."
    fi

    # Copy contents from $1 to a new file
	echo "Creating the file - ${name}.stl"
    sed -n "${startLine},${endLine}p" $1 > "${name}.stl"
done

echo "STL splitting succesful."
