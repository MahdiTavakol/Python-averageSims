#!/usr/bin/env python3
import numpy as np
import statistics
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import csv
import os


#####################################################################################################

def smooth(y, box_pts):
	box = np.ones(box_pts)/box_pts
	y_smooth = np.convolve(y, box, mode='same')
	return y_smooth


#####################################################################################################
print("Reading data") 

num_data = 5050

folders = ["1-Series1","2-Series2","3-Series3"]
num_sims = len(folders)

epsilon = np.empty(num_data)
sigma = np.empty((num_data,num_sims))




for i, folder in enumerate(folders):
	print(f"\tReading folder {folder}")
	
	sigma_i = []
	
	fileName = folder + "/5-Press/dump/deformation.txt"
	
	with open(fileName,"r") as csvfile:
		reader = csv.reader(csvfile,delimiter=" ")
		next(reader)
		for j, row in enumerate(reader):
			if (i == 0):
				epsilon[j] = float(row[2])
			sigma_i.append(float(row[5]))
		sigma_i = np.array(sigma_i)
	

	sigma[:,i] = sigma_i


#####################################################################################################	
print("Averaging the data")
sigma_avg = np.mean(sigma,axis=1)
sigma_err = np.std(sigma,axis=1)
#sigma_err = [x/sqrt(num_data) for x in sigma_err]


#####################################################################################################
print("Writing the data")
output = "Stress-strain-summary.csv"
with open(output,"w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(["Strain","Stress-1","Stress-2","Stress-3","Stress-avg","Stress-error"])
	for i in range(num_data):
		writer.writerow([epsilon[i],sigma[i,0],sigma[i,1],sigma[i,2],sigma_avg[i],sigma_err[i]])
		
		
#####################################################################################################
print("Plotting the data")



fontsize = 10
outputwidth = 7
outputheight = 3.9375

cmap = plt.get_cmap('rainbow')  # You can choose any colormap you like
colors = [cmap(i / num_sims) for i in range(num_sims)]
colors = ["#DA291C","#56A8CB","#53A567"]

fig = plt.figure()

#####################################################################################################
print("\tPlotting the individual simulations")
ax = fig.add_subplot(121)
plt.sca(ax)

for i in range(num_sims):
	print(f"\t\tPlotting the {folders[i]}")
	plt.plot(epsilon,sigma[:,i],color=colors[i],label=f"{folders[i]}")

	
plt.xlabel("Strain",fontsize=fontsize)
plt.ylabel("Stress (GPa)",fontsize=fontsize)
plt.xlim(-0.4,0)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.legend(fontsize='small')

xtick = ax.get_xticks()
ax.set_xticks(xtick[:-1])
#####################################################################################################
print("\tPlotting the average")
ax2 = fig.add_subplot(122)
plt.sca(ax2)

print("\t\tSmoothing the average and error")
sigma_avg_smooth = smooth(sigma_avg,9)
sigma_err_smooth = smooth(sigma_err,9)

sigma_max = [a+e for a,e in zip(sigma_avg_smooth,sigma_err_smooth)]
sigma_min = [a-e for a,e in zip(sigma_avg_smooth,sigma_err_smooth)]


#plt.errorbar(epsilon,sigma_avg_smooth,yerr=sigma_err_smooth,color='black')
plt.plot(epsilon,sigma_avg_smooth,color='black')
plt.fill_between(epsilon,sigma_min,sigma_max,color='black',alpha=0.2)



# adjusting the min and max
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()
plt.ylim(ymin,ymax)


# Calculating the secant modulus
index04 = 0
strain04 = 0
for i in range(len(epsilon)):
	if (epsilon[i] <= -0.04):
		index04 = i
		strain04 = epsilon[i]
		break
E = sigma_avg_smooth[index04]/strain04

# The text box
y_txt = ymax-0.1*(ymax-ymin)
x_txt = xmax-0.25*(xmax-xmin)
props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='navy', linewidth=2)
textbox = ax2.text(x_txt, y_txt,f"E={E:.2f}(GPa)", fontsize=fontsize, bbox=props, verticalalignment='top', horizontalalignment='center')


plt.xlabel("Strain",fontsize=fontsize)
plt.yticks([])
plt.xlim(-0.4,0)
plt.xticks(fontsize=fontsize)
ax2.set_yticklabels([])


#####################################################################################################
print("Adjusting the plot")

fig.tight_layout()
plt.subplots_adjust(top=0.95,bottom=0.15,left=0.1,right=0.95,hspace=0.1,wspace=0.)

#######################################################################################################
print("\tSaving the plot")
fileName = "Stress-Strain-Summary"
fig.set_size_inches(outputwidth,outputheight)
fig.savefig(fileName+".svg",dpi=1200)


#######################################################################################################
print("All done!")


		
		
