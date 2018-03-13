import tkinter
import tkinter.simpledialog
import tkinter.ttk as ttk
import os

playerSR = 0
SR_FILE_NAME = "resources/sr"
AVG_FILE_NAME = "resources/avgs"

### OW SR COUNTER ###
# Author: Tiyst#2803 (EU,PC)
# Version: 0.1 (Like, day one alpha??)
# Contact: Sijie.wuu@gmail.com
#####################

##### To-do #####
#Slowly moving bar
#Progress bar color
#Enter == confirm (same as button)

#------------------------------------------------------------------------

def setSR(current, difference):
	global playerSR
	playerSR = current

	fileHandle = open(SR_FILE_NAME,"a")
	fileHandle.write("\n" + str(current) + " " + str(difference))
	fileHandle.close()

#------------------------------------------------------------------------

def getSR():
	global playerSR

	fileHandle = open(SR_FILE_NAME, "r")
	lines = fileHandle.readlines()
	fileHandle.close()

	avgs = open(AVG_FILE_NAME, "r").readline()
	avgs = avgs.split(" ")
	
	srParse = lines[-1].split(" ")
	srParse = srParse[0]

	playerSR = int(srParse)

	plus = 0
	minus = 0

	for line in lines:
		srParse = line.split(" ")
		srParse = float(srParse[1])
		if srParse > 0:
			plus += 1
		elif srParse < 0:
			minus += 1

	currLabel.configure(text=str(playerSR))
	avgGain.configure(text=round(float(avgs[0]),2))
	avgLose.configure(text=round(float(avgs[1]),2))


#------------------------------------------------------------------------

def refreshSrBar():

	srBar["value"] = playerSR

#------------------------------------------------------------------------

def calcAverages():
	fileHandle = open(SR_FILE_NAME, "r")
	lines = fileHandle.readlines()
	fileHandle.close()
	#numLines = sum(1 for line in lines)

	plus = 0
	minus = 0

	prevAvgPlus = 0
	prevAvgMinus = 0

	for line in lines:
		srParse = line.split(" ")
		srParse = float(srParse[1])
		if srParse > 0:
			plus += 1
		elif srParse < 0:
			minus += 1

	avgGainGames.configure(text=plus)
	avgLoseGames.configure(text=minus)

	if srParse > 0:
		calcAvgGain(srParse, plus)
	elif srParse < 0:
		calcAvgLose(srParse, minus)

#------------------------------------------------------------------------

def calcAvgGain(gain, lines):
	line = open(AVG_FILE_NAME).readline()
	line = line.split(" ")

	average = float(line[0]) * (lines - 1)
	average = (average + gain) / lines

	os.remove(AVG_FILE_NAME)
	writer = str(round(average,2)) + " " + str(line[1])

	fileHandle = open(AVG_FILE_NAME, "a")
	fileHandle.write(writer)
	fileHandle.close()


	avgGain.configure(text=round(float(average),2))

#------------------------------------------------------------------------

def calcAvgLose(lose, lines):
	#fileHandle = open(AVG_FILE_NAME, "r+")
	line = open(AVG_FILE_NAME).readline()
	line = line.split(" ")

	average = float(line[1]) * (lines - 1) 		#This is correct
	average = (average + lose) / lines

	os.remove(AVG_FILE_NAME)
	writer = str(line[0]) + " " + str(round(average,2))

	fileHandle = open(AVG_FILE_NAME, "a")
	fileHandle.write(writer)
	fileHandle.close()

	avgLose.configure(text=round(float(average),2))

#------------------------------------------------------------------------

def calcDifference(newsr):
	global playerSR

	diff = newsr - playerSR
	diffLabel.configure(text="Your SR difference is: " + str(diff))
	currLabel.configure(text=str(newsr))

	return diff

#------------------------------------------------------------------------

