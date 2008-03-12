#This is automatically created file containing an Orange schema
        
import orngOrangeFoldersQt4
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI

from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWKNN import *
from OWClassificationTree import *
from OWC45Tree import *
from OWITree import *
from OWClassificationTreeViewer import *
from OWMajority import *



class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'Classify', signalManager = self.signalManager)
        self.widgets = []
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owk_Nearest_Neighbours = OWKNN(signalManager = self.signalManager)
        self.owClassification_Tree = OWClassificationTree(signalManager = self.signalManager)
        self.owC45 = OWC45Tree(signalManager = self.signalManager)
        self.owInteractive_Tree_Builder = OWITree(signalManager = self.signalManager)
        self.owClassification_Tree_Viewer = OWClassificationTreeViewer(signalManager = self.signalManager)
        self.owMajority = OWMajority(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owk_Nearest_Neighbours, 'icons/kNearestNeighbours.png', 'k Nearest Neighbours', 1)
        self.setWidgetParameters(self.owClassification_Tree, 'icons/ClassificationTree.png', 'Classification Tree', 1)
        self.setWidgetParameters(self.owC45, 'icons/C45.png', 'C4.5', 1)
        self.setWidgetParameters(self.owInteractive_Tree_Builder, 'icons/ITree.png', 'Interactive Tree Builder', 1)
        self.setWidgetParameters(self.owClassification_Tree_Viewer, 'icons/ClassificationTreeViewer.png', 'Classification Tree Viewer', 1)
        self.setWidgetParameters(self.owMajority, 'icons/Majority.png', 'Majority', 1)
        
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
        self.signalManager.addLink( self.owClassification_Tree, self.owClassification_Tree_Viewer, 'Classification Tree', 'Classification Tree', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owk_Nearest_Neighbours, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owClassification_Tree, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owC45, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owInteractive_Tree_Builder, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMajority, 'Examples', 'Examples', 1)
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
            file = open("Classify.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owk_Nearest_Neighbours.loadSettingsStr(strSettings["k Nearest Neighbours"]); self.owk_Nearest_Neighbours.activateLoadedSettings()
            self.owClassification_Tree.loadSettingsStr(strSettings["Classification Tree"]); self.owClassification_Tree.activateLoadedSettings()
            self.owC45.loadSettingsStr(strSettings["C4.5"]); self.owC45.activateLoadedSettings()
            self.owInteractive_Tree_Builder.loadSettingsStr(strSettings["Interactive Tree Builder"]); self.owInteractive_Tree_Builder.activateLoadedSettings()
            self.owClassification_Tree_Viewer.loadSettingsStr(strSettings["Classification Tree Viewer"]); self.owClassification_Tree_Viewer.activateLoadedSettings()
            self.owMajority.loadSettingsStr(strSettings["Majority"]); self.owMajority.activateLoadedSettings()
            
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
        strSettings["k Nearest Neighbours"] = self.owk_Nearest_Neighbours.saveSettingsStr()
        strSettings["Classification Tree"] = self.owClassification_Tree.saveSettingsStr()
        strSettings["C4.5"] = self.owC45.saveSettingsStr()
        strSettings["Interactive Tree Builder"] = self.owInteractive_Tree_Builder.saveSettingsStr()
        strSettings["Classification Tree Viewer"] = self.owClassification_Tree_Viewer.saveSettingsStr()
        strSettings["Majority"] = self.owMajority.saveSettingsStr()
        
        file = open("Classify.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        