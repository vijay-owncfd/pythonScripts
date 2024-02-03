#!/usr/bin/env python3
"""
Filename: setBoundaryConditions.py
Author: G. Vijaya Kumar
Date: 3rd February 2024
Description: Setup the initial and boundary conditions, i.e., create 0 folder
"""

import os
import re
import subprocess
import sys

#----------------------------------------------------------------------------------------------------------------
def run_command(command):
    try:
        # Run the OpenFOAM command and capture the output
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)

        # Access the output from the 'result' variable
        command_output = result.stdout.strip()

        # Return the output
        return command_output

    except subprocess.CalledProcessError as e:
        print(f"Error executing the OpenFOAM command: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
#----------------------------------------------------------------------------------------------------------------
def create_or_check_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created.")
    else:
        print(f"Directory '{directory_name}' already exists. Its contents will be overwritten!")
#----------------------------------------------------------------------------------------------------------------
def setWallBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model):
    wall_type=int(input("Enter wall type:\n 1. No slip wall (non-moving)\n 2. Slip wall\n 3. Moving wall\n"))
    if(wall_type==1):
        # Velocity
        run_command(f'foamDictionary 0/U -entry boundaryField/{bound} -add \"{{}}\"')
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add noSlip")
        # Pressure
        if(simulation_mode==1):
            run_command(f'foamDictionary 0/p -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/type -add fixedFluxPressure")
            run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/value -add \"uniform 0.0\"")
            run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/gradient -add \"uniform 0.0\"")
        # Turbulence 
        if(turbulence_model_type=="RAS"):
            if(RANS_model=="kOmega" or RANS_model=="kOmegaSST"):
                # TKE
                run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add kqRWallFunction")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
                # Omega
                run_command(f'foamDictionary 0/omega -entry boundaryField/{bound} -add \"{{}}\"')
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/type -add omegaWallFunction")
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/blended -add true")
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/value -add \"uniform 1000.0\"")
            elif(RANS_model=="kEpsilon" or RANS_model=="LaunderSharmaKE" or RANS_model=="realizableKE" or RANS_model=="RNGkEpsilon"):
                # TKE
                run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add kqRWallFunction")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
                # Epsilon
                run_command(f'foamDictionary 0/epsilon -entry boundaryField/{bound} -add \"{{}}\"')
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/type -add epsilonWallFunction")
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/value -add \"uniform 1000\"")
            else:
                print(f"The RANS turbulence model - {RANS_model} is not supported yet!")
                sys.exit(1)
            # Turbulent viscosity
            run_command(f'foamDictionary 0/nut -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/type -add nutUSpaldingWallFunction")
            run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
            # Turbulent thermal diffusivity
            if(simulation_mode==2):
                run_command(f'foamDictionary 0/alphat -entry boundaryField/{bound} -add \"{{}}\"')
                run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/type -add alphatJayatillekeWallFunction")
                run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/Prt -add 0.85")
                run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
    else:
        print("Wall type not supported yet.")
        sys.exit(1)
        
#----------------------------------------------------------------------------------------------------------------
def setInletBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model):
    inlet_type=int(input("Enter INLET type:\n1. Velocity components\n2. Mass flow rate\n3. Volume flow rate\n4. Mean velocity + Profile\n5. Something else\n"))
    # Velocity 
    run_command(f'foamDictionary 0/U -entry boundaryField/{bound} -add \"{{}}\"')
    if(inlet_type==1):
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add fixedValue")
        print("Enter velocity components in m/s\n")
        Ux_in = float(input("Ux = "))
        Uy_in = float(input("Uy = "))
        Uz_in = float(input("Uz = "))
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/value -set \"uniform ({Ux_in} {Uy_in} {Uz_in})\"")
    elif(inlet_type==2):
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add flowRateInletVelocity")
        mDot = float(input("Enter mass flow rate in kg/s: "))
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/massFlowRate -add {mDot}")
        if(simulation_mode==1):
            rho_in = float(input(f"Enter density of the fluid at {bound} in kg/m3: "))
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/rhoInlet -add {rho_in}")
        else:
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/rho -add rho")
        velProfile = int(input("None(0) or Laminar(1) or turbulent(2) or velocity profile: "))
        if(velProfile==1):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add laminarBL")
        elif(velProfile==2):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add turbulentBL")
        else:
            print("No profile imposed.")
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/value -add \"uniform (0 0 0)\"")
    elif(inlet_type==3):
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add flowRateInletVelocity")
        QDot = float(input("Enter volume flow rate in m3/s: "))
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/volumetricFlowRate -add {QDot}")
        velProfile = int(input("None(0) or Laminar(1) or turbulent(2) or velocity profile: "))
        if(velProfile==1):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add laminarBL")
        elif(velProfile==2):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add turbulentBL")
        else:
            print("No profile imposed.")
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/value -add \"uniform (0 0 0)\"")
    elif(inlet_type==4):
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add flowRateInletVelocity")
        UMean = float(input("Enter the mean velocity in m/s: "))
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/meanVelocity -add {UMean}")
        velProfile = int(input("None(0) or Laminar(1) or turbulent(2) or velocity profile: "))
        if(velProfile==1):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add laminarBL")
        elif(velProfile==2):
            run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/profile -add turbulentBL")
        else:
            print("No profile imposed.")
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/value -add \"uniform (0 0 0)\"")
    else:
        print("Inlet type not implemented yet!")
        sys.exit(1)
    # Pressure
    if(simulation_mode==1):
        run_command(f'foamDictionary 0/p -entry boundaryField/{bound} -add \"{{}}\"')
        run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/type -add fixedFluxPressure")
        run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/value -add \"uniform 0.0\"")
        run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/gradient -add \"uniform 0.0\"")
    # Turbulence 
    if(turbulence_model_type=="RAS"):
        turb_inlet_mode = int(input("Intensity and Turbulent length scale (1) or Dirichlet values (2): "))
        if(RANS_model=="kOmega" or RANS_model=="kOmegaSST"):
            run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f'foamDictionary 0/omega -entry boundaryField/{bound} -add \"{{}}\"')
            if(turb_inlet_mode==1):
                # TKE
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add turbulentIntensityKineticEnergyInlet")
                I_in = float(input("Turbulent Intensity as a fraction: "))
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/intensity -add {I_in}")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
                # omega
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/type -add turbulentMixingLengthFrequencyInlet")
                l_in = float(input("Turbulent length scale in m: "))
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/mixingLength -add {l_in}")
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/value -add \"uniform 1000.0\"")
            elif(turb_inlet_mode==2):
                tke_in = float(input("Enter TKE at inlet in m2/s2: "))
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add fixedValue")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform {tke_in}\"")
                omega_in = float(input("Enter Omega at inlet in 1/s: "))
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/type -add fixedValue")
                run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/value -add \"uniform {omega_in}\"")
            else:
                print("Wrong option!")
                sys.exit(1)
        elif(RANS_model=="kEpsilon" or RANS_model=="LaunderSharmaKE" or RANS_model=="realizableKE" or RANS_model=="RNGkEpsilon"):
            run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f'foamDictionary 0/epsilon -entry boundaryField/{bound} -add \"{{}}\"')
            if(turb_inlet_mode==1):
                # TKE
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add turbulentIntensityKineticEnergyInlet")
                I_in = float(input("Turbulent Intensity as a fraction: "))
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/intensity -add {I_in}")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
                # epsilon
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/type -add turbulentMixingLengthDissipationRateInlet")
                l_in = float(input("Turbulent length scale in m: "))
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/mixingLength -add {l_in}")
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/value -add \"uniform 1000.0\"")
            elif(turb_inlet_mode==2):
                tke_in = float(input("Enter TKE at inlet in m2/s2: "))
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add fixedValue")
                run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -add \"uniform {tke_in}\"")
                epsilon_in = float(input("Enter epsilon at inlet in m2/s3: "))
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/type -add fixedValue")
                run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/value -add \"uniform {epsilon_in}\"")
            else:
                print("Wrong option!")
                sys.exit(1)
        else:
            print(f"The RANS turbulence model - {RANS_model} is not supported yet!")
            sys.exit(1)
        # Turbulent viscosity
        run_command(f'foamDictionary 0/nut -entry boundaryField/{bound} -add \"{{}}\"')
        run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/type -add calculated")
        run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
        # Turbulent thermal diffusivity
        if(simulation_mode==2):
            run_command(f'foamDictionary 0/alphat -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/type -add calculated")
            run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")


#----------------------------------------------------------------------------------------------------------------
def setOutletBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model):
    outlet_type=int(input("Enter OUTLET type:\n1. Pressure outlet\n2. Something else\n"))

    if(outlet_type==1):
        # Velocity 
        run_command(f'foamDictionary 0/U -entry boundaryField/{bound} -add \"{{}}\"')
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/type -add inletOutlet")
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/inletValue -set \"uniform (0 0 0)\"")
        run_command(f"foamDictionary 0/U -entry boundaryField/{bound}/value -set \"uniform (0 0 0)\"")
        # Pressure
        if(simulation_mode==1):
            run_command(f'foamDictionary 0/p -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/type -add fixedValue")
            p_out = float(input("Outlet pressure in m2/s2 (p/rho form) : "))
            run_command(f"foamDictionary 0/p -entry boundaryField/{bound}/value -add \"uniform {p_out}\"")
    else:
        print("OUTLET type not supported yet!")
        sys.exit(1)

    # Turbulence outlet setup is same for all types of outlet boundaries
    if(turbulence_model_type=="RAS"):
        if(RANS_model=="kOmega" or RANS_model=="kOmegaSST"):
            # TKE
            run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add inletOutlet")
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/inletValue -set \"uniform 1e-10\"")
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -set \"uniform 1e-10\"")
            # Omega
            run_command(f'foamDictionary 0/omega -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/type -add inletOutlet")
            run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/inletValue -set \"uniform 1000\"")
            run_command(f"foamDictionary 0/omega -entry boundaryField/{bound}/value -set \"uniform 1000\"")
        elif(RANS_model=="kEpsilon" or RANS_model=="LaunderSharmaKE" or RANS_model=="realizableKE" or RANS_model=="RNGkEpsilon"):
            # TKE
            run_command(f'foamDictionary 0/k -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/type -add inletOutlet")
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/inletValue -set \"uniform 1e-10\"")
            run_command(f"foamDictionary 0/k -entry boundaryField/{bound}/value -set \"uniform 1e-10\"")
            # Epsilon
            run_command(f'foamDictionary 0/epsilon -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/type -add inletOutlet")
            run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/inletValue -set \"uniform 1000\"")
            run_command(f"foamDictionary 0/epsilon -entry boundaryField/{bound}/value -set \"uniform 1000\"")
        else:
            print(f"The RANS turbulence model - {RANS_model} is not supported yet!")
            sys.exit(1)
        # Turbulent viscosity
        run_command(f'foamDictionary 0/nut -entry boundaryField/{bound} -add \"{{}}\"')
        run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/type -add calculated")
        run_command(f"foamDictionary 0/nut -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")
        # Turbulent thermal diffusivity
        if(simulation_mode==2):
            run_command(f'foamDictionary 0/alphat -entry boundaryField/{bound} -add \"{{}}\"')
            run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/type -add calculated")
            run_command(f"foamDictionary 0/alphat -entry boundaryField/{bound}/value -add \"uniform 1e-10\"")

