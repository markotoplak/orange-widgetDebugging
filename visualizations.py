#This is automatically created file containing an Orange schema
        
import orngOrangeFoldersQt4
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI

from OWFile import *
from OWDataSampler import *
from OWDataDomain import *
from OWAttributeStatistics import *
from OWScatterPlot import *
from OWLinProj import *
from OWRadviz import *
from OWPolyviz import *
from OWParallelCoordinates import *
from OWSurveyPlot import *
from OWMosaicDisplay import *
from OWSieveDiagram import *



class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'visualizations', signalManager = self.signalManager)
        self.widgets = []
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owAttribute_Statistics = OWAttributeStatistics(signalManager = self.signalManager)
        self.owScatterplot = OWScatterPlot(signalManager = self.signalManager)
        self.owLinear_Projection = OWLinProj(signalManager = self.signalManager)
        self.owRadviz = OWRadviz(signalManager = self.signalManager)
        self.owPolyviz = OWPolyviz(signalManager = self.signalManager)
        self.owParallel_coordinates = OWParallelCoordinates(signalManager = self.signalManager)
        self.owSurvey_Plot = OWSurveyPlot(signalManager = self.signalManager)
        self.owMosaic_Display = OWMosaicDisplay(signalManager = self.signalManager)
        self.owSieve_Diagram = OWSieveDiagram(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owAttribute_Statistics, 'icons/AttributeStatistics.png', 'Attribute Statistics', 1)
        self.setWidgetParameters(self.owScatterplot, 'icons/ScatterPlot.png', 'Scatterplot', 1)
        self.setWidgetParameters(self.owLinear_Projection, 'icons/LinearProjection.png', 'Linear Projection', 1)
        self.setWidgetParameters(self.owRadviz, 'icons/Radviz.png', 'Radviz', 1)
        self.setWidgetParameters(self.owPolyviz, 'icons/Polyviz.png', 'Polyviz', 1)
        self.setWidgetParameters(self.owParallel_coordinates, 'icons/ParallelCoordinates.png', 'Parallel coordinates', 1)
        self.setWidgetParameters(self.owSurvey_Plot, 'icons/SurveyPlot.png', 'Survey Plot', 1)
        self.setWidgetParameters(self.owMosaic_Display, 'icons/MosaicDisplay.png', 'Mosaic Display', 1)
        self.setWidgetParameters(self.owSieve_Diagram, 'icons/SieveDiagram.png', 'Sieve Diagram', 1)
        
        box2 = OWGUI.widgetBox(self, 1)
        exitButton = OWGUI.button(box2, self, "Exit", callback = self.accept)
        self.layout().addStretch(100)
        
        statusBar = QStatusBar(self)
        self.layout().addWidget(statusBar)
        self.caption = QLabel('', statusBar)
        self.caption.setMaximumWidth(230)
        self.progress = QProgressBar(statusBar)
        self.progress.setMaximumWidth(100)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress)
        statusBar.addWidget(self.caption)
        statusBar.addWidget(self.status)
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owAttribute_Statistics, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owScatterplot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owLinear_Projection, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owRadviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owPolyviz, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owParallel_coordinates, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owSurvey_Plot, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owMosaic_Display, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owSieve_Diagram, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLinear_Projection, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owScatterplot, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owRadviz, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owPolyviz, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owParallel_coordinates, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMosaic_Display, 'Remaining Examples', 'Example Subset', 1)
        self.signalManager.setFreeze(0)
        

    def setWidgetParameters(self, widget, iconName, caption, shown):
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setWindowTitle(caption)
        self.signalManager.addWidget(widget)
        self.widgets.append(widget)
        if shown: OWGUI.button(self.box, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
            self.widgets.append(dlg)
            dlg.setEventHandler(self.eventHandler)
            dlg.setProgressBarHandler(self.progressHandler)
        
    def eventHandler(self, text, eventVerbosity = 1):
        if orngDebugging.orngVerbosity >= eventVerbosity:
            self.status.setText(text)

    def progressHandler(self, widget, val):
        if val < 0:
            self.caption.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setValue(0)
        elif val >100:
            self.caption.setText("")
            self.progress.reset()
        else:
            self.progress.setValue(val)
            self.update()

    def loadSettings(self):
        try:
            file = open("visualizations.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owAttribute_Statistics.loadSettingsStr(strSettings["Attribute Statistics"]); self.owAttribute_Statistics.activateLoadedSettings()
            self.owScatterplot.loadSettingsStr(strSettings["Scatterplot"]); self.owScatterplot.activateLoadedSettings()
            self.owLinear_Projection.loadSettingsStr(strSettings["Linear Projection"]); self.owLinear_Projection.activateLoadedSettings()
            self.owRadviz.loadSettingsStr(strSettings["Radviz"]); self.owRadviz.activateLoadedSettings()
            self.owPolyviz.loadSettingsStr(strSettings["Polyviz"]); self.owPolyviz.activateLoadedSettings()
            self.owParallel_coordinates.loadSettingsStr(strSettings["Parallel coordinates"]); self.owParallel_coordinates.activateLoadedSettings()
            self.owSurvey_Plot.loadSettingsStr(strSettings["Survey Plot"]); self.owSurvey_Plot.activateLoadedSettings()
            self.owMosaic_Display.loadSettingsStr(strSettings["Mosaic Display"]); self.owMosaic_Display.activateLoadedSettings()
            self.owSieve_Diagram.loadSettingsStr(strSettings["Sieve Diagram"]); self.owSieve_Diagram.activateLoadedSettings()
            
        except:
            print "unable to load settings" 
            pass

    def closeEvent(self, ev):
        OWBaseWidget.closeEvent(self, ev)
        print "debugging enabled: ", orngDebugging.orngDebuggingEnabled
        if orngDebugging.orngDebuggingEnabled: return
        for widget in self.widgets[::-1]:
            widget.synchronizeContexts()
            widget.close()
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Attribute Statistics"] = self.owAttribute_Statistics.saveSettingsStr()
        strSettings["Scatterplot"] = self.owScatterplot.saveSettingsStr()
        strSettings["Linear Projection"] = self.owLinear_Projection.saveSettingsStr()
        strSettings["Radviz"] = self.owRadviz.saveSettingsStr()
        strSettings["Polyviz"] = self.owPolyviz.saveSettingsStr()
        strSettings["Parallel coordinates"] = self.owParallel_coordinates.saveSettingsStr()
        strSettings["Survey Plot"] = self.owSurvey_Plot.saveSettingsStr()
        strSettings["Mosaic Display"] = self.owMosaic_Display.saveSettingsStr()
        strSettings["Sieve Diagram"] = self.owSieve_Diagram.saveSettingsStr()
        
        file = open("visualizations.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        