import orngOrangeFoldersQt4
import os, sys, random, re, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import orange, orngSignalManager, orngRegistry
import orngDebugging

changeDatasetClicks = 100   # after how many random clicks do we want to change the dataset file
debugDir = os.path.split(os.path.abspath(__file__))[0]
#debugDir = r"E:\Development\Orange-Qt4\WidgetDebugging"
#sys.argv = ['debugOne.py', 'visualizations.py', '20000', '0', '30']

os.chdir(debugDir)

guiName = " ".join(sys.argv[1:-3])
    
nrOfThingsToChange = int(sys.argv[-3])
verbosity = int(sys.argv[-2])
timeLimit = int(sys.argv[-1])

orngDebugging.orngDebuggingEnabled = 1       # set debugging variable to 1 and prevent execution of code that requires user's intervention
orngDebugging.orngDebuggingFileName = os.path.splitext(guiName)[0] + ".txt"
orngDebugging.orngVerbosity = verbosity


import OWFile       # we need to know the file widget so that we can remove it from the instance.widgets list

# set datasets to try
datasets = []
datapath = os.path.join(debugDir, "datasets")
for name in os.listdir(datapath):
    if os.path.isfile(os.path.join(datapath, name)):
        datasets.append(os.path.join(datapath, name))

datasets.append("(none)") # we add a blank dataset. This will be to test the none signal

f = open(orngDebugging.orngDebuggingFileName, "wt")
f.close()

startTime = time.time()
initializationOK = 0

f = open(guiName)
script = f.read()
f.close()
search = re.search("datasets:(?P<types>.*)\n", script)      # which datasets are valid for this test - those with class, those without, or both
if search:
    validDatasets = [val.strip().lower() for val in search.group("types").split(",")]
else:
    validDatasets = ["class", "noclass"]

# remove datasets which should be ignored
search = re.search("ignore:(?P<names>.*)\n", script)      
if search:
    invalidNames = [val.strip().lower() for val in search.group("names").split(",")]
    for name in datasets[-1::-1]:
        if os.path.split(name)[1].lower() in invalidNames:
            datasets.remove(name)
            print "ignoring dataset", os.path.split(name)[1]


# do we have specified which datasets only to use?
search = re.search("useonly:(?P<names>.*)\n", script)      # which datasets ONLY should be used in testing
if search:
    validNames = [val.strip().lower() for val in search.group("names").split(",")]
    for name in datasets[-1::-1]:
        if os.path.split(name)[1].lower() not in validNames:
            datasets.remove(name)
            print "ignoring dataset", os.path.split(name)[1]

try:
    application = QApplication(sys.argv[1:])
    module = __import__(os.path.splitext(os.path.basename(guiName))[0])
    module.application = application
    instance = module.GUIApplication()
    instance.show()
    initializationOK = 1
except:
    type, val, traceback = sys.exc_info()
    sys.excepthook(type, val, traceback)