#----------------------------------------------------------------------------------------------------------------

sampleFilesDir="/home/pc/gitRepos/pythonScripts/caseGenerator/sampleFiles/boundaryFiles"

create_or_check_directory("0")

simulation_mode = int(input("Incompressible (1) or compressible simulation (2) ? : "))

if(simulation_mode==1):
    run_command("cp "+sampleFilesDir+"/incompressible/p 0/")
    run_command("cp "+sampleFilesDir+"/incompressible/U 0/")
elif(simulation_mode==2):
    print("Implementation incomplete for compressible flows.")
    sys.exit(1)

turbulence_model_type = run_command("foamDictionary constant/momentumTransport -entry simulationType -value")

# Copying files necessary for turbulence
RANS_model=""
if(turbulence_model_type == "RAS"):
    RANS_model = run_command("foamDictionary constant/momentumTransport -entry RAS/model -value")
    
    run_command("cp "+sampleFilesDir+"/turbulence/nut 0/")
    
    if(simulation_mode==2):
        run_command("cp "+sampleFilesDir+"/turbulence/alphat 0/")

    if(RANS_model=="kOmega" or RANS_model=="kOmegaSST"):
        run_command("cp "+sampleFilesDir+"/turbulence/k 0/")
        run_command("cp "+sampleFilesDir+"/turbulence/omega 0/")
    elif(RANS_model=="kEpsilon" or RANS_model=="LaunderSharmaKE" or RANS_model=="realizableKE" or RANS_model=="RNGkEpsilon"):
        run_command("cp "+sampleFilesDir+"/turbulence/k 0/")
        run_command("cp "+sampleFilesDir+"/turbulence/epsilon 0/")
    else:
        print(f"The RANS turbulence model - {RANS_model} is not supported yet!")
        sys.exit(1)
        
