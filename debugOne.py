import os, sys, random, re, time
from qt import *
import orange, orngSignalManager, orngRegistry
import orngDebugging

changeDatasetClicks = 100   # after how many random clicks do we want to change the dataset file
debugDir = os.path.split(os.path.abspath(__file__))[0]
#debugDir = r"E:\Development\Orange\WidgetDebugging"
#sys.argv = ['debugOne.py', 'visualizations.py', '2000', '0', '30']
#sys.argv = ['debugOne.py', 'associate.py', '2000', '0', '30']

os.chdir(debugDir)

guiName = " ".join(sys.argv[1:-3])
nrOfThingsToChange = int(sys.argv[-3])
verbosity = int(sys.argv[-2])
timeLimit = int(sys.argv[-1])

orngDebugging.orngDebuggingEnabled = 1       # set debugging variable to 1 and prevent execution of code that requires user's intervention
orngDebugging.orngDebuggingFileName = os.path.splitext(guiName)[0] + ".txt"
orngDebugging.orngVerbosity = verbosity


orngRegistry.addWidgetDirectories()
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
    application.setMainWidget(instance)
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
                widget.randomlyChangeSettings(verbosity)
                application.processEvents()
        except:
            type, val, traceback = sys.exc_info()
            sys.excepthook(type, val, traceback)  # print the exception

    instance.signalManager.addEvent("Test finished", eventVerbosity = 0)
    instance.signalManager.closeDebugFile()

