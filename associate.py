#This is automatically created file containing an Orange schema
        
import orngOrangeFoldersQt4
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI

from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWAssociationRules import *
from OWExampleDistance import *
from OWAttributeDistance import *
from OWKMeans import *
from OWInteractionGraph import *
from OWMDS import *



class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'associate', signalManager = self.signalManager)
        self.widgets = []
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owAssociation_Rules = OWAssociationRules(signalManager = self.signalManager)
        self.owExample_Distance = OWExampleDistance(signalManager = self.signalManager)
        self.owAttribute_Distance = OWAttributeDistance(signalManager = self.signalManager)
        self.owKMeans_Clustering = OWKMeans(signalManager = self.signalManager)
        self.owInteraction_Graph = OWInteractionGraph(signalManager = self.signalManager)
        self.owMDS = OWMDS(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owAssociation_Rules, 'icons/AssociationRules.png', 'Association Rules', 1)
        self.setWidgetParameters(self.owExample_Distance, 'icons/ExampleDistance.png', 'Example Distance', 1)
        self.setWidgetParameters(self.owAttribute_Distance, 'icons/AttributeDistance.png', 'Attribute Distance', 1)
        self.setWidgetParameters(self.owKMeans_Clustering, 'icons/KMeans.png', 'K-Means Clustering', 1)
        self.setWidgetParameters(self.owInteraction_Graph, 'icons/InteractionGraph.png', 'Interaction Graph', 1)
        self.setWidgetParameters(self.owMDS, 'MDS.png', 'MDS', 1)
        
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
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owAssociation_Rules, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owExample_Distance, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owAttribute_Distance, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owKMeans_Clustering, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owInteraction_Graph, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owExample_Distance, self.owMDS, 'Distance Matrix', 'Distances', 1)
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
            file = open("associate.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owAssociation_Rules.loadSettingsStr(strSettings["Association Rules"]); self.owAssociation_Rules.activateLoadedSettings()
            self.owExample_Distance.loadSettingsStr(strSettings["Example Distance"]); self.owExample_Distance.activateLoadedSettings()
            self.owAttribute_Distance.loadSettingsStr(strSettings["Attribute Distance"]); self.owAttribute_Distance.activateLoadedSettings()
            self.owKMeans_Clustering.loadSettingsStr(strSettings["K-Means Clustering"]); self.owKMeans_Clustering.activateLoadedSettings()
            self.owInteraction_Graph.loadSettingsStr(strSettings["Interaction Graph"]); self.owInteraction_Graph.activateLoadedSettings()
            self.owMDS.loadSettingsStr(strSettings["MDS"]); self.owMDS.activateLoadedSettings()
            
        except:
            print "unable to load settings" 
            pass

    def closeEvent(self, ev):
        OWBaseWidget.closeEvent(self, ev)
        if orngDebugging.orngDebuggingEnabled: return
        for widget in self.widgets[::-1]:
            widget.synchronizeContexts()
            widget.close()
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Association Rules"] = self.owAssociation_Rules.saveSettingsStr()
        strSettings["Example Distance"] = self.owExample_Distance.saveSettingsStr()
        strSettings["Attribute Distance"] = self.owAttribute_Distance.saveSettingsStr()
        strSettings["K-Means Clustering"] = self.owKMeans_Clustering.saveSettingsStr()
        strSettings["Interaction Graph"] = self.owInteraction_Graph.saveSettingsStr()
        strSettings["MDS"] = self.owMDS.saveSettingsStr()
        
        file = open("associate.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        