c:
cd \Python25\Lib\site-packages

rem svn co --force http://www.ailab.si/svn/orange/trunk/orange/ orange
rem svn co --force http://www.ailab.si/svn/orange/trunk/add-ons/Bioinformatics/ orange\add-ons\Bioinformatics
rem svn co --force http://www.ailab.si/svn/orange/trunk/testing/widgetDebugging/ WidgetDebugging

svn cleanup orange
svn update orange

svn cleanup orange\add-ons\Bioinformatics
svn update orange\add-ons\Bioinformatics

svn cleanup WidgetDebugging
svn update WidgetDebugging

python orange\downloadPyd.py

cd WidgetDebugging
python debugWidgets.py --Sendmail

shutdown -s
