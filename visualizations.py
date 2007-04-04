# contact: gregor.leban@fri.uni-lj.si
# datasets: class, noclass
# ignore: titanic.tab

import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWDataSampler import *
from OWDataDomain import *
from OWScatterPlot import *
from OWLinProj import *
from OWRadviz import *
from OWPolyviz import *
from OWParallelCoordinates import *
from OWMosaicDisplay import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt visualizations")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.verbosity = verbosity

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owScatterplot = OWScatterPlot(signalManager = self.signalManager)
        self.owLinear_Projection = OWLinProj(signalManager = self.signalManager)
        self.owRadviz = OWRadviz(signalManager = self.signalManager)
        self.owPolyviz = OWPolyviz(signalManager = self.signalManager)
        self.owParallel_coordinates = OWParallelCoordinates(signalManager = self.signalManager)
        self.owMosaic_Display = OWMosaicDisplay(signalManager = self.signalManager)

        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owSelect_Attributes.setEventHandler(self.eventHandler)
        self.owSelect_Attributes.setProgressBarHandler(self.progressHandler)
        self.owScatterplot.setEventHandler(self.eventHandler)
        self.owScatterplot.setProgressBarHandler(self.progressHandler)
        self.owLinear_Projection.setEventHandler(self.eventHandler)
        self.owLinear_Projection.setProgressBarHandler(self.progressHandler)
        self.owRadviz.setEventHandler(self.eventHandler)
        self.owRadviz.setProgressBarHandler(self.progressHandler)
        self.owPolyviz.setEventHandler(self.eventHandler)
        self.owPolyviz.setProgressBarHandler(self.progressHandler)
        self.owParallel_coordinates.setEventHandler(self.eventHandler)
        self.owParallel_coordinates.setProgressBarHandler(self.progressHandler)
        self.owMosaic_Display.setEventHandler(self.eventHandler)
        self.owMosaic_Display.setProgressBarHandler(self.progressHandler)

        #list of widget instances
        vizranks = [self.owScatterplot.vizrank, self.owLinear_Projection.vizrank, self.owRadviz.vizrank]        # don't add polyviz's vizrank, because it doesn't use time limit!!
        for w in vizranks:
            w.useTimeLimit = 1
            w.useProjectionLimit = 1
            w.timeLimit = 0.3
            w.optimizeTimeLimit = 0.3
            w.projectionLimit = 20
            w.optimizeProjectionLimit = 20
            w.attributeCount = 6
            w.setEventHandler(self.eventHandler)

        self.widgets = [self.owFile, self.owData_Sampler, self.owSelect_Attributes, self.owScatterplot,
                        self.owLinear_Projection, self.owRadviz, self.owPolyviz, self.owParallel_coordinates,
                        self.owMosaic_Display, ]
        self.widgets += vizranks

        # set widget captions
        self.owFile.setCaptionTitle('Qt File')
        self.owData_Sampler.setCaptionTitle('Qt Data Sampler')
        self.owSelect_Attributes.setCaptionTitle('Qt Select Attributes')
        self.owScatterplot.setCaptionTitle('Qt Scatterplot')
        self.owLinear_Projection.setCaptionTitle('Qt Linear Projection')
        self.owRadviz.setCaptionTitle('Qt Radviz')
        self.owPolyviz.setCaptionTitle('Qt Polyviz')
        self.owParallel_coordinates.setCaptionTitle('Qt Parallel coordinates')
        self.owMosaic_Display.setCaptionTitle('Qt Mosaic Display')

        # set icons
        self.owFile.setWidgetIcon('icons/File.png')
        self.owData_Sampler.setWidgetIcon('icons/DataSampler.png')
        self.owSelect_Attributes.setWidgetIcon('icons/SelectAttributes.png')
        self.owScatterplot.setWidgetIcon('icons/ScatterPlot.png')
        self.owLinear_Projection.setWidgetIcon('icons/LinearProjection.png')
        self.owRadviz.setWidgetIcon('icons/Radviz.png')
        self.owPolyviz.setWidgetIcon('icons/Polyviz.png')
        self.owParallel_coordinates.setWidgetIcon('icons/ParallelCoordinates.png')
        self.owMosaic_Display.setWidgetIcon('icons/MosaicDisplay.png')

        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owSelect_Attributes)
        self.signalManager.addWidget(self.owScatterplot)
        self.signalManager.addWidget(self.owLinear_Projection)
        self.signalManager.addWidget(self.owRadviz)
        self.signalManager.addWidget(self.owPolyviz)
        self.signalManager.addWidget(self.owParallel_coordinates)
        self.signalManager.addWidget(self.owMosaic_Display)

        # create widget buttons
        owButtonFile = QPushButton("File", self)
        owButtonData_Sampler = QPushButton("Data Sampler", self)
        owButtonSelect_Attributes = QPushButton("Select Attributes", self)
        owButtonScatterplot = QPushButton("Scatterplot", self)
        owButtonLinear_Projection = QPushButton("Linear Projection", self)
        owButtonRadviz = QPushButton("Radviz", self)
        owButtonPolyviz = QPushButton("Polyviz", self)
        owButtonParallel_coordinates = QPushButton("Parallel coordinates", self)
        owButtonMosaic_Display = QPushButton("Mosaic Display", self)
        frameSpace = QFrame(self);  frameSpace.setMinimumHeight(20); frameSpace.setMaximumHeight(20)
        exitButton = QPushButton("E&xit",self)
        self.connect(exitButton,SIGNAL("clicked()"), application, SLOT("quit()"))


        statusBar = QStatusBar(self)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        #connect GUI buttons to show widgets
        self.connect(owButtonFile ,SIGNAL("clicked()"), self.owFile.reshow)
        self.connect(owButtonData_Sampler ,SIGNAL("clicked()"), self.owData_Sampler.reshow)
        self.connect(owButtonSelect_Attributes ,SIGNAL("clicked()"), self.owSelect_Attributes.reshow)
        self.connect(owButtonScatterplot ,SIGNAL("clicked()"), self.owScatterplot.reshow)
        self.connect(owButtonLinear_Projection ,SIGNAL("clicked()"), self.owLinear_Projection.reshow)
        self.connect(owButtonRadviz ,SIGNAL("clicked()"), self.owRadviz.reshow)
        self.connect(owButtonPolyviz ,SIGNAL("clicked()"), self.owPolyviz.reshow)
        self.connect(owButtonParallel_coordinates ,SIGNAL("clicked()"), self.owParallel_coordinates.reshow)
        self.connect(owButtonMosaic_Display ,SIGNAL("clicked()"), self.owMosaic_Display.reshow)

        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owScatterplot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLinear_Projection, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owRadviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owPolyviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owParallel_coordinates, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owScatterplot, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owLinear_Projection, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owPolyviz, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owRadviz, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owParallel_coordinates, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMosaic_Display, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owMosaic_Display, 'Examples', 'Example Subset', 1)
        self.signalManager.setFreeze(0)



    def eventHandler(self, text, eventVerbosity = 1):
        if self.verbosity >= eventVerbosity:
            self.status.setText(text)

    def progressHandler(self, widget, val):
        if val < 0:
            self.status.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setProgress(0)
        elif val >100:
            self.status.setText("")
            self.progress.reset()
        else:
            self.progress.setProgress(val)
            self.update()



    def loadSettings(self):
        try:
            file = open("visualizations.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"])
        self.owData_Sampler.activateLoadedSettings()
        self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"])
        self.owSelect_Attributes.activateLoadedSettings()
        self.owScatterplot.loadSettingsStr(strSettings["Scatterplot"])
        self.owScatterplot.activateLoadedSettings()
        self.owLinear_Projection.loadSettingsStr(strSettings["Linear Projection"])
        self.owLinear_Projection.activateLoadedSettings()
        self.owRadviz.loadSettingsStr(strSettings["Radviz"])
        self.owRadviz.activateLoadedSettings()
        self.owPolyviz.loadSettingsStr(strSettings["Polyviz"])
        self.owPolyviz.activateLoadedSettings()
        self.owParallel_coordinates.loadSettingsStr(strSettings["Parallel coordinates"])
        self.owParallel_coordinates.activateLoadedSettings()
        self.owMosaic_Display.loadSettingsStr(strSettings["Mosaic Display"])
        self.owMosaic_Display.activateLoadedSettings()


    def saveSettings(self):
        return
        if DEBUG_MODE: return
        self.owMosaic_Display.synchronizeContexts()
        self.owParallel_coordinates.synchronizeContexts()
        self.owPolyviz.synchronizeContexts()
        self.owRadviz.synchronizeContexts()
        self.owLinear_Projection.synchronizeContexts()
        self.owScatterplot.synchronizeContexts()
        self.owSelect_Attributes.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owFile.synchronizeContexts()

        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Scatterplot"] = self.owScatterplot.saveSettingsStr()
        strSettings["Linear Projection"] = self.owLinear_Projection.saveSettingsStr()
        strSettings["Radviz"] = self.owRadviz.saveSettingsStr()
        strSettings["Polyviz"] = self.owPolyviz.saveSettingsStr()
        strSettings["Parallel coordinates"] = self.owParallel_coordinates.saveSettingsStr()
        strSettings["Mosaic Display"] = self.owMosaic_Display.saveSettingsStr()

        file = open("visualizations.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()



if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    application.setMainWidget(ow)
    ow.show()

    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_loop()
    #ow.saveSettings()
