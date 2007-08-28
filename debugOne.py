import os, sys, random, re, time
from qt import *
import orange, orngSignalManager, orngRegistry

changeDatasetClicks = 100   # after how many random clicks do we want to change the dataset file
debugDir = os.path.split(os.path.abspath(__file__))[0]
#debugDir = r"E:\Development\Orange\WidgetDebugging"
#sys.argv = ['debugOne.py', 'data selection.py', '2000', '0', '30']

os.chdir(debugDir)

guiName = " ".join(sys.argv[1:-3])
    
nrOfThingsToChange = int(sys.argv[-3])
verbosity = int(sys.argv[-2])
timeLimit = int(sys.argv[-1])

orngRegistry.addWidgetDirectories()
import OWFile       # we need to know the file widget so that we can remove it from the instance.widgets list

# set datasets to try
datasets = []
datapath = os.path.join(debugDir, "datasets")
for name in os.listdir(datapath):
    if os.path.isfile(os.path.join(datapath, name)):
        datasets.append(os.path.join(datapath, name))

datasets.append("") # we add a blank dataset. this will never be selected and replaces the "Browse documentation data sets..."

debugFileName = os.path.splitext(guiName)[0] + ".txt"
f = open(debugFileName, "wt")
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

search = re.search("ignore:(?P<types>.*)\n", script)      # which datasets should be ignored
if search:
    ignoreDatasets = [val.strip().lower() for val in search.group("types").split(",")]
else:
    ignoreDatasets = []


try:
    application = QApplication(sys.argv[1:])
    module = __import__(os.path.splitext(os.path.basename(guiName))[0])
    module.application = application
    instance = module.GUIApplication(debugMode = 1, debugFileName = debugFileName, verbosity = verbosity)
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
                    datasetIndex = random.randint(0, len(datasets)-2)
                    datasetName =  datasets[datasetIndex]
                    data = orange.ExampleTable(datasetName)
                    if "class" in validDatasets and "noclass" in validDatasets: validChange = 1
                    elif "class" in validDatasets and data.domain.classVar: validChange = 1
                    elif "noclass" in validDatasets and data.domain.classVar == None: validChange = 1
                    if os.path.split(datasetName)[1].lower() in ignoreDatasets: validChange = 0

                instance.signalManager.addEvent("---- Setting data set: %s ----" % (str(os.path.split(datasetName)[1])), eventVerbosity = 0)
                fileWidgets[random.randint(0, len(fileWidgets)-1)].selectFile(datasetIndex)
            else:
                widget = instance.widgets[random.randint(0, len(instance.widgets)-1)]
                widget.randomlyChangeSettings(verbosity)
                application.processEvents()
        except:
            type, val, traceback = sys.exc_info()
            sys.excepthook(type, val, traceback)  # print the exception

    instance.signalManager.addEvent("Test finished", eventVerbosity = 0)
    instance.signalManager.closeDebugFile()

