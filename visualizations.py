#This is automatically created file containing an Orange schema
# contact: gregor.leban@fri.uni-lj.si
# datasets: class, noclass
# ignore: titanic.tab
        
import sys, os, cPickle, orange, orngSignalManager, orngRegistry, OWGUI
import orngDebugging
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWDataSampler import *
from OWDataDomain import *
from OWParallelCoordinates import *
from OWPolyviz import *
from OWRadviz import *
from OWMosaicDisplay import *
from OWLinProj import *
from OWScatterPlot import *



class GUIApplication(QVBox):
    def __init__(self,parent=None):
        QVBox.__init__(self,parent)
        self.setCaption("Qt visualizations")
        self.signalManager = orngSignalManager.SignalManager()
        self.widgets = []
        

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owParallel_coordinates = OWParallelCoordinates(signalManager = self.signalManager)
        self.owPolyviz = OWPolyviz(signalManager = self.signalManager)
        self.owRadviz = OWRadviz(signalManager = self.signalManager)
        self.owMosaic_Display = OWMosaicDisplay(signalManager = self.signalManager)
        self.owLinear_Projection = OWLinProj(signalManager = self.signalManager)
        self.owScatterplot = OWScatterPlot(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owParallel_coordinates, 'icons/ParallelCoordinates.png', 'Parallel coordinates', 1)
        self.setWidgetParameters(self.owPolyviz, 'icons/Polyviz.png', 'Polyviz', 1)
        self.setWidgetParameters(self.owRadviz, 'icons/Radviz.png', 'Radviz', 1)
        self.setWidgetParameters(self.owMosaic_Display, 'icons/MosaicDisplay.png', 'Mosaic Display', 1)
        self.setWidgetParameters(self.owLinear_Projection, 'icons/LinearProjection.png', 'Linear Projection', 1)
        self.setWidgetParameters(self.owScatterplot, 'icons/ScatterPlot.png', 'Scatterplot', 1)
        
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
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owSelect_Attributes, 'Remaining Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owParallel_coordinates, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owPolyviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owRadviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owMosaic_Display, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owLinear_Projection, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owScatterplot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owScatterplot, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLinear_Projection, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMosaic_Display, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owRadviz, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owPolyviz, 'Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owParallel_coordinates, 'Examples', 'Example Subset', 1)
        self.signalManager.setFreeze(0)
        

    def setWidgetParameters(self, widget, iconName, caption, shown):
        self.signalManager.addWidget(widget)
        self.widgets.append(widget)
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setCaption(caption)
        if shown: OWGUI.button(self, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
            self.widgets.append(dlg)
            dlg.setEventHandler(self.eventHandler)
            dlg.setProgressBarHandler(self.progressHandler)
        
    def eventHandler(self, text, eventVerbosity = 1):
        if orngDebugging.orngVerbosity >= eventVerbosity:
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
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owParallel_coordinates.loadSettingsStr(strSettings["Parallel coordinates"]); self.owParallel_coordinates.activateLoadedSettings()
            self.owPolyviz.loadSettingsStr(strSettings["Polyviz"]); self.owPolyviz.activateLoadedSettings()
            self.owRadviz.loadSettingsStr(strSettings["Radviz"]); self.owRadviz.activateLoadedSettings()
            self.owMosaic_Display.loadSettingsStr(strSettings["Mosaic Display"]); self.owMosaic_Display.activateLoadedSettings()
            self.owLinear_Projection.loadSettingsStr(strSettings["Linear Projection"]); self.owLinear_Projection.activateLoadedSettings()
            self.owScatterplot.loadSettingsStr(strSettings["Scatterplot"]); self.owScatterplot.activateLoadedSettings()
            
        except:
            print "unable to load settings" 
            pass

    def saveSettings(self):
        if orngDebugging.orngDebuggingEnabled: return
        for widget in self.widgets[::-1]:
            widget.synchronizeContexts()
            widget.close()
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Parallel coordinates"] = self.owParallel_coordinates.saveSettingsStr()
        strSettings["Polyviz"] = self.owPolyviz.saveSettingsStr()
        strSettings["Radviz"] = self.owRadviz.saveSettingsStr()
        strSettings["Mosaic Display"] = self.owMosaic_Display.saveSettingsStr()
        strSettings["Linear Projection"] = self.owLinear_Projection.saveSettingsStr()
        strSettings["Scatterplot"] = self.owScatterplot.saveSettingsStr()
        
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
    ow.saveSettings()
        