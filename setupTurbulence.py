#!/usr/bin/env python3
"""
Filename: setupTurbulence.py
Author: G. Vijaya Kumar
Date: January 7, 2023
Description: Create the momentumTransport and other turbulence related dictionaries
"""

import os
import sys

folder_name = "constant"
file_name = "momentumTransport"
# List of valid RANS models
valid_rans_models = ["kEpsilon", "realizableKE", "RNGkEpsilon", "kOmega", "kOmegaSST", "SpalartAllmaras", "v2f"]

# Check if the folder exists
if not os.path.exists(folder_name) or not os.path.isdir(folder_name):
    print(f"Fatal Error: The folder '{folder_name}' does not exist in the current directory.")
    sys.exit(1)

# Get a list of directories inside the constant folder
subdirectories = [d for d in os.listdir(folder_name) if os.path.isdir(os.path.join(folder_name, d))]

# Filter out the "polyMesh" directory
other_directories = [d for d in subdirectories if d != "polyMesh"]

if other_directories:
    print("Other directories in 'constant' folder:")
    for index, directory in enumerate(other_directories, start=1):
        print(f"{index}. {directory}")

    user_choice = input("Which region would you like to build the momentTransport dictionary? (Enter the corresponding number or press Enter to use 'constant'): ")

    if user_choice and user_choice.isdigit() and 1 <= int(user_choice) <= len(other_directories):
        selected_directory = os.path.join(folder_name, other_directories[int(user_choice) - 1])
    else:
        print("Invalid choice. Using 'constant' folder.")
        selected_directory = folder_name

else:
    print("No directories other than 'polyMesh' found in 'constant' folder.")
    selected_directory = folder_name

# Create or recreate the 'momentumTransport' file in the selected directory
file_path = os.path.join(selected_directory, file_name)

# Check if the file already exists and delete it
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Existing file '{file_name}' deleted in '{selected_directory}' folder.")

# Get user input for turbulence
turbulence_input = input("Is turbulence ON or OFF? (Enter 'ON' or 'OFF'): ")

# Process user input for turbulence
if turbulence_input.upper() == "OFF":
    turbulence_line = "simulationType    laminar;"
elif turbulence_input.upper() == "ON":
    turbulence_type = input("Is it a RANS or LES simulation? (Enter 'RANS' or 'LES'): ")
    if turbulence_type.upper() == "RANS":
        rans_model = input(f"Choose the RANS model: {', '.join(valid_rans_models)}: ")
        while rans_model not in valid_rans_models:
            print("Invalid RANS model. Please choose a valid model.")
            rans_model = input(f"Choose the RANS model: {', '.join(valid_rans_models)}: ")
        turbulence_line = f"""simulationType    RAS;

RAS
{{
    model           {rans_model};
    turbulence      on; 
    printCoeffs     on; 
    viscosityModel  Newtonian;
}}
"""
    elif turbulence_type.upper() == "LES":
        print("LES is not supported yet! Aborting.")
        exit(1)
    else:
        print("Invalid turbulence type. Aborting.")
        exit(1)
else:
    print("Invalid turbulence input. Aborting.")
    exit(1)

# Create the new 'momentumTransport' file and write the specified content
file_content = f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  11
     \\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    format      ascii;
    class       dictionary;
    location    "constant";
    object      momentumTransport;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

{turbulence_line}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""

# Create the new 'momentumTransport' file
with open(file_path, 'w') as file:
    file.write(file_content)

print(f"New file '{file_name}' created in '{selected_directory}' folder.")
