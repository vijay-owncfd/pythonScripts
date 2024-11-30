#!/usr/bin/env python3
"""
Filename: generateSnappyHexMeshDict.py
Author: G. Vijaya Kumar
Date: November 30, 2024
Description: Generate snappyHexMeshDict
Developed for ESI OpenFOAM-v2312
"""

import os
import subprocess
import argparse

def execute_command(command):
    """
    Executes a shell command and handles the output.
    :param command: Command string to be executed.
    """
    try:
        result = subprocess.run(command, text=True, capture_output=True, shell=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Command failed with error:")
            print(result.stderr)
    except FileNotFoundError:
        print(f"Command not found: {command}")
    except Exception as e:
        print(f"An unexpected error occurred while executing command: {e}")

# Define the system folder and required files
system_folder = "system"
control_dict_file = os.path.join(system_folder, "controlDict")
snappy_hex_mesh_dict_file = os.path.join(system_folder, "snappyHexMeshDict")

try:
    # Check if the system folder exists
    if not os.path.exists(system_folder):
        raise FileNotFoundError(f"The directory '{system_folder}' does not exist.")
    
    # Check if controlDict file exists in the system folder
    if not os.path.isfile(control_dict_file):
        raise FileNotFoundError(f"The required file 'controlDict' is missing in the '{system_folder}' directory.")
    
    # Check if snappyHexMeshDict already exists
    if os.path.isfile(snappy_hex_mesh_dict_file):
        print("Warning: 'snappyHexMeshDict' will be overwritten by the current program.")
    
    # Create or overwrite the snappyHexMeshDict file
    with open(snappy_hex_mesh_dict_file, "w") as file:
        file.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
        file.write("| =========                 |                                                 |\n")
        file.write("| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n")
        file.write("|  \\\\    /   O peration     | Version:  v2312                                 |\n")
        file.write("|   \\\\  /    A nd           | Website:  www.openfoam.com                      |\n")
        file.write("|    \\\\/     M anipulation  |                                                 |\n")
        file.write("\*---------------------------------------------------------------------------*/\n")
        file.write("FoamFile\n")
        file.write("{\n")
        file.write("\tversion     2.0;\n")
        file.write("\tformat      ascii;\n")
        file.write("\tclass       dictionary;\n")
        file.write("\tobject      snappyHexMeshDict;\n")
        file.write("}\n")
        file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
        file.write("\n")
    
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMesh -add true")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snap -add true")
    
    add_boundary_layers = int(input("Add boundary layers? 1 (yes) or 0 (no): "))

    if add_boundary_layers:
        execute_command("foamDictionary system/snappyHexMeshDict -entry addLayers -add true")
    else:
        execute_command("foamDictionary system/snappyHexMeshDict -entry addLayers -add false")

    execute_command("foamDictionary system/snappyHexMeshDict -entry geometry -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry addLayersControls -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry meshQualityControls -add \"{}\"")

    execute_command("foamDictionary system/snappyHexMeshDict -entry mergeTolerance -add 1e-6")

    #--------------------------------
    # castellatedMeshControls section
    #--------------------------------
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxLocalCells -add 100000000")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxGlobalCells -add 300000000")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/minRefinementCells -add 10")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxLoadUnbalance -add 0.1")
    
    print("Enter the number of cells between mesh levels...")
    print("1 - fast transition, low cell count, may cause convergence issues")
    print("2 - balanced transition and cell count (preferred)")
    print("3 - slow transition, high cell count, robust")
    num_cells_between_levels = int(input("Value = "))

    execute_command(f"foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/nCellsBetweenLevels -add {num_cells_between_levels}")

    print(f"File '{snappy_hex_mesh_dict_file}' generation succesfull.")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
