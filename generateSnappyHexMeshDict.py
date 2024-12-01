#!/usr/bin/env python3
"""
Filename: generateSnappyHexMeshDict.py
Author: G. Vijaya Kumar
Date: November 30, 2024
Description: Generate snappyHexMeshDict
Compatible with: ESI OpenFOAM-v2312

Instructions: 
1. The OpenFOAM environment should be sourced first
2. The surface files should be in .stl file
3. Edge files can be all supported OpenFOAM formats
"""

import os
import subprocess
import argparse
import sys

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

def get_boolean_input(prompt):
    """
    Prompt the user for a boolean response (True/False).
    :param prompt: The question to display to the user.
    :return: True for 'true', False for 'false'.
    """
    while True:
        response = input(prompt + " yes (y/Y) or no (n/N): ").strip().lower()
        if response in ["true", "t", "yes", "y", "1", "Y"]:
            return True
        elif response in ["false", "f", "no", "n", "0", "N"]:
            return False
        else:
            print("Invalid input. Please type 'true' or 'false'.")

def get_vector(prompt):
    """
    Prompt the user for a 3-component vector and return it as a string in the format "(x y z)".
    :param prompt: The message to display to the user.
    :return: A string representing the vector in the format "(x y z)".
    """
    while True:
        try:
            user_input = input(prompt + " x y z: ").strip()
            components = user_input.split()
            
            # Ensure exactly 3 components are provided
            if len(components) != 3:
                raise ValueError("You must enter exactly 3 components.")
            
            # Convert components to floats to validate them as numbers
            components = [float(component) for component in components]
            
            # Format the vector as a string
            return f"({components[0]} {components[1]} {components[2]})"
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def list_files(directory):
    """
    List all files in a directory.
    :param directory: Path to the directory.
    :return: List of file names.
    """
    try:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")
        
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            raise FileNotFoundError(f"No files found in the directory '{directory}'.")
        
        return files
    except FileNotFoundError as e:
        print(e)
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_stl_zone_names(stl_file_path):
    """
    Extract the names of zones from an ASCII STL file.
    :param stl_file_path: Path to the STL file.
    :return: A list of zone names.
    """
    try:
        with open(stl_file_path, 'r') as file:
            lines = file.readlines()
        
        zone_names = []
        for line in lines:
            stripped_line = line.strip().lower()
            if stripped_line.startswith("solid"):
                # Extract the zone name (everything after 'solid')
                parts = line.strip().split(maxsplit=1)
                if len(parts) > 1:  # Check if there's a name after 'solid'
                    zone_names.append(parts[1])
                else:
                    zone_names.append("Unnamed Zone")  # Default for unnamed zones
        
        if zone_names:
            return zone_names
        else:
            return "No zones found in the STL file."
    except FileNotFoundError:
        return f"File not found: {stl_file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

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
    
    add_boundary_layers = get_boolean_input("Add boundary layers?")

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
    # geometry section
    #--------------------------------
    geometry_folder = "constant/triSurface"
    geom_files = list_files(geometry_folder)
    
    print("\nGeometric files in constant/triSurface directory:")
    for i, file in enumerate(geom_files, start=1):
        print(f"{i}. {file}")
    
    # Get surface files from user input
    surface_input = input("\nSurface files in this list (numbers separated by spaces): ").strip()
    edge_input = input("Edge files in this list (numbers separated by spaces): ").strip()
    
    surface_files=[]
    edge_files=[]
    try:
        surface_indices = [int(num) for num in surface_input.split()]
        edge_indices = [int(num) for num in edge_input.split()]
        
        # Map indices to file names
        surface_files = [geom_files[i - 1] for i in surface_indices]
        edge_files = [geom_files[i - 1] for i in edge_indices]

        if not set(surface_files).isdisjoint(set(edge_files)):
            sys.exit("Surface files and Edge files should be mutually exclusive!")
    except (ValueError, IndexError):
        print("Invalid input. Please ensure you enter valid numbers corresponding to the file list.")

    for ii in range(len(surface_files)):
        surface_file_path = os.path.join(geometry_folder, surface_files[ii])
        stl_region_name = os.path.splitext(surface_files[ii])[0]    # removing suffix .stl
        print(ii)
        print(stl_region_name)
        execute_command("foamDictionary system/snappyHexMeshDict -entry geometry/"+surface_files[ii]+" -add \"{}\"")
        execute_command(f"foamDictionary system/snappyHexMeshDict -entry geometry/{surface_files[ii]}/type -add triSurfaceMesh")
        execute_command(f"foamDictionary system/snappyHexMeshDict -entry geometry/{surface_files[ii]}/name -add {stl_region_name}")
        zone_names = get_stl_zone_names(surface_file_path)
        print(zone_names)
        num_zones = len(zone_names)
        if(num_zones > 1):
            execute_command("foamDictionary system/snappyHexMeshDict -entry geometry/"+surface_files[ii]+"/regions"+" -add \"{}\"")
            for jj in range(num_zones):
                execute_command("foamDictionary system/snappyHexMeshDict -entry geometry/"+surface_files[ii]+"/regions/"+zone_names[jj]+" -add \"{}\"")
                execute_command(f"foamDictionary system/snappyHexMeshDict -entry geometry/{surface_files[ii]}/regions/{zone_names[jj]}/name -add {zone_names[jj]}")
            
    #--------------------------------
    # castellatedMeshControls section
    #--------------------------------
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxLocalCells -add 100000000")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxGlobalCells -add 300000000")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/minRefinementCells -add 10")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/maxLoadUnbalance -add 0.1")

    # features - refinement level
    #--------------------------------------------------------------------------------------------------
    with open(snappy_hex_mesh_dict_file, "r") as file:
        lines = file.readlines()
    
    modified_lines = []
    inside_castellated_section = False

    for line in lines:
        stripped_line = line.strip()
        modified_lines.append(line)

        # Detect the start of 'castellatedMeshControls' section
        if stripped_line.startswith("castellatedMeshControls"):
            inside_castellated_section = True

        # Detect the end of 'castellatedMeshControls' section
        if inside_castellated_section and stripped_line == "}":
            # Append the 'features' section before the closing brace
            modified_lines.insert(-1, "    features\n")
            modified_lines.insert(-1,"    (\n")
            for ii in range(len(edge_files)):
                modified_lines.insert(-1,"        {\n")
                modified_lines.insert(-1,f"        file    \"{edge_files[ii]}\";\n")
                edge_ref_level = int(input(f"Enter refinement level for {edge_files[ii]}: "))
                modified_lines.insert(-1,f"        level    {edge_ref_level};\n")
                modified_lines.insert(-1,"        }\n")
            modified_lines.insert(-1,"    );\n")
            inside_castellated_section = False  # Exit the section
    #--------------------------------------------------------------------------------------------------
    # END OF features - refinement level
    
    # Write back the modified content
    with open(snappy_hex_mesh_dict_file, "w") as file:
        file.writelines(modified_lines)    

    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/refinementRegions -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/refinementSurfaces -add \"{}\"")
    execute_command("foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/resolveFeatureAngle -add 30")
    
    print("Enter the number of cells between mesh levels...")
    print("1 - fast transition, low cell count, may cause convergence issues")
    print("2 - balanced transition and cell count (preferred)")
    print("3 - slow transition, high cell count, robust")
    num_cells_between_levels = int(input("Value = "))

    execute_command(f"foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/nCellsBetweenLevels -add {num_cells_between_levels}")

    # castellatedMeshControls --> features section
    
    location_in_mesh = get_vector("Enter a point (region to keep): ")
    execute_command(f"foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/locationInMesh -add \"{location_in_mesh}\"")
    
    execute_command(f"foamDictionary system/snappyHexMeshDict -entry castellatedMeshControls/allowFreeStandingZoneFaces -add false")

    #--------------------------------
    # snapControls section
    #--------------------------------
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/nSmoothPatch -add 3")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/nSmoothInternal -add 5")
    execute_command(f"foamDictionary system/snappyHexMeshDict -entry snapControls/tolerance -add 2.0")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/nSolveIter -add 30")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/nRelaxIter -add 5")
    execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/nFeatureSnapIter -add 10")

    feature_snap_type = int(input("Type of snapping feature edges: explicit (1) or implicit (0) ? "))

    if(feature_snap_type == 1):
        if(len(edge_files) > 0):
            execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/implicitFeatureSnap -add false")
            execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/explicitFeatureSnap -add true")
            execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/multiRegionFeatureSnap -add true")
        else:
            print("WARNING: Explicit feature edge snapping chosen, but no feature edges are defined. Continuing with implicit feature edge snapping")
            feature_snap_type = 0
            
    if(feature_snap_type == 0):
        execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/implicitFeatureSnap -add true")
        execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/explicitFeatureSnap -add false")
        execute_command("foamDictionary system/snappyHexMeshDict -entry snapControls/multiRegionFeatureSnap -add false")
    
    print(f"File '{snappy_hex_mesh_dict_file}' generation succesfull.")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