elif(turbulence_model_type == "laminar"):
    print("Turbulence is OFF")
else:
    print("Incompatible turbulence model type in constant/momentumTransport file .")
    sys.exit(1)


#-----------------------------------------------------------------------------------------------------------
'''
# Set initial conditions
print("Setting initial conditions..\n")
# initial condition - velocity
print("Enter initial velocity components in m/s\n")
Ux_init = float(input("Ux = "))
Uy_init = float(input("Uy = "))
Uz_init = float(input("Uz = "))
run_command(f"foamDictionary 0/U -entry internalField -set \"uniform ({Ux_init} {Uy_init} {Uz_init})\"")

# initial condition - pressure
if(simulation_mode==1):
    pres_init = float(input("Enter initial pressure (p/rho) form in m2/s2: "))
    run_command(f"foamDictionary 0/p -entry internalField -set \"uniform {pres_init}\"")

# initial conditions - turbulence quantities
if(turbulence_model_type=="RAS"):
    if(RANS_model=="kOmega" or RANS_model=="kOmegaSST"):
        tke_init = float(input("Enter initial TKE in m2/s2 (typically 1.0): "))
        run_command(f"foamDictionary 0/k -entry internalField -set \"uniform {tke_init}\"")
        omega_init = float(input("Enter initial Omega in 1/s (typically 100.0): "))
        run_command(f"foamDictionary 0/omega -entry internalField -set \"uniform {omega_init}\"")
    elif(RANS_model=="kEpsilon" or RANS_model=="LaunderSharmaKE" or RANS_model=="realizableKE" or RANS_model=="RNGkEpsilon"):
        tke_init = float(input("Enter initial TKE in m2/s2 (typically 1.0): "))
        run_command(f"foamDictionary 0/k -entry internalField -set \"uniform {tke_init}\"")
        eps_init = float(input("Enter initial Epsilon in m2/s3 (typically 100.0): "))
        run_command(f"foamDictionary 0/epsilon -entry internalField -set \"uniform {eps_init}\"")
    else:
        print(f"The RANS turbulence model - {RANS_model} is not supported yet!")
        sys.exit(1)
    nut_init = float(input("Enter initial Turbulent Viscosity in m2/s (typically 1e-10): "))
    run_command(f"foamDictionary 0/nut -entry internalField -set \"uniform {nut_init}\"")
    if(simulation_mode==2):
        alphat_init = float(input("Enter initial Turbulent thermal diffusivity in kg/m/s (typically 1e-10): "))
        run_command(f"foamDictionary 0/alphat -entry internalField -set \"uniform {alphat_init}\"")
'''    
#-----------------------------------------------------------------------------------------------------------
    
boundary_list = subprocess.run("foamDictionary constant/polyMesh/boundary -entry entry0 -keywords", shell=True, check=True, text=True, stdout=subprocess.PIPE)
boundary_list = [line.strip().replace(' ', '') for line in boundary_list.stdout.splitlines()]

for bound in boundary_list:
    bound_type = run_command(f"foamDictionary constant/polyMesh/boundary -entry entry0/{bound}/type -value")
    print(f"\nSetting boundary conditions for {bound} of type {bound_type}")
    if(bound_type=="wall"):
        setWallBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model)
    elif(bound_type=="patch"):
        patch_type = int(input("Enter patch type:\n1. INLET \n2. OUTLET \n3. something else\n"))
        if(patch_type==1):
            setInletBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model)
        elif(patch_type==2):
            setOutletBoundaryConditions(bound, simulation_mode, turbulence_model_type, RANS_model)
        else:
            print("Patch type not supported yet!")
            sys.exit(1)
    else:
        continue


