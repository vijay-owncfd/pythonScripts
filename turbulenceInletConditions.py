#!/usr/bin/env python3
"""
File: turbulenceInletConditions.py
Author: G. Vijaya Kumar
Date: 6th Aug 2023
Description: Calculates the turbulent conditions for inlet boundary and freestream
Disclaimer: This is only a helper tool and not authorized by Convergent Science. 
            The user is expected to verify the values
"""
import sys as sys
import math as math

model = int(input("Spalart-Allmaras (1) or k-epsilon based (2) or k-omega based (3) : "))

if model==1:
    sys.exit("The code is under development.. Spalart-Allmaras turbulence model is not supported yet!")
    print("Estimating nu_tilda for the Spalart-Allmaras model...")
elif model==2:
    print("Estimating turbulence quantities for the k-epsilon based model...")
elif model==3:
    print("Estimating turbulence quantities for the k-omega based model...")
else:
    sys.exit("Wrong choice!")

print("\n Choose the application type: \
        \n 1. Wall bounded flow (Pipe flow / Channel flow / Ducted flow) \
        \n 2. Inlet into a domain (e.g., Jet inlet into a chamber) \
        \n 3. External aerodynamics (Flow over flat palte / airfoil / bluff bodies \
        \n 4. High speed flows inside complex geometries \
        \n 5. Flow inside pumps or compressors \
        \n 6. I am unsure of the turbulence leves for my case \
        ")

application = int(input("Enter your choice: "))

I = 0.0
l = 1e-10
visc_rat = 1.0
k = 0.0
omega = 0.0
epsilon = 0.0
Cmu = 0.09

if application==1 or application==2:
    print("\n Choose your velocity type: \
            \n 1. Constant inlet velocity \
            \n 2. Velocity spatial profile (e.g., parabola or some tabular form \
            \n 3. Inlet velocity varies with time \
          ")
    vel_type = int(input("Enter your choice: "))

    if vel_type==1:
        U = float(input("Enter inlet velocity in m/s : "))
    elif vel_type==2:
        U = float(input("Enter averaged value of your spatial velocity profile in m/s : "))
    elif vel_type==3:
        U = float(input("Enter the max. value of velocity that you would expect in your transient profile in m/s : "))
    else:
        sys.exit("Wrong input!")

    print("\n Choose the cross-section of your inlet: \
            \n 1. Circular \
            \n 2. Annular section \
            \n 3. Square \
            \n 4. Rectangular \
            \n 5. Two-dimensional channel flow \
            \n 6. Other \
            \n 7. Specified hydraulic diameter \
         ")

    Dh = 0.0
    cross_sec = int(input("Enter your choice: "))

    if cross_sec==1:
        Dh = float(input("Enter the diameter in m : "))
    elif cross_sec==2:
        Din = float(input("Enter the inner diameter in m : "))
        Dout = float(input("Enter the outer diameter in m : "))
        Dh = Dout-Din
    elif cross_sec==3:
        Dh = float(input("Enter the side length of the square in m : "))
    elif cross_sec==4:
        a = float(input("Enter the width in m : "))
        b = float(input("Enter the height in m : "))
        Dh = 2*a*b/(a+b)
    elif cross_sec==5:
        a = float(input("Enter the height in m : "))
        Dh = 2*a
    elif cross_sec==6:
        print("You are dealing with powers beyond my ken.. \
                I need more information ...")
        A = float(input("Enter the cross-sectional area in m2 : "))
        P = A = float(input("Enter the perimeter of the cross-section in m : "))
        Dh = 4*A/P
    elif cross_sec==7:
        Dh = float(input("Enter the hydraulic diameter in m : "))
    else:
        sys.exit("Wrong input")

    print("\nEnter the fluid properties...")
    rho = float(input("Density in kg/m3 : "))
    mu = float(input("Viscosity in Pa-s : "))    

    Re = rho*U*Dh/mu
    print("\nHydraulic diameter = "+str(Dh))
    print("Reynolds number based on hydraulic diameter = "+str(round(Re)))
    I = 0.16/Re**0.125

    print("\nI would like to know more about what creates turbulence in your flow.. \
            \n 1. The cross-section of the inlet determines turbulence \
            \n 2. My inlet velocity profile has a boundary layer thickness \
            \n 3. My domain has special features with a characterisitic length, e.g., perforations on a plate \
            ")

    L_choice = int(input("Enter your choice: "))
    
    if(L_choice==1):
        l = 0.07*Dh
    elif(L_choice==2):
        delta_99 = float(input("Enter the boundary layer thickness of your incoming flow in m : "))
        l = 0.4*delta_99
    elif(L_choice==3):
        l = float(input("Enter the characteristic length of your special feature in m : "))
    else:
        sys.exit("Wrong input!")

    print("\nFor your application, it is suggested to specify the turbulent intensity + length scale..")
    print("Intensity = "+str(I))
    print("Turbulent Length scale = "+str(l)+" [m]")
    k = 1.5*(U*I)**2
elif application==3:
    I = 0.01
    visc_rat = 1.0
    print("\nFor external aerodynamics or flow past bluff bodies, it is suggested to specify the turbulent intensity + viscosity ratio..")
    print("Intensity = "+str(I))
    print("Viscosity ratio = "+str(visc_rat))
elif application==4 or application==5:
    I = 0.1
    visc_rat = 10.0
    print("\nFor your high turbulent case, it is suggested to specify the turbulent intensity + viscosity ratio..")
    print("Intensity = "+str(I))
    print("Viscosity ratio = "+str(visc_rat))
else:
    print("If you are clueless on the turbulence leves in your flow, these values are a safer bet.")
    I = 0.05
    visc_rat = 5
    print("Intensity = "+str(I))
    print("Viscosity ratio = "+str(visc_rat))


print_turb = int(input("Do you want to print k, epsilon, and omega for reference ? 1 or 0 : "))

if print_turb==1:
   print("\nPriniting k, epsilon, and omega values just for reference.. Please do not use these values to set inlet BC")

   if application==1 or application==2:
      omega = math.pow(Cmu,-0.25)*math.sqrt(k)/l
   else:
      print("\nEnter the fluid properties...")
      rho = float(input("Density in kg/m3 : "))
      mu = float(input("Viscosity in Pa-s : "))    
      U = float(input("Enter reference velocity in m/s : "))
      k = 1.5*(U*I)**2
      omega = (rho*k/mu)/visc_rat
   
   epsilon = Cmu*k*omega
   print("k = "+str(k)+" [m2/s2]")
   print("omega = "+str(omega)+" [1/s]")
   print("epsilon = "+str(epsilon)+" [m2/s3]")
   

