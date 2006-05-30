import sys, os, cPickle, orange
import orngSignalManager

#set value in next line to 1 if want to output debugging info to file 'signalManagerOutput.txt'
DEBUG_MODE = 0

widgetDir = os.path.join(os.path.split(orange.__file__)[0], "OrangeWidgets")
if os.path.exists(widgetDir):
        for name in os.listdir(widgetDir):
            fullName = os.path.join(widgetDir, name)
            if os.path.isdir(fullName): sys.path.append(fullName)

from OWFile import *
from OWDataSampler import *
from OWAttributeStatistics import *
from OWScatterPlot import *
from OWLinProj import *
from OWRadviz import *
from OWPolyviz import *
from OWParallelCoordinates import *
from OWSurveyPlot import *
from OWSieveDiagram import *
from OWMosaicDisplay import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt visualizations")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owAttribute_Statistics = OWAttributeStatistics(signalManager = self.signalManager)
        self.owScatterplot = OWScatterPlot(signalManager = self.signalManager)
        self.owLinear_Projection = OWLinProj(signalManager = self.signalManager)
        self.owRadviz = OWRadviz(signalManager = self.signalManager)
        self.owPolyviz = OWPolyviz(signalManager = self.signalManager)
        self.owParallel_coordinates = OWParallelCoordinates(signalManager = self.signalManager)
        self.owSurvey_Plot = OWSurveyPlot(signalManager = self.signalManager)
        self.owSieve_Diagram = OWSieveDiagram(signalManager = self.signalManager)
        self.owMosaic_Display = OWMosaicDisplay(signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owAttribute_Statistics.setEventHandler(self.eventHandler)
        self.owAttribute_Statistics.setProgressBarHandler(self.progressHandler)
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
        self.owSurvey_Plot.setEventHandler(self.eventHandler)
        self.owSurvey_Plot.setProgressBarHandler(self.progressHandler)
        self.owSieve_Diagram.setEventHandler(self.eventHandler)
        self.owSieve_Diagram.setProgressBarHandler(self.progressHandler)
        self.owMosaic_Display.setEventHandler(self.eventHandler)
        self.owMosaic_Display.setProgressBarHandler(self.progressHandler)
        

        #list of widget instances
        self.widgets = [self.owFile, self.owData_Sampler, self.owAttribute_Statistics, self.owScatterplot, self.owLinear_Projection, self.owRadviz, self.owPolyviz, self.owParallel_coordinates, self.owSurvey_Plot, self.owSieve_Diagram, self.owMosaic_Display, ]
        # set widget captions
        self.owFile.setCaptionTitle('Qt File')
        self.owData_Sampler.setCaptionTitle('Qt Data Sampler')
        self.owAttribute_Statistics.setCaptionTitle('Qt Attribute Statistics')
        self.owScatterplot.setCaptionTitle('Qt Scatterplot')
        self.owLinear_Projection.setCaptionTitle('Qt Linear Projection')
        self.owRadviz.setCaptionTitle('Qt Radviz')
        self.owPolyviz.setCaptionTitle('Qt Polyviz')
        self.owParallel_coordinates.setCaptionTitle('Qt Parallel coordinates')
        self.owSurvey_Plot.setCaptionTitle('Qt Survey Plot')
        self.owSieve_Diagram.setCaptionTitle('Qt Sieve Diagram')
        self.owMosaic_Display.setCaptionTitle('Qt Mosaic Display')
        
        # set icons
        self.owFile.setWidgetIcon('icons/File.png')
        self.owData_Sampler.setWidgetIcon('icons/DataSampler.png')
        self.owAttribute_Statistics.setWidgetIcon('icons/AttributeStatistics.png')
        self.owScatterplot.setWidgetIcon('icons/ScatterPlot.png')
        self.owLinear_Projection.setWidgetIcon('icons/LinProj.png')
        self.owRadviz.setWidgetIcon('icons/Radviz.png')
        self.owPolyviz.setWidgetIcon('icons/Polyviz.png')
        self.owParallel_coordinates.setWidgetIcon('icons/ParallelCoordinates.png')
        self.owSurvey_Plot.setWidgetIcon('icons/SurveyPlot.png')
        self.owSieve_Diagram.setWidgetIcon('icons/SieveDiagram.png')
        self.owMosaic_Display.setWidgetIcon('icons/MosaicDisplay.png')
        
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owAttribute_Statistics)
        self.signalManager.addWidget(self.owScatterplot)
        self.signalManager.addWidget(self.owLinear_Projection)
        self.signalManager.addWidget(self.owRadviz)
        self.signalManager.addWidget(self.owPolyviz)
        self.signalManager.addWidget(self.owParallel_coordinates)
        self.signalManager.addWidget(self.owSurvey_Plot)
        self.signalManager.addWidget(self.owSieve_Diagram)
        self.signalManager.addWidget(self.owMosaic_Display)
        
        # create widget buttons
        owButtonFile = QPushButton("File", self)
        frameSpace1 = QFrame(self);  frameSpace1.setMinimumHeight(10); frameSpace1.setMaximumHeight(10)
        owButtonData_Sampler = QPushButton("Data Sampler", self)
        frameSpace2 = QFrame(self);  frameSpace2.setMinimumHeight(10); frameSpace2.setMaximumHeight(10)
        owButtonAttribute_Statistics = QPushButton("Attribute Statistics", self)
        owButtonScatterplot = QPushButton("Scatterplot", self)
        owButtonLinear_Projection = QPushButton("Linear Projection", self)
        owButtonRadviz = QPushButton("Radviz", self)
        owButtonPolyviz = QPushButton("Polyviz", self)
        owButtonParallel_coordinates = QPushButton("Parallel coordinates", self)
        owButtonSurvey_Plot = QPushButton("Survey Plot", self)
        frameSpace3 = QFrame(self);  frameSpace3.setMinimumHeight(10); frameSpace3.setMaximumHeight(10)
        owButtonSieve_Diagram = QPushButton("Sieve Diagram", self)
        owButtonMosaic_Display = QPushButton("Mosaic Display", self)
        frameSpace = QFrame(self);  frameSpace.setMinimumHeight(20); frameSpace.setMaximumHeight(20)
        exitButton = QPushButton("E&xit",self)
        self.connect(exitButton,SIGNAL("clicked()"), application, SLOT("quit()"))
        

        statusBar = QStatusBar(self)
        self.caption = QLabel('', statusBar)
        self.caption.setMaximumWidth(230)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.caption, 1)
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        #connect GUI buttons to show widgets
        self.connect(owButtonFile ,SIGNAL("clicked()"), self.owFile.reshow)
        self.connect(owButtonData_Sampler ,SIGNAL("clicked()"), self.owData_Sampler.reshow)
        self.connect(owButtonAttribute_Statistics ,SIGNAL("clicked()"), self.owAttribute_Statistics.reshow)
        self.connect(owButtonScatterplot ,SIGNAL("clicked()"), self.owScatterplot.reshow)
        self.connect(owButtonLinear_Projection ,SIGNAL("clicked()"), self.owLinear_Projection.reshow)
        self.connect(owButtonRadviz ,SIGNAL("clicked()"), self.owRadviz.reshow)
        self.connect(owButtonPolyviz ,SIGNAL("clicked()"), self.owPolyviz.reshow)
        self.connect(owButtonParallel_coordinates ,SIGNAL("clicked()"), self.owParallel_coordinates.reshow)
        self.connect(owButtonSurvey_Plot ,SIGNAL("clicked()"), self.owSurvey_Plot.reshow)
        self.connect(owButtonSieve_Diagram ,SIGNAL("clicked()"), self.owSieve_Diagram.reshow)
        self.connect(owButtonMosaic_Display ,SIGNAL("clicked()"), self.owMosaic_Display.reshow)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owFile, self.owAttribute_Statistics, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owScatterplot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owLinear_Projection, 'Classified Examples', 'Classified Examples', 1)
        self.signalManager.addLink( self.owFile, self.owRadviz, 'Classified Examples', 'Classified Examples', 1)
        self.signalManager.addLink( self.owFile, self.owParallel_coordinates, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owSurvey_Plot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owSieve_Diagram, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owMosaic_Display, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owScatterplot, 'Classified Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLinear_Projection, 'Classified Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owRadviz, 'Classified Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owFile, self.owPolyviz, 'Classified Examples', 'Classified Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owParallel_coordinates, 'Classified Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMosaic_Display, 'Classified Examples', 'Example Subset', 1)
        self.signalManager.setFreeze(0)
        


    def eventHandler(self, text):
        self.status.setText(text)
        
    def progressHandler(self, widget, val):
        if val < 0:
            self.caption.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setProgress(0)
        elif val >100:
            self.caption.setText("")
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
        self.owAttribute_Statistics.loadSettingsStr(strSettings["Attribute Statistics"])
        self.owAttribute_Statistics.activateLoadedSettings()
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
        self.owSurvey_Plot.loadSettingsStr(strSettings["Survey Plot"])
        self.owSurvey_Plot.activateLoadedSettings()
        self.owSieve_Diagram.loadSettingsStr(strSettings["Sieve Diagram"])
        self.owSieve_Diagram.activateLoadedSettings()
        self.owMosaic_Display.loadSettingsStr(strSettings["Mosaic Display"])
        self.owMosaic_Display.activateLoadedSettings()
        
        
    def saveSettings(self):
        return
        """
        if DEBUG_MODE: return
        self.owMosaic_Display.synchronizeContexts()
        self.owSieve_Diagram.synchronizeContexts()
        self.owSurvey_Plot.synchronizeContexts()
        self.owParallel_coordinates.synchronizeContexts()
        self.owPolyviz.synchronizeContexts()
        self.owRadviz.synchronizeContexts()
        self.owLinear_Projection.synchronizeContexts()
        self.owScatterplot.synchronizeContexts()
        self.owAttribute_Statistics.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Attribute Statistics"] = self.owAttribute_Statistics.saveSettingsStr()
        strSettings["Scatterplot"] = self.owScatterplot.saveSettingsStr()
        strSettings["Linear Projection"] = self.owLinear_Projection.saveSettingsStr()
        strSettings["Radviz"] = self.owRadviz.saveSettingsStr()
        strSettings["Polyviz"] = self.owPolyviz.saveSettingsStr()
        strSettings["Parallel coordinates"] = self.owParallel_coordinates.saveSettingsStr()
        strSettings["Survey Plot"] = self.owSurvey_Plot.saveSettingsStr()
        strSettings["Sieve Diagram"] = self.owSieve_Diagram.saveSettingsStr()
        strSettings["Mosaic Display"] = self.owMosaic_Display.saveSettingsStr()
        
        file = open("visualizations.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        """
        


if __name__ == "__main__": 
    application = QApplication(sys.argv)
    ow = GUIApplication()
    application.setMainWidget(ow)
    ow.show()

    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_loop()
    ow.saveSettings()
