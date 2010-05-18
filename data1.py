#This file is automatically created by Orange Canvas and containing an Orange schema

import orngEnviron
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI
from OWBaseWidget import *

class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'data1', signalManager = self.signalManager)
        self.widgets = {}
        self.loadSettings()
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        self.createWidget('OWFile', 'icons/File.png', 'File', 1, self.signalManager)
        self.createWidget('OWDataInfo', 'icons/DataInfo.png', 'Info', 1, self.signalManager)
        self.createWidget('OWDataSampler', 'icons/DataSampler.png', 'Data Sampler', 1, self.signalManager)
        self.createWidget('OWDataDomain', 'icons/SelectAttributes.png', 'Select Attributes', 1, self.signalManager)
        self.createWidget('OWDataSampler', 'icons/DataSampler.png', 'Data Sampler (2)', 1, self.signalManager)
        self.createWidget('OWMergeData', 'icons/MergeData.png', 'Merge Data', 1, self.signalManager)
        self.createWidget('OWDataTable', 'icons/DataTable.png', 'Data Table', 1, self.signalManager)
        self.createWidget('OWConcatenate', 'icons/Concatenate.png', 'Concatenate', 1, self.signalManager)
        self.createWidget('OWDataTable', 'icons/DataTable.png', 'Data Table (2)', 1, self.signalManager)
        self.createWidget('OWSelectData', 'icons/SelectData.png', 'Select Data', 1, self.signalManager)
        self.createWidget('OWDataTable', 'icons/DataTable.png', 'Data Table (3)', 1, self.signalManager)
        self.createWidget('OWContinuize', 'icons/Continuize.png', 'Continuize', 1, self.signalManager)
        self.createWidget('OWDiscretize', 'icons/Discretize.png', 'Discretize', 1, self.signalManager)
        self.createWidget('OWImpute', 'icons/Impute.png', 'Impute', 1, self.signalManager)
        self.createWidget('OWOutliers', 'icons/Outliers.png', 'Outliers', 1, self.signalManager)
        self.createWidget('OWDataTable', 'icons/DataTable.png', 'Data Table (4)', 1, self.signalManager)
        
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

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Info'], 'Examples', 'Data Table', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Data Sampler'], 'Examples', 'Data', 1)
        self.signalManager.addLink( self.widgets['Data Sampler'], self.widgets['Select Attributes'], 'Sample', 'Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Data Sampler (2)'], 'Examples', 'Data', 1)
        self.signalManager.addLink( self.widgets['Data Sampler'], self.widgets['Merge Data'], 'Sample', 'Examples A', 1)
        self.signalManager.addLink( self.widgets['Data Sampler (2)'], self.widgets['Merge Data'], 'Sample', 'Examples B', 1)
        self.signalManager.addLink( self.widgets['Merge Data'], self.widgets['Data Table'], 'Merged Examples A+B', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Merge Data'], self.widgets['Data Table'], 'Merged Examples B+A', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Data Sampler'], self.widgets['Concatenate'], 'Sample', 'Primary Table', 1)
        self.signalManager.addLink( self.widgets['Data Sampler (2)'], self.widgets['Concatenate'], 'Sample', 'Additional Tables', 1)
        self.signalManager.addLink( self.widgets['Concatenate'], self.widgets['Data Table (2)'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Data Sampler'], self.widgets['Select Data'], 'Sample', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Data'], self.widgets['Data Table (3)'], 'Matching Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Continuize'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Discretize'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Impute'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Outliers'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Impute'], self.widgets['Data Table (4)'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Data Table'], self.widgets['Data Table (4)'], 'Selected Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Data Table (2)'], self.widgets['Data Table (4)'], 'Selected Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Continuize'], self.widgets['Data Table (4)'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Discretize'], self.widgets['Data Table (4)'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Outliers'], self.widgets['Data Table (4)'], 'Outliers', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Outliers'], self.widgets['Data Table (4)'], 'Inliers', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Outliers'], self.widgets['Data Table (4)'], 'Examples with Z-scores', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Data Table (3)'], self.widgets['Data Table (4)'], 'Selected Examples', 'Examples', 1)
        self.signalManager.setFreeze(0)
        

    def createWidget(self, fname, iconName, caption, shown, signalManager):
        widgetSettings = cPickle.loads(self.strSettings[caption])
        m = __import__(fname)
        widget = m.__dict__[fname].__new__(m.__dict__[fname], _settingsFromSchema = widgetSettings)
        widget.__init__(signalManager=signalManager)
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setWindowTitle(caption)
        self.signalManager.addWidget(widget)
        self.widgets[caption] = widget
        if shown: OWGUI.button(self.box, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
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
            file = open("data1.sav", "r")
            self.strSettings = cPickle.load(file)
            file.close()

        except:
            print "unable to load settings"
            pass

    def closeEvent(self, ev):
        OWBaseWidget.closeEvent(self, ev)
        if orngDebugging.orngDebuggingEnabled: return
        strSettings = {}
        for (name, widget) in self.widgets.items():
            widget.synchronizeContexts()
            strSettings[name] = widget.saveSettingsStr()
            widget.close()
        file = open("data1.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        