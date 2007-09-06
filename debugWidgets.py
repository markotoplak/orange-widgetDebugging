import orngOrangeFoldersQt4
import os, sys, random, smtplib, re, time
import orange, subprocess

# options and settings
nrOfThingsToChange = 2000   # how many random clicks do we want to simulate
timeLimit = 30              # 30 minutes is the maximum time that we will spend in testing one schema

# possible command line parameters
sendMailText = "-sendmail"      # do we want to send an email to authors after finishing
verbosity1Text = "-verbose"     # do we want to see a bit more output from widgets - prints a line for every change in the widget (checkboxes, buttons, comboboxes, ...)
verbosity2Text = "-Verbose"     # do we want to see a lot of output from widgets - prints also passing and processing of signals
changesText = "-changes="       # specify the number of random changes that you would like to do in each tested schema
debugOneText = "debugOne.py"

# get gui applications to try
guiAppPath = os.path.split(sys.argv[0])[0]
sys.path.append(guiAppPath)
os.chdir(guiAppPath)

sendMail = sendMailText in sys.argv[1:]     # do we want to send status mail or not
verbosity = 0
if verbosity1Text in sys.argv[1:]: verbosity = 1
if verbosity2Text in sys.argv[1:]: verbosity = 2

guiApps = sys.argv[1:]

# do we have a specific number of things to change
for flag in guiApps:
    if changesText.lower() in flag.lower():
        guiApps.remove(flag)
        nrOfThingsToChange = int(flag[flag.index("=") + 1 :])

#guiApps = ["visualizations.py"]
#verbosity = 2

for text in [sendMailText, verbosity1Text, verbosity2Text, debugOneText]:
    if text in guiApps:
        guiApps.remove(text)

if len(guiApps) == 0:
    for name in os.listdir(guiAppPath):
        if os.path.isfile(os.path.join(guiAppPath, name)) and os.path.splitext(name)[1].lower() in [".py", ".pyw"] and name.lower() not in ["debugwidgets.py", "debugone.py"]:
            guiApps.append(name)

widgetStatus = ""
nrOfFailed = 0

for guiApp in guiApps:
    guiName, guiExt = os.path.splitext(guiApp)
    if guiExt.lower() not in [".py", ".pyw"]:
        if os.path.exists(guiName + ".py"):
            guiApp = guiName + ".py"
        else:
            print "invalid file type for file", guiApp
            continue

    print guiApp
    startTime = time.time()
    process = subprocess.Popen(sys.executable + " debugOne.py %s %s %s %s" % (guiApp, str(nrOfThingsToChange), str(verbosity), str(timeLimit)))

    while process.poll() == None and time.time() - startTime < timeLimit * 60 + 10:
         time.sleep(3)

    successful = 1
    if process.poll() == None and sys.platform == "win32":
        import win32api
        win32api.TerminateProcess(process.pid,0)
        successful = 0


    print "Finished. Status:",

    # check output for exceptions
    f = open(guiName + ".txt", "rt")
    content = f.read()
    f.close()
    if content.find("Unhandled exception") != -1 or content.find("Time limit (%d min) exceeded" % (timeLimit)) != -1 or not successful:
        if not successful:
            widgetStatus += " TIMEOUT\n"
            print "TIMEOUT"
        else:
            widgetStatus += " FAILED\n"
            print "FAILED"
        nrOfFailed += 1

        f = open(guiApp)
        script = f.read()
        f.close()

        # if we found somebody to bug then send him an email
        search = re.search("contact:(?P<imena>.*)\n", script)
        if (search) and sendMail == 1:
            fromaddr = "orange@fri.uni-lj.si"
            toaddrs = search.group("imena")
            toaddrs.replace(" ", ",")
            msg = "From: %s\r\nTo: %s\r\nSubject: Exception in widgets - %s script\r\n\r\n" % (fromaddr, toaddrs, guiApp) + content
            server = smtplib.SMTP('212.235.188.18', 25)
            #server.set_debuglevel(0)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
    else:
        widgetStatus += " OK\n"
        print "OK"

if sendMail == 1:
    fromaddr = "orange@fri.uni-lj.si"
    toaddrs = "tomaz.curk@fri.uni-lj.si, gregor.leban@fri.uni-lj.si"
    msg = "From: %s\r\nTo: %s\r\nSubject: Widget test status. Number of failed: %d \r\n\r\n" % (fromaddr, toaddrs, nrOfFailed) + widgetStatus

    server = smtplib.SMTP('212.235.188.18', 25)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()