c:
cd \Python23\Lib\site-packages
rem cvs -d :sspi:cvs@estelle.fri.uni-lj.si:/CVS checkout -A -- orange
rem cvs -d :sspi:cvs@estelle.fri.uni-lj.si:/CVS checkout -- WidgetDebugging

cd orange
cvs update -d -C
cd ..\widgetDebugging
cvs update -d -C
debugWidgets.py

shutdown -s
