# Developed by G. Vijaya Kumar on 24th December 2023
# This utility converts an edge mesh in .dat format to .obj format
# .dat can be generated with Salome
# OpenFOAM's snappyHexMesh can read .obj 

import sys
import datetime

# Function to read the .dat file containing the edge mesh information.
def read_dat_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line and extract numPoints
        first_line = file.readline().strip().split()
        numPoints = int(first_line[0])
        numEdges = int(first_line[1])

        # Initialize arrays
        dat_vertex = []        # vertex index of points in .dat file
        coordX = []            # x-coordinate of points in .dat
        coordY = []            # y-coordinate of points in .dat
        coordZ = []            # z-coordinate of points in .dat
        dat_line_start = []    # Starting vertex of the edges in the .dat file
        dat_line_end = []      # Ending vertex of the edges in the .dat file
          
        # Read the next numPoints lines of the .dat file and populate the dat_vertex, coordinate values
		# After numPoints number of lines, read the next numEdges lines containing edge (line) information and populate the 
		# starting and ending vertices in dat_line_start and dat_line_end arrays
        for i in range(numPoints+numEdges):
            line = file.readline().strip().split()
            if(i<numPoints):
                dat_vertex.append(int(line[0]))
                coordX.append(float(line[1]))
                coordY.append(float(line[2]))
                coordZ.append(float(line[3]))
            else:
                dat_line_start.append(int(line[2]))
                dat_line_end.append(int(line[3]))

    return numPoints, dat_vertex, coordX, coordY, coordZ, numEdges, dat_line_start, dat_line_end

# Function to write the obj file
def create_obj_file(file_path, numPoints, dat_vertex, coordX, coordY, coordZ, numEdges, dat_line_start, dat_line_end):
    # Create a new file with the same name and .obj extension
    obj_file_path = file_path.rsplit('.', 1)[0] + '.obj'

    # Write data to the new .obj file
    with open(obj_file_path, 'w') as obj_file:
        # Write the header with today's date
        obj_file.write(f"# Wavefront OBJ file created on {datetime.datetime.now().date()}\n")

        # Write the vertices (v)
        obj_file.write("# Vertices\n")

        # Write the coordX, coordY, and coordZ values for each vertex
        for i in range(numPoints):
            obj_file.write(f"v {coordX[i]} {coordY[i]} {coordZ[i]}\n")

        # Write the Edges
        obj_file.write("# Edges\n")
        
        # Creating the vertex array for obj file. It goes from 1 to numPoints
        obj_vertex = []
        for i in range(numPoints):
            obj_vertex.append(int(i+1))
        
        # Create key-value pairs mapping dat_vertex to obj_vertex
        dat_obj_dict = {}
        for i in range(numPoints):
            dat_obj_dict[dat_vertex[i]] = obj_vertex[i]
        
		# Writing the edges (l)
        for i in range(numEdges):
            obj_file.write(f"l {dat_obj_dict[dat_line_start[i]]} {dat_obj_dict[dat_line_end[i]]}\n")
            
    return obj_file_path

# Loop over all the .dat files
numFiles = len(sys.argv)

for i in range(1, numFiles):	
    file_path = sys.argv[i]
    numPoints, dat_vertex, coordX, coordY, coordZ, numEdges, dat_line_start, dat_line_end = read_dat_file(file_path)
	
    # Create the .obj file
    obj_file_path = create_obj_file(file_path, numPoints, dat_vertex, coordX, coordY, coordZ, numEdges, dat_line_start, dat_line_end)
    print(f"The .obj file has been created: {obj_file_path}")