def calcSR():
	global playerSR

	ansValue = srInputBox.get()
	
	if ansValue.isdigit():					#//Checks if input is a number
		ansValue = int(ansValue)			#//if it is, cast it as int
	else:
		return

	if ansValue >= 0 and ansValue <= 5000 and ansValue != playerSR:
		difference = calcDifference(ansValue)
		setSR(ansValue, difference)
	else:
		diffLabel.configure(text="Please input a valid SR number.")
		return

	calcAverages()
	refreshSrBar()
	srInputBox.delete(0, "end")				#//Delete contents of entrybox

#------------------------------------------------------------------------


def initiateFiles():
	sr = tkinter.simpledialog.askstring("Your SR", "What's your SR Value now?", initialvalue = "SR")
	#gain = tkinter.simpledialog.askstring("SR gain", "How much SR do you think you approximaly get?", initialvalue = "SR gain")
	#loss = tkinter.simpledialog.askstring("SR loss", "How much SR do you think you approximaly lose?", initialvalue = "SR loss")

	fileHandle = open(SR_FILE_NAME,"a")
	fileHandle.write(str(sr) + " " + str(0))
	fileHandle.close()

	fileHandle = open(AVG_FILE_NAME,"a")
	#fileHandle.write(str(gain) + " -" + str(loss))
	fileHandle.write(str("0") + " " + str(0))
	fileHandle.close()

#--GUI-------------------------------------------------------------------

#create a GUI window.
root = tkinter.Tk()
root.title("Overwatch SR Counter")
root.iconbitmap("resources/owlogo.ico")
root.geometry("500x500")
root.resizable(0,0)

#Image files
headerImg = tkinter.PhotoImage(file="resources/owHeader.png")
headerPanel = tkinter.Label(root, image=headerImg)
avgsrGainImg = tkinter.PhotoImage(file="resources/avgsrgain.png")
avgsrGainPnl = tkinter.Label(root, image=avgsrGainImg)
avgsrLossImg = tkinter.PhotoImage(file="resources/avgsrloss.png")
avgsrLossPnl = tkinter.Label(root, image=avgsrLossImg)
currentSrImg = tkinter.PhotoImage(file="resources/currentSr.png")
currentSrPnl = tkinter.Label(root, image=currentSrImg)

#SR ProgressBar
s = ttk.Style()
#s.theme_use("clam")
#s.configure("red.Horizontal.TProgressbar", background="red")
srBar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length="300", variable="playerSR", maximum=5000)

#GUI elements
srInputBox = tkinter.Entry(root)
processButton = tkinter.Button(root, text="Calculate SR", command=calcSR, activebackground="lightblue")
diffLabel = tkinter.Label(root, text="", activebackground="lightblue")
currLabel = tkinter.Label(root, text="0", activebackground="lightblue")
avgGain = tkinter.Label(root, text="0", activebackground="lightblue")
avgLose = tkinter.Label(root, text="0", activebackground="lightblue")
avgGainGames = tkinter.Label(root, text="0", activebackground="lightblue")
avgLoseGames = tkinter.Label(root, text="0", activebackground="lightblue")

#Placing on canvas (WARNING: Shitcode inc)
headerPanel.place(relx=0.5, rely=0.15, anchor="center")
srBar.place(relx=0.5, rely=0.35, anchor="center")
srInputBox.place(relx=0.5, rely=0.42, anchor="center")
#srInputBox.bind("<Enter>", calcSR)							//Make this work!
processButton.place(relx=0.5, rely=0.5, anchor="center")
diffLabel.place(relx=0.5, rely=0.7, anchor="center")
currLabel.place(relx=0.5, rely=0.65, anchor="center")
avgsrGainPnl.place(relx=0.25, rely=0.75, anchor="center")
avgsrLossPnl.place(relx=0.75, rely=0.75, anchor="center")
currentSrPnl.place(relx=0.5, rely=0.6, anchor="center")
avgGain.place(relx=0.25, rely=0.8, anchor="center")
avgLose.place(relx=0.75, rely=0.8, anchor="center")
avgGainGames.place(relx=0.25, rely=0.85, anchor="center")
avgLoseGames.place(relx=0.75, rely=0.85, anchor="center")

#Init
if os.stat(SR_FILE_NAME).st_size == 0:
	initiateFiles()

getSR()
calcAverages()
refreshSrBar()


root.mainloop()