c:
cd \Python25\Lib\site-packages

net use o: \\www.ailab.si\download

rem svn co --force http://www.ailab.si/svn/orange/trunk/orange/ orange
rem svn co --force http://www.ailab.si/svn/orange/trunk/add-ons/Bioinformatics/ orange\add-ons\Bioinformatics
rem svn co --force http://www.ailab.si/svn/orange/trunk/testing/widgetDebugging/ WidgetDebugging

svn cleanup orange
svn update --force orange

svn cleanup orange\add-ons\Bioinformatics
svn update --force orange\add-ons\Bioinformatics

svn cleanup WidgetDebugging
svn update --force WidgetDebugging

C:\cygwin\bin\find.exe orange/ -name "*.pyc" -delete
C:\cygwin\bin\find.exe WidgetDebugging/ -name "*.pyc" -delete

python orange\downloadPyd.py

python -c "import orngServerFiles; orngServerFiles.update_local_files();"

cd WidgetDebugging
python debugWidgets.py --sendmail

cp widgetDebugging*.log o:\widgetDebuggingLogs\winxp

shutdown -s
