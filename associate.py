# contact: ales.erjavec@fri.uni-lj.si janez.demsar@fri.uni-lj.si blaz.zupan@fri.uni-lj.si

import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()
from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWAssociationRules import *
from OWExampleDistance import *
from OWAttributeDistance import *
from OWDistanceMap import *
from OWDistanceMap import *
from OWKMeans import *
from OWInteractionGraph import *
from OWMDS import *
from OWHierarchicalClustering import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt associate")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.verbosity = verbosity

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owAssociation_Rules = OWAssociationRules(signalManager = self.signalManager)
        self.owExample_Distance = OWExampleDistance(signalManager = self.signalManager)
        self.owAttribute_Distance = OWAttributeDistance(signalManager = self.signalManager)
        self.owDistance_Map = OWDistanceMap(signalManager = self.signalManager)
        self.owDistance_Map_2 = OWDistanceMap(signalManager = self.signalManager)
        self.owKMeans_Clustering = OWKMeans(signalManager = self.signalManager)
        self.owInteraction_Graph = OWInteractionGraph(signalManager = self.signalManager)
        self.owMDS = OWMDS(signalManager = self.signalManager)
        self.owHierarchical_Clustering = OWHierarchicalClustering(signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSelect_Attributes.setEventHandler(self.eventHandler)
        self.owSelect_Attributes.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owAssociation_Rules.setEventHandler(self.eventHandler)
        self.owAssociation_Rules.setProgressBarHandler(self.progressHandler)
        self.owExample_Distance.setEventHandler(self.eventHandler)
        self.owExample_Distance.setProgressBarHandler(self.progressHandler)
        self.owAttribute_Distance.setEventHandler(self.eventHandler)
        self.owAttribute_Distance.setProgressBarHandler(self.progressHandler)
        self.owDistance_Map.setEventHandler(self.eventHandler)
        self.owDistance_Map.setProgressBarHandler(self.progressHandler)
        self.owDistance_Map_2.setEventHandler(self.eventHandler)
        self.owDistance_Map_2.setProgressBarHandler(self.progressHandler)
        self.owKMeans_Clustering.setEventHandler(self.eventHandler)
        self.owKMeans_Clustering.setProgressBarHandler(self.progressHandler)
        self.owInteraction_Graph.setEventHandler(self.eventHandler)
        self.owInteraction_Graph.setProgressBarHandler(self.progressHandler)
        self.owMDS.setEventHandler(self.eventHandler)
        self.owMDS.setProgressBarHandler(self.progressHandler)
        self.owHierarchical_Clustering.setEventHandler(self.eventHandler)
        self.owHierarchical_Clustering.setProgressBarHandler(self.progressHandler)
        

        #list of widget instances
        self.widgets = [self.owFile, self.owSelect_Attributes, self.owData_Sampler, self.owAssociation_Rules, self.owExample_Distance, self.owAttribute_Distance, self.owDistance_Map, self.owDistance_Map_2, self.owKMeans_Clustering, self.owInteraction_Graph, self.owMDS, self.owHierarchical_Clustering, ]
        # set widget captions
        self.owFile.setCaptionTitle('Qt File')
        self.owSelect_Attributes.setCaptionTitle('Qt Select Attributes')
        self.owData_Sampler.setCaptionTitle('Qt Data Sampler')
        self.owAssociation_Rules.setCaptionTitle('Qt Association Rules')
        self.owExample_Distance.setCaptionTitle('Qt Example Distance')
        self.owAttribute_Distance.setCaptionTitle('Qt Attribute Distance')
        self.owDistance_Map.setCaptionTitle('Qt Distance Map')
        self.owDistance_Map_2.setCaptionTitle('Qt Distance Map (2)')
        self.owKMeans_Clustering.setCaptionTitle('Qt K-Means Clustering')
        self.owInteraction_Graph.setCaptionTitle('Qt Interaction Graph')
        self.owMDS.setCaptionTitle('Qt MDS')
        self.owHierarchical_Clustering.setCaptionTitle('Qt Hierarchical Clustering')
        
        # set icons
        self.owFile.setWidgetIcon('icons/File.png')
        self.owSelect_Attributes.setWidgetIcon('icons/SelectAttributes.png')
        self.owData_Sampler.setWidgetIcon('icons/DataSampler.png')
        self.owAssociation_Rules.setWidgetIcon('icons/AssociationRules.png')
        self.owExample_Distance.setWidgetIcon('icons/ExampleDistance.png')
        self.owAttribute_Distance.setWidgetIcon('icons/AttributeDistance.png')
        self.owDistance_Map.setWidgetIcon('icons/DistanceMap.png')
        self.owDistance_Map_2.setWidgetIcon('icons/DistanceMap.png')
        self.owKMeans_Clustering.setWidgetIcon('icons/KMeans.png')
        self.owInteraction_Graph.setWidgetIcon('icons/InteractionGraph.png')
        self.owMDS.setWidgetIcon('MDS.png')
        self.owHierarchical_Clustering.setWidgetIcon('HierarchicalClustering.png')
        
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owSelect_Attributes)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owAssociation_Rules)
        self.signalManager.addWidget(self.owExample_Distance)
        self.signalManager.addWidget(self.owAttribute_Distance)
        self.signalManager.addWidget(self.owDistance_Map)
        self.signalManager.addWidget(self.owDistance_Map_2)
        self.signalManager.addWidget(self.owKMeans_Clustering)
        self.signalManager.addWidget(self.owInteraction_Graph)
        self.signalManager.addWidget(self.owMDS)
        self.signalManager.addWidget(self.owHierarchical_Clustering)
        
        # create widget buttons
        owButtonFile = QPushButton("File", self)
        owButtonSelect_Attributes = QPushButton("Select Attributes", self)
        owButtonData_Sampler = QPushButton("Data Sampler", self)
        owButtonAssociation_Rules = QPushButton("Association Rules", self)
        owButtonExample_Distance = QPushButton("Example Distance", self)
        owButtonAttribute_Distance = QPushButton("Attribute Distance", self)
        owButtonDistance_Map = QPushButton("Distance Map", self)
        owButtonDistance_Map_2 = QPushButton("Distance Map (2)", self)
        owButtonKMeans_Clustering = QPushButton("K-Means Clustering", self)
        owButtonInteraction_Graph = QPushButton("Interaction Graph", self)
        owButtonMDS = QPushButton("MDS", self)
        owButtonHierarchical_Clustering = QPushButton("Hierarchical Clustering", self)
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
        self.connect(owButtonSelect_Attributes ,SIGNAL("clicked()"), self.owSelect_Attributes.reshow)
        self.connect(owButtonData_Sampler ,SIGNAL("clicked()"), self.owData_Sampler.reshow)
        self.connect(owButtonAssociation_Rules ,SIGNAL("clicked()"), self.owAssociation_Rules.reshow)
        self.connect(owButtonExample_Distance ,SIGNAL("clicked()"), self.owExample_Distance.reshow)
        self.connect(owButtonAttribute_Distance ,SIGNAL("clicked()"), self.owAttribute_Distance.reshow)
        self.connect(owButtonDistance_Map ,SIGNAL("clicked()"), self.owDistance_Map.reshow)
        self.connect(owButtonDistance_Map_2 ,SIGNAL("clicked()"), self.owDistance_Map_2.reshow)
        self.connect(owButtonKMeans_Clustering ,SIGNAL("clicked()"), self.owKMeans_Clustering.reshow)
        self.connect(owButtonInteraction_Graph ,SIGNAL("clicked()"), self.owInteraction_Graph.reshow)
        self.connect(owButtonMDS ,SIGNAL("clicked()"), self.owMDS.reshow)
        self.connect(owButtonHierarchical_Clustering ,SIGNAL("clicked()"), self.owHierarchical_Clustering.reshow)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owAssociation_Rules, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owExample_Distance, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owAttribute_Distance, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owExample_Distance, self.owDistance_Map, 'Distance Matrix', 'Distance Matrix', 1)
        self.signalManager.addLink( self.owAttribute_Distance, self.owDistance_Map_2, 'Distance Matrix', 'Distance Matrix', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owKMeans_Clustering, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owInteraction_Graph, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owExample_Distance, self.owMDS, 'Distance Matrix', 'Distances', 1)
        self.signalManager.addLink( self.owExample_Distance, self.owHierarchical_Clustering, 'Distance Matrix', 'Distance matrix', 1)
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
            file = open("associate.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"])
        self.owSelect_Attributes.activateLoadedSettings()
        self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"])
        self.owData_Sampler.activateLoadedSettings()
        self.owAssociation_Rules.loadSettingsStr(strSettings["Association Rules"])
        self.owAssociation_Rules.activateLoadedSettings()
        self.owExample_Distance.loadSettingsStr(strSettings["Example Distance"])
        self.owExample_Distance.activateLoadedSettings()
        self.owAttribute_Distance.loadSettingsStr(strSettings["Attribute Distance"])
        self.owAttribute_Distance.activateLoadedSettings()
        self.owDistance_Map.loadSettingsStr(strSettings["Distance Map"])
        self.owDistance_Map.activateLoadedSettings()
        self.owDistance_Map_2.loadSettingsStr(strSettings["Distance Map (2)"])
        self.owDistance_Map_2.activateLoadedSettings()
        self.owKMeans_Clustering.loadSettingsStr(strSettings["K-Means Clustering"])
        self.owKMeans_Clustering.activateLoadedSettings()
        self.owInteraction_Graph.loadSettingsStr(strSettings["Interaction Graph"])
        self.owInteraction_Graph.activateLoadedSettings()
        self.owMDS.loadSettingsStr(strSettings["MDS"])
        self.owMDS.activateLoadedSettings()
        self.owHierarchical_Clustering.loadSettingsStr(strSettings["Hierarchical Clustering"])
        self.owHierarchical_Clustering.activateLoadedSettings()
        

    def saveSettings(self):
        if DEBUG_MODE: return
        self.owHierarchical_Clustering.synchronizeContexts()
        self.owMDS.synchronizeContexts()
        self.owInteraction_Graph.synchronizeContexts()
        self.owKMeans_Clustering.synchronizeContexts()
        self.owDistance_Map_2.synchronizeContexts()
        self.owDistance_Map.synchronizeContexts()
        self.owAttribute_Distance.synchronizeContexts()
        self.owExample_Distance.synchronizeContexts()
        self.owAssociation_Rules.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owSelect_Attributes.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Association Rules"] = self.owAssociation_Rules.saveSettingsStr()
        strSettings["Example Distance"] = self.owExample_Distance.saveSettingsStr()
        strSettings["Attribute Distance"] = self.owAttribute_Distance.saveSettingsStr()
        strSettings["Distance Map"] = self.owDistance_Map.saveSettingsStr()
        strSettings["Distance Map (2)"] = self.owDistance_Map_2.saveSettingsStr()
        strSettings["K-Means Clustering"] = self.owKMeans_Clustering.saveSettingsStr()
        strSettings["Interaction Graph"] = self.owInteraction_Graph.saveSettingsStr()
        strSettings["MDS"] = self.owMDS.saveSettingsStr()
        strSettings["Hierarchical Clustering"] = self.owHierarchical_Clustering.saveSettingsStr()
        
        file = open("associate.sav", "w")
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
