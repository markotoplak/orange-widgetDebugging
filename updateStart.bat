c:
cd \Python23\Lib\site-packages
cvs -d :sspi:cvs@estelle.fri.uni-lj.si:/CVS checkout -A -- orange
cvs -d :sspi:cvs@estelle.fri.uni-lj.si:/CVS checkout -A -- WidgetDebugging

cd orange
cvs update -d -C
cd ..\widgetDebugging
cvs update -d -C
debugWidgets.py sendmail

shutdown -s
