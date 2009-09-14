c:
cd \Python25\Lib\site-packages

rem svn co --force http://www.ailab.si/svn/orange/trunk/orange/ orange
rem svn co --force http://www.ailab.si/svn/orange/trunk/add-ons/Bioinformatics/ orange\add-ons\Bioinformatics
rem svn co --force http://www.ailab.si/svn/orange/trunk/testing/widgetDebugging/ WidgetDebugging

svn update orange
svn update orange\add-ons\Bioinformatics
svn update WidgetDebugging

cd orange
python downloadPy.py

cd ..\WidgetDebugging
python debugWidgets.py -sendmail

shutdown -s
