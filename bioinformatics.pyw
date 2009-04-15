#This file is automatically created by Orange Canvas and containing an Orange schema
# contact: ales.erjavec@fri.uni-lj.si
# useonly: brown-selected.tab

import orngEnviron
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI
from OWBaseWidget import *

class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'bioinformatics', signalManager = self.signalManager)
        self.widgets = {}
        self.loadSettings()
        
        self.tabs = QTabWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)
        self.resize(800,600)

        self.createWidget('OWFile', 'icons/File.png', 'File', 1, self.signalManager)
        self.createWidget('OWDisplayProfiles', 'icons/ExpressionProfiles.png', 'Data Profiles', 1, self.signalManager)
        self.createWidget('OWHeatMap', 'icons/HeatMap.png', 'Heat Map', 1, self.signalManager)
        self.createWidget('OWGOEnrichmentAnalysis', 'icons/GOTermFinder.png', 'GO Enrichment Analysis', 1, self.signalManager)
        self.createWidget('OWKEGGPathwayBrowser', 'icons/KEGG.png', 'KEGG Pathway Browser', 1, self.signalManager)
        self.createWidget('OWFeatureSelection', 'icons/FeatureSelection.png', 'Gene Selection', 1, self.signalManager)
        self.createWidget('OWVulcanoPlot', 'icons/VulcanoPlot.png', 'Vulcano Plot', 1, self.signalManager)
        self.createWidget('OWDataTable', 'icons/DataTable.png', 'Data Table', 1, self.signalManager)
        
        
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
        self.signalManager.addLink( self.widgets['File'], self.widgets['Data Profiles'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Heat Map'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['GO Enrichment Analysis'], 'Examples', 'Cluster Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['KEGG Pathway Browser'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Gene Selection'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Vulcano Plot'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Gene Selection'], self.widgets['Data Table'], 'Examples with selected attributes', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Vulcano Plot'], self.widgets['Data Table'], 'Examples with selected attributes', 'Examples', 1)
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
        if shown: OWGUI.createTabPage(self.tabs, caption, widget)
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
            file = open("bioinformatics.sav", "r")
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
        file = open("bioinformatics.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        