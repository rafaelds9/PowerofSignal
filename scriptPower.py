import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat
from scipy import integrate
import pandas as pd


# Function to select the points of interest in the ECG curve
xcoord = []	
def onclick(event):
	#print ("\nSelected point: %f"%(event.xdata)) # Shows the time value of the clicked point
	xcoord.append(round(event.xdata)) # Appends the points to an array



# Constants related to the signal
amplification = 200

# Loading signals
normal = loadmat('Signals/NormalSinusRhythm/100m (0).mat')
atrialFib = loadmat('Signals/AtrialFibrillation/201m (0).mat')


normal = normal['val'][0]/amplification
atrialFib = atrialFib['val'][0]/amplification


# Plotting the signals to select the points that define the signal period
for it in range(2):
    fig = plt.figure(figsize=(19.2,9.91)) #19.2,9.91
    if it == 0:
        plt.plot(normal)
    else:
        xcoord = []
        plt.plot(atrialFib)
    plt.xlim(0,1000)
    plt.grid()
    cid = fig.canvas.mpl_connect('button_press_event', onclick) # Allowing to store the time values of the clicked points
    plt.show()
    fig.canvas.mpl_disconnect(cid)	# After the points selection the function to store them will finish
    if it == 0:
        pointsECG = np.asarray(xcoord, dtype = int)
    else:
        pointsECG = np.vstack([pointsECG,np.asarray(xcoord, dtype = int)])

#print(pointsECG)



#Calculating power and plotting the signals for the comparative

fig = plt.figure(figsize=(19.2,9.91)) #19.2,9.91
plt.rcParams.update({'font.size': 16})


for it in range(2):

    #Calculating
    if it == 0:
        print("\n\nNormal:")
        sqrAbsSignal = np.power(np.abs(normal[pointsECG[it][0]:pointsECG[it][1]+1]), 2) 
    else:
        print("Atrial Fibrillation: ")
        sqrAbsSignal = np.power(np.abs(atrialFib[pointsECG[it][0]:pointsECG[it][1]+1]), 2) 

    power = round((1/(pointsECG[it][1]-pointsECG[it][0]+1))*np.sum(sqrAbsSignal),2)
    print("\tPower: ", power, " (mV)²\n")
    #

    #Plotting    
    ax = plt.subplot(1,2,it+1)
    if it == 0:
        ax.set_title('Normal')
        plt.plot(normal)
    else:
        ax.set_title('Fibrilação Atrial')
        plt.plot(atrialFib)
   
    auxPrint = "Potência = " + str(power) + "mV²"
    plt.text(pointsECG[it][0]+5, 6, auxPrint, fontsize = 11)

    ax.set_xlabel("Amostra [n]")
    ax.set_ylabel("Tensão (mV)")
    

    ax.axvline(x=pointsECG[it][0], c = "r")
    ax.axvline(x=pointsECG[it][1], c = "r")



    plt.xlim(0,1000)
    plt.ylim(4.5, 6.5)
    
    plt.grid()

plt.show()
