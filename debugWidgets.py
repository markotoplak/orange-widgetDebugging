import os, sys, random, smtplib, re, time
from qt import *
import orange
import orngSignalManager

# options and settings
nrOfThingsToChange = 2000   # how many random clicks do we want to simulate
changeDatasetClicks = 100   # after how many random clicks do we want to change the dataset file
timeLimit = 30              # 30 minutes is the maximum time that we will spend in testing one schema

# possible command line parameters
sendMailText = "-sendmail"      # do we want to send an email to authors after finishing
verbosity1Text = "-verbose"     # do we want to see a bit more output from widgets - prints a line for every change in the widget (checkboxes, buttons, comboboxes, ...)
verbosity2Text = "-Verbose"     # do we want to see a lot of output from widgets - prints also passing and processing of signals


widgetDir = os.path.join(os.path.split(orange.__file__)[0], "OrangeWidgets")
sys.path.append(os.path.join(widgetDir, "Data"))
import OWFile       # we need to know the file widget so that we can remove it from the instance.widgets list

# get gui applications to try
guiAppPath = os.path.split(sys.argv[0])[0]
sys.path.append(guiAppPath)
os.chdir(guiAppPath)

sendMail = sendMailText in sys.argv[1:]     # do we want to send status mail or not
verbosity = 0
if verbosity1Text in sys.argv[1:]: verbosity = 1
if verbosity2Text in sys.argv[1:]: verbosity = 2

guiApps = sys.argv[1:]

#guiApps = ["visualizations.py"]
#verbosity = 2

for text in [sendMailText, verbosity1Text, verbosity2Text]:
    if text in guiApps:
        guiApps.remove(text)

if len(guiApps) == 0:
    for name in os.listdir(guiAppPath):
        if os.path.isfile(os.path.join(guiAppPath, name)) and os.path.splitext(name)[1] in [".py", ".pyw"] and name.lower() != "debugwidgets.py":
            guiApps.append(name)

# set datasets to try
datasets = []
datapath = os.path.join(guiAppPath, "datasets")
for name in os.listdir(datapath):
    if os.path.isfile(os.path.join(datapath, name)):
        datasets.append(os.path.join(datapath, name))

datasets.append("") # we add a blank dataset. this will never be selected and replaces the "Browse documentation data sets..."

widgetStatus = ""
nrOfFailed = 0

application = QApplication(sys.argv)
for guiApp in guiApps:
    guiName, guiExt = os.path.splitext(guiApp)
    if guiExt.lower() not in [".py", ".pyw"]:
        print "invalid file type for file", guiApp
        continue

    debugFileName = guiName + ".txt"
    f = open(debugFileName, "wt")
    f.close()

    widgetStatus += guiApp + " "
    startTime = time.time()
    initializationOK = 0

    f = open(guiApp)
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

    print guiApp
    try:
        module = __import__(guiName,  globals(), locals())
        module.application = application
        instance = module.GUIApplication(debugMode = 1, debugFileName = debugFileName, verbosity = verbosity)
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

        instance.hide()
        for widget in instance.widgets:
            widget.destroy()
        instance.destroy()
        print "finished...\n----------"
    else:
        print "initialization failed, therefore skipping...\n----------"

    # check output for exceptions
    f = open(debugFileName, "rt")
    content = f.read()
    f.close()
    if content.find("Unhandled exception") != -1:
        widgetStatus += " FAILED\n"
        nrOfFailed += 1


        # if we found somebody to bug then send him an email
        search = re.search("contact:(?P<imena>.*)\n", script)
        if (search) and sendMail == 1:
            fromaddr = "orange@fri.uni-lj.si"
            toaddrs = search.group("imena")
            toaddrs.replace(" ", ",")
            msg = "From: %s\r\nTo: %s\r\nSubject: Exception in widgets - %s script\r\n\r\n" % (fromaddr, toaddrs, guiApp) + content
            server = smtplib.SMTP('212.235.188.18', 25)
            #server.set_debuglevel(0)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
    elif time.time() - startTime >= timeLimit * 60:
        widgetStatus += " Time limit %d minutes exceeded. No exceptions were reported up to then.\n" % (timeLimit)
    else:
        widgetStatus += " OK\n"

if sendMail == 1:
    fromaddr = "orange@fri.uni-lj.si"
    toaddrs = "tomaz.curk@fri.uni-lj.si, gregor.leban@fri.uni-lj.si"
    msg = "From: %s\r\nTo: %s\r\nSubject: Widget test status. Number of failed: %d \r\n\r\n" % (fromaddr, toaddrs, nrOfFailed) + widgetStatus

    server = smtplib.SMTP('212.235.188.18', 25)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

application.setMainWidget(None)