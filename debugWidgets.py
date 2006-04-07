import os, sys, random, smtplib, re
from qt import *
import orange
import orngSignalManager

# options and settings
nrOfThingsToChange = 2000    # how many random clicks do we want to simulate
changeDatasetClicks = 100   # after how many random clicks do we want to change the dataset file


widgetDir = os.path.join(os.path.split(orange.__file__)[0], "OrangeWidgets")
sys.path.append(os.path.join(widgetDir, "Data"))
import OWFile       # we need to know the file widget so that we can remove it from the instance.widgets list

# get gui applications to try
guiAppPath = os.path.split(sys.argv[0])[0]
sys.path.append(guiAppPath)
os.chdir(guiAppPath)

guiApps = []
if len(sys.argv) > 1:
    guiApps = sys.argv[1:]
else:
    for name in os.listdir(guiAppPath):
        if os.path.isfile(os.path.join(guiAppPath, name)) and os.path.splitext(name)[1] in [".py", ".pyw"]:
            guiApps.append(name)

if "debugWidgets.py" in guiApps:
    guiApps.remove("debugWidgets.py")       # ignore this file if in the same directory

# set datasets to try
datasets = []
datapath = os.path.join(guiAppPath, "datasets")
for name in os.listdir(datapath):
    if os.path.isfile(os.path.join(datapath, name)):
        datasets.append(os.path.join(datapath, name))

datasets.append("") # we add a blank dataset. this will never be selected and replaces the "Browse documentation data sets..."

widgetStatus = ""; nrOfFailed = 0

application = QApplication(sys.argv)        
for guiApp in guiApps:
    guiName, guiExt = os.path.splitext(guiApp)
    debugFileName = guiName + ".txt"
    f = open(debugFileName, "wt"); f.close()

    widgetStatus += guiApp + " "

    initializationOK = 0
    try:
        module = __import__(guiName,  globals(), locals())
        module.application = application
        instance = module.GUIApplication(debugMode = 1, debugFileName = debugFileName, verbosity = 0)
        application.setMainWidget(instance)
        instance.show()
        initializationOK = 1
    except:
        type, val, traceback = sys.exc_info()
        sys.excepthook(type, val, traceback)
        #widgetStatus += " FAILED\n"
        #nrOfFailed += 1

    if initializationOK:
        # remove the file widgets
        fileWidgets = []
        for widget in instance.widgets[::-1]:
            if isinstance(widget, OWFile.OWSubFile):
                instance.widgets.remove(widget)
                fileWidgets.append(widget)
                widget.recentFiles = datasets
                widget.selectFile(0)
        
        random.seed(0)      # for each gui application reset the random generator

        # randomly change gui elements in widgets
        for i in range(nrOfThingsToChange):
            application.processEvents()
            
            if i%changeDatasetClicks == 0:
                datasetIndex = random.randint(0, len(datasets)-2)
                datasetName =  datasets[datasetIndex]
                fileWidgets[random.randint(0, len(fileWidgets)-1)].selectFile(datasetIndex)
                instance.signalManager.addEvent("Setting data set: %s" % (str(os.path.split(datasetName)[1])))
            else:
                try:
                    widget = instance.widgets[random.randint(0, len(instance.widgets)-1)]
                    widget.randomlyChangeSettings()
                    application.processEvents()
                except:
                    instance.signalManager.addEvent("-----------------------------------")
                    type, val, traceback = sys.exc_info()
                    sys.excepthook(type, val, traceback)
                    instance.signalManager.addEvent("State of widget %s: %s" % (widget.__class__.__name__, widget.getSettings()))
                    instance.signalManager.addEvent("-----------------------------------")

        instance.signalManager.addEvent("Test finished")
        instance.hide()
        for widget in instance.widgets:
            widget.destroy()
        instance.destroy()

    # check output for exceptions
    f = open(debugFileName, "rt")
    content = f.read()
    f.close()
    if content.find("Unhandled exception") != -1:
        widgetStatus += " FAILED\n"
        nrOfFailed += 1
        file = open(guiApp)
        script = file.read()
        file.close()

        # if we found somebody to bug then send him an email
        search = re.search("contact:(?P<imena>.*)\n", script)
        if (search):
            fromaddr = "orange@fri.uni-lj.si"
            toaddrs = search.group("imena").split(",")
            msg = "From: %s\r\nTo: %s\r\nSubject: Exception in widgets - %s script\r\n\r\n" % (fromaddr, ", ".join(toaddrs), guiApp) + content
            server = smtplib.SMTP('postar.fri.uni-lj.si', 25)
            #server.set_debuglevel(0)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
    else:
        widgetStatus += " OK\n"

fromaddr = "orange@fri.uni-lj.si"
toaddrs = ["tomaz.curk@fri.uni-lj.si", "gregor.leban@fri.uni-lj.si"]
msg = "From: %s\r\nTo: %s\r\nSubject: Widget test status. Number of failed: %d \r\n\r\n" % (fromaddr, ", ".join(toaddrs), nrOfFailed) + widgetStatus

server = smtplib.SMTP('postar.fri.uni-lj.si', 25)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
application.setMainWidget(None)