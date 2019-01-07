# By Tom Baker

import datetime
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
import urllib
import webbrowser
import random

locationNames = ["Sensor 1", "Sensor 2", "Sensor 3"]
dataLocation = "http://localhost/data"
textFont = ("Helvetica", 15, "bold")
tempLimits = {"low" : 18.0, "high" : 30.0}
RHLimits = {"low" : 30.0, "high" : 70.0}

def getRandomData(): # For testing purposes.
    rawdata = [random.uniform(29.0, 31.0) for _ in range(10)]
    data = []
    for d in rawdata:
        data.append("{0:.1f}".format(d))
    return data

def openMap():
    webbrowser.open("http://localhost/map")

def openSPX():
    webbrowser.open("https://localhost/spx")


class Application(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.winfo_toplevel().title("RH+T")
        master.resizable(width=False, height=False)

        # Variables. locationInfo is a nested dictionary.
        self.timestamp = tk.StringVar()
        self.locationInfo = {}
        for name in locationNames:
            d = {"RH" : tk.StringVar(),
                 "T" : tk.StringVar(),
                 "RHLabel" : tk.Label(),
                 "TLabel" : tk.Label()
                 }
            self.locationInfo[name] = d
            
        # GUI Components. Builds a row for each location in locationInfo dict.
        for location in self.locationInfo:
            frame = tk.LabelFrame(root)
            frame.pack(fill="both")
            tk.Label(frame, text=location.ljust(12), width=9, font = textFont).grid(row=0, column=0, columnspan=25, sticky='E')
            tk.Label(frame, text="RH: ", borderwidth=2, font = textFont).grid(row=0, column=25, columnspan=10, sticky='E')
            self.locationInfo[location]["RHLabel"] = tk.Label(frame, textvariable=self.locationInfo[location]["RH"], borderwidth=2, relief="sunken", font = textFont, bg="gray99")
            self.locationInfo[location]["RHLabel"].grid(row=0, column=35, columnspan=10, sticky='E')
            tk.Label(frame, text="T: ", borderwidth=2, font = textFont).grid(row=0, column=45, columnspan=10, sticky='E')
            self.locationInfo[location]["TLabel"] = tk.Label(frame, textvariable=self.locationInfo[location]["T"], borderwidth=2, relief="sunken", font = textFont, bg="gray99")
            self.locationInfo[location]["TLabel"].grid(row=0, column=55, columnspan=10, sticky='E')

            for column in range(frame.grid_size()[0]):
                frame.grid_columnconfigure(column, weight=1)

        frame = tk.Frame(root)
        frame.pack()
        tk.Button(frame, text="Map", command=openMap).grid(row=0, column=0, columnspan=2)
        tk.Button(frame, text="SPX", command=openSPX).grid(row=0, column=2, columnspan=2)
        tk.Label(frame, textvariable=self.timestamp).grid(row=0, column=4, columnspan=6)

    def update(self):
        try:
            with urlopen(dataLocation) as response:
                data = str(response.read().decode('utf-8')).strip('\n\r').split(',')[1:]
##            data = getRandomData()
                
            for location in self.locationInfo:
                if (tempLimits["low"] + 1) <= float(data[0]) <= (tempLimits["high"] - 1):
                    self.locationInfo[location]["TLabel"].config(bg="gray99")
                elif tempLimits["low"] <= float(data[0]) <= tempLimits["high"]:
                    self.locationInfo[location]["TLabel"].config(bg="yellow")
                else:
                    self.locationInfo[location]["TLabel"].config(bg="red")
                if (RHLimits["low"] + 0.5) <= float(data[1]) <= (RHLimits["high"] - 0.5):
                    self.locationInfo[location]["RHLabel"].config(bg="gray99")
                elif RHLimits["low"] <= float(data[1]) <= RHLimits["high"]:
                    self.locationInfo[location]["RHLabel"].config(bg="yellow")
                else:
                    self.locationInfo[location]["RHLabel"].config(bg="red") 
                self.locationInfo[location]["T"].set(data.pop(0) + "°C")
                self.locationInfo[location]["RH"].set(data.pop(0) + "%")

            self.timestamp.set("Last updated at " + datetime.datetime.now().strftime('%H:%M on %m/%d/%y'))

        except IndexError as e:
            self.timestamp.set("IndexError:" + str(e))

        except urllib.error.URLError as e:
            self.timestamp.set("Cannot access data:" + str(e))

        except:
            self.timestamp.set("Unhandled Exception!")

        self.after(120000, self.update)


root = tk.Tk()
app = Application(root)
root.after(100, app.update)
root.mainloop()