if initializationOK:
    # remove the file widgets
    fileWidgets = []
    for widget in instance.widgets[::-1]:
        if isinstance(widget, OWFile.OWFile):
            instance.widgets.remove(widget)
            fileWidgets.append(widget)
            widget.recentFiles = datasets
            #widget.selectFile(0)
    random.seed(0)      # for each gui application reset the random generator

    # randomly change gui elements in widgets
    for i in range(nrOfThingsToChange):
        application.processEvents()

        if time.time() - startTime >= timeLimit * 60:
            instance.signalManager.addEvent("Time limit (%d min) exceeded" % (timeLimit), eventVerbosity = 0)
            break
        try:
            if i % changeDatasetClicks == 0:
                validChange = 0
                while validChange == 0:
                    datasetName =  datasets[random.randint(0, len(datasets)-1)]
                    if datasetName != "(none)":
                        data = orange.ExampleTable(datasetName)
                        if "class" in validDatasets and "noclass" in validDatasets: validChange = 1
                        elif "class" in validDatasets and data.domain.classVar: validChange = 1
                        elif "noclass" in validDatasets and data.domain.classVar == None: validChange = 1
                    else:
                        validChange = 1

                instance.signalManager.addEvent("---- Setting data set: %s ----" % (str(os.path.split(datasetName)[1])), eventVerbosity = 0)
                fileWidget = fileWidgets[random.randint(0, len(fileWidgets)-1)]
                fileWidget.openFile(datasetName, 0, fileWidget.symbolDK, fileWidget.symbolDC)
            else:
                widget = instance.widgets[random.randint(0, len(instance.widgets)-1)]
                
                if len(widget._guiElements) == 0: continue

                try:
                    newValue = ""
                    callback = None
        
                    #index = random.randint(0, len(widget._guiElements)-1)
                    index = random.randint(0, len(widget._guiElements))
                    if index == len(widget._guiElements):
                        elementType = "signalChange"
                        guiElement = None
                    else:
                        elementType, guiElement = widget._guiElements[index][0], widget._guiElements[index][1]
                        if not guiElement.isEnabled(): continue
        
                    if elementType == "signalChange":
                        if len(widget.outputs) > 0:
                            output = widget.outputs[random.randint(0, len(widget.outputs)-1)][0]
                            widget.send(output, None)
                            newValue = "Sending None to output signal " + output
                    elif elementType == "qwtPlot":
                        guiElement.randomChange()
                        newValue = "Random change in qwtPlot"
                    elif elementType == "checkBox":
                        elementType, guiElement, value, callback = widget._guiElements[index]
                        newValue = "Changing checkbox %s to %s" % (value, not widget.getdeepattr(value))
                        setattr(widget, value, not widget.getdeepattr(value))
                    elif elementType == "button":
                        elementType, guiElement, callback = widget._guiElements[index]
                        if guiElement.isCheckable():
                            newValue = "Clicking button %s. State is %d" % (str(guiElement.text()).strip(), not guiElement.isChecked())
                            guiElement.setChecked(not guiElement.isChecked())
                        else:
                            newValue = "Pressed button %s" % (str(guiElement.text()).strip())
                    elif elementType == "listBox":
                        elementType, guiElement, value, callback = widget._guiElements[index]
                        if guiElement.count():
                            itemIndex = random.randint(0, guiElement.count()-1)
                            newValue = "Listbox %s. Changed selection of item %d to %s" % (value, itemIndex, not guiElement.item(itemIndex).isSelected())
                            guiElement.item(itemIndex).setSelected(not guiElement.item(itemIndex).isSelected())
                        else:
                            callback = None
                    elif elementType == "radioButtonsInBox":
                        elementType, guiElement, value, callback = widget._guiElements[index]
                        radioIndex = random.randint(0, len(guiElement.buttons)-1)
                        if guiElement.buttons[radioIndex].isEnabled():
                            newValue = "Set radio button %s to index %d" % (value, radioIndex)
                            setattr(widget, value, radioIndex)
                        else:
                            callback = None
                    elif elementType == "radioButton":
                        elementType, guiElement, value, callback = widget._guiElements[index]
                        newValue = "Set radio button %s to %d" % (value, not widget.getdeepattr(value))
                        setattr(widget, value, not widget.getdeepattr(value))
                    elif elementType in ["hSlider", "qwtHSlider", "spin"]:
                        elementType, guiElement, value, min, max, step, callback = widget._guiElements[index]
                        currentValue = widget.getdeepattr(value)
                        if currentValue == min:   setattr(widget, value, currentValue+step)
                        elif currentValue == max: setattr(widget, value, currentValue-step)
                        else:                     setattr(widget, value, currentValue + [-step,step][random.randint(0,1)])
                        newValue = "Changed value of %s to %f" % (value, widget.getdeepattr(value))
                    elif elementType == "comboBox":
                        elementType, guiElement, value, sendSelectedValue, valueType, callback = widget._guiElements[index]
                        if guiElement.count():
                            pos = random.randint(0, guiElement.count()-1)
                            newValue = "Changed value of combo %s to %s" % (value, str(guiElement.itemText(pos)))
                            if sendSelectedValue:
                                setattr(widget, value, valueType(str(guiElement.itemText(pos))))
                            else:
                                setattr(widget, value, pos)
                        else:
                            callback = None
                    if newValue != "":
                        widget.printEvent("Widget %s. %s" % (str(widget.windowTitle()), newValue), eventVerbosity = 1)
                    if callback:
                        if type(callback) == list:
                            for c in callback:
                                c()
                        else:
                            callback()
                except:
                    excType, value, tracebackInfo = sys.exc_info()
                    if not widget.signalManager.exceptionSeen(type, value, tracebackInfo):
                        sys.stderr.write("------------------\n")
                        if newValue != "":
                            sys.stderr.write("Widget %s. %s\n" % (str(widget.windowTitle()), newValue))
                        sys.excepthook(excType, value, tracebackInfo)  # print the exception
                        sys.stderr.write("Widget settings are:\n")
                        for i, setting in enumerate(getattr(widget, "settingsList", [])):
                            if setting in ["widgetWidth", "widgetHeight", "widgetXPosition", "widgetYPosition", "widgetShown"]:
                                continue
                            sys.stderr.write("%30s: %7s\n" % (setting, str(widget.getdeepattr(setting))))
                        
                application.processEvents()
        except:
            type, val, traceback = sys.exc_info()
            sys.excepthook(type, val, traceback)  # print the exception

    instance.signalManager.addEvent("Test finished", eventVerbosity = 0)
    instance.signalManager.closeDebugFile()

