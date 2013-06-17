#!/usr/bin/python
#
# Pecube-average-exhumation-rate.py
#
# This script calculates average rates of rock exhumation for each sample
# location and thermochronometer system in Pecube using the predicted cooling
# ages in the Comparison.txt file and the Tt paths stored in the Ttpaths.txt
# file. The script should be run from the Pecube base directory.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial 3.0
# Unported License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative
# Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#
# dwhipp 06.13
#-------------------------------------------------------------------------------

#--- Say hello
print("#--- Pecube average exhumation rate calculator started ------------------------#")
print("")

#--- Import required libraries
import math,os,sys,numpy

#--- Check that required flags are present and OK
if (len(sys.argv) > 2):
    print("Error: Too many arguments")
    print("")
    print("Usage:")
    print("python Pecube_long-term_exhumation.py <Pecube run name>")
    print("")
    print("#--- Execution complete with error code 1. --------------------------------#")
    quit(1)
elif (len(sys.argv) > 1):
    model=sys.argv[1]
else:
    print("Error: Too few arguments")
    print("")
    print("Usage:")
    print("python Pecube_long-term_exhumation.py <Pecube run name>")
    print("")
    print("#--- Execution complete with error code 2. --------------------------------#")
    quit(2)

#--- Check for required input, output files
try:
    with open(os.path.join(model,"Comparison.txt")): pass
except IOError:
    print("Error: Cannot open file "+os.path.join(model,"Comparison.txt"))
    print("")
    print("Did you run this script from the Pecube base directory?")
    print("")
    print("#--- Execution complete with error code 3. --------------------------------#")
    quit(3)

try:
    with open("Ttpaths.txt") as file:
        file.close()
except IOError:
    print("Error: Cannot open file Ttpaths.txt")
    print("")
    print("Did you run this script from the Pecube base directory?")
    print("")
    print("#--- Execution complete with error code 4. --------------------------------#")
    quit(4)

try:
    with open("Exhumation_rate_summary.csv") as file:
        print("Error: File Exhumation_rate_summary.csv already exists")
        print("")
        print("Please delete or move the file and rerun this script")
        print("")
        print("#--- Execution complete with error code 5. --------------------------------#")
        file.close()
        quit(5)
except IOError:
    pass

#--- Open input files
fcompin = open(os.path.join(model,"Comparison.txt"),"r")
fTtin = open ("Ttpaths.txt","r")
fout = open("Exhumation_rate_summary.csv","w")

#--- Write output file header
fout.write('Latitude,Longitude,Elevation,AHe Observed,AHe Predicted,AHe '
           + 'exhumation rate,AFT Observed,AFT Predicted,AFT exhumation rate,'
           + 'ZHe Observed,ZHe Predicted,ZHe exhumation rate,ZFT Observed,ZFT '
           + 'Predicted,ZFT exhumation rate\n')

#--- Read in number of samples in Comparison.txt file
newln=fcompin.readline()
newln=str.split(newln)
fc_numsamp=int(newln[0])

#--- Create lists
lon=[]
lat=[]
elev=[]
ahe=[]
aft=[]
zhe=[]
zft=[]
pahe=[]
paft=[]
pzhe=[]
pzft=[]
ahedepth=[]
aftdepth=[]
zhedepth=[]
zftdepth=[]
eahe=[]
eaft=[]
ezhe=[]
ezft=[]

#--- Read first line of Ttpaths.txt
newln=fTtin.readline()
newln=str.split(newln)

#--- Loop over all samples and read their info
for sample in range(fc_numsamp):
    #--- Read from Comparison.txt
    print("Reading data for sample "+str(sample+1))
    newln=fcompin.readline()
    newln=str.split(newln)
    lon.append(float(newln[0]))
    lat.append(float(newln[1]))
    elev.append(float(newln[2]))
    # Append observed AHe age
    if (float(newln[4]) >= 0):
        ahe.append(float(newln[4]))
    else:
        ahe.append(-999.0)
    # Append predicted AHe age
    pahe.append(float(newln[5]))
    # Append AFT age
    if (float(newln[6]) >= 0):
        aft.append(float(newln[6]))
    else:
        aft.append(-999.0)
    # Append predicted AFT age
    paft.append(float(newln[7]))
    # Append ZHe age
    if (float(newln[8]) >= 0):
        zhe.append(float(newln[8]))
    else:
        zhe.append(-999.0)
    # Append predicted ZHe age
    pzhe.append(float(newln[9]))
    # Append ZFT age
    if (float(newln[10]) >= 0):
        zft.append(float(newln[10]))
    else:
        zft.append(-999.0)
    # Append predicted ZFT age
    pzft.append(float(newln[11]))

    #--- Read from Ttpaths.txt
    age=[]
    depth=[]
    while (len(newln) > 2):
        newln=fTtin.readline()
        newln=str.split(newln)
        if (len(newln) == 3):
            age.append(float(newln[0]))
            depth.append(float(newln[2]))

    #--- Interpolate cooling history to get depth of closure
    age=age[::-1]
    depth=depth[::-1]
    surfel=depth[0]
    depth[:] = [x - surfel for x in depth]
    if (ahe[sample] >= 0.0):
        ahedepth.append(numpy.interp(pahe[sample], age, depth))
    else:
        ahedepth.append(-999.000)
    if (aft[sample] >= 0.0):
        aftdepth.append(numpy.interp(paft[sample], age, depth))
    else:
        aftdepth.append(-999.000)
    if (zhe[sample] >= 0.0):
        zhedepth.append(numpy.interp(pzhe[sample], age, depth))
    else:
        zhedepth.append(-999.000)
    if (zft[sample] >= 0.0):
        zftdepth.append(numpy.interp(pzft[sample], age, depth))
    else:
        zftdepth.append(-999.000)
    
    #--- Calculate long-term average exhumation rate
    if (ahe[sample] >= 0.0 and abs(pahe[sample]) > 0.0):
        eahe.append(str(ahedepth[sample]/pahe[sample]))
    else:
        eahe.append('')
    if (aft[sample] >= 0.0 and abs(paft[sample]) > 0.0):
        eaft.append(str(aftdepth[sample]/paft[sample]))
    else:
        eaft.append('')
    if (zhe[sample] >= 0.0 and abs(pzhe[sample]) > 0.0):
        ezhe.append(str(zhedepth[sample]/pzhe[sample]))
    else:
        ezhe.append('')
    if (zft[sample] >= 0.0 and abs(pzft[sample]) > 0.0):
        ezft.append(str(zftdepth[sample]/pzft[sample]))
    else:
        ezft.append('')

    #--- Write output file
    fout.write(str(lat[sample])+','+str(lon[sample])+','+str(elev[sample])+','
               +str(ahe[sample])+','+str(pahe[sample])+','+eahe[sample]+','
               +str(aft[sample])+','+str(paft[sample])+','+eaft[sample]+','
               +str(zhe[sample])+','+str(pzhe[sample])+','+ezhe[sample]+','
               +str(zft[sample])+','+str(pzft[sample])+','+ezft[sample]+','+'\n')

#--- Close files
fcompin.close()
fTtin.close()
fout.close()

#--- Say goodbye
print("")
print("#--- Execution complete. Have a nice day. -------------------------------------#")
quit(0)
