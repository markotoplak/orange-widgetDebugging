c:
cd \Python23\Lib\site-packages
rem cvs -d :pserver:cvs@estelle.fri.uni-lj.si:/CVS checkout -A -- orange
rem cvs -d :pserver:cvs@estelle.fri.uni-lj.si:/CVS checkout -A -- WidgetDebugging

cvs -d :pserver:cvs@estelle.fri.uni-lj.si:/CVS update -P -d -C orange
cvs -d :pserver:cvs@estelle.fri.uni-lj.si:/CVS update -P -d -C WidgetDebugging

cd orange
cvs update -d -C
cd ..\widgetDebugging
cvs update -d -C

debugWidgets.py sendmail

shutdown -s
