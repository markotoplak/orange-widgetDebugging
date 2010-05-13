import orngEnviron
import os, sys, random, smtplib, re, time
import orange, subprocess

from optparse import OptionParser
# options and settings
nrOfThingsToChange = 2000   # how many random clicks do we want to simulate
timeLimit = 30             # 20 minutes is the maximum time that we will spend in testing one schema
seed = 0

# possible command line parameters
sendMailText = "-sendmail"      # do we want to send an email to authors after finishing
verbosity1Text = "-verbose"     # do we want to see a bit more output from widgets - prints a line for every change in the widget (checkboxes, buttons, comboboxes, ...)
verbosity2Text = "-Verbose"     # do we want to see a lot of output from widgets - prints also passing and processing of signals
changesText = "-changes="       # specify the number of random changes that you would like to do in each tested schema
randomSeed = "-seed="
debugOneText = "debugOne.py"

parser = OptionParser()
parser.add_option("-m", "--sendmail", action="store_true", help="Send mail to script maintainers")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Prints a line for every change in the widget (checkboxes, buttons, comboboxes, ...)")
parser.add_option("-V", "--Verbose", action="store_true", dest="Verbose", help="Prints also passing and processing of signals")
parser.add_option("-c", "--Changes=", type=int, dest="nrOfThingsToChange", default=nrOfThingsToChange, help="How many random clicks do we want to simulate")
parser.add_option("-s", "--Seed=", type=int, dest="randomSeed", default=seed, help="Random seed")


options, args = parser.parse_args()

# get gui applications to try

#os.chdir(r"E:\Development\Orange-Qt4\WidgetDebugging")
guiAppPath = os.path.realpath(".")
sys.path.append(guiAppPath)

sendMail = sendMailText in sys.argv or options.sendmail    # do we want to send status mail or not
verbosity = 0
if verbosity1Text in sys.argv or options.verbose: verbosity = 1
if verbosity2Text in sys.argv or options.Verbose: verbosity = 2

#defaultaddrs = ["ales.erjavec@fri.uni-lj.si"]
defaultaddrs = ["tomaz.curk@fri.uni-lj.si", "gregor.leban@fri.uni-lj.si", "ales.erjavec@fri.uni-lj.si"]


guiApps = sys.argv
if "debugWidgets.py" in guiApps[0]: guiApps.pop(0)

# do we have a specific number of things to change
for flag in guiApps:
    if changesText.lower() in flag.lower():
        guiApps.remove(flag)
        nrOfThingsToChange = int(flag[flag.index("=") + 1 :])
nrOfThingsToChange = options.nrOfThingsToChange
randomSeed = options.randomSeed

#guiApps = ["visualizations.py"]
#verbosity = 2

#for text in [sendMailText, verbosity1Text, verbosity2Text, debugOneText]:
#    if text in guiApps:
#        guiApps.remove(text)
        
guiApps= args


if len(guiApps) == 0:
    for name in os.listdir(guiAppPath):
        if os.path.isfile(os.path.join(guiAppPath, name)) and os.path.splitext(name)[1].lower() in [".py", ".pyw"]:
            guiApps.append(name)

widgetStatus = ""
nrOfFailed = 0

groupedMsg = ""

for guiApp in guiApps:
    if guiApp.lower() in ["debugwidgets.py", "debugone.py"]: 
        continue 
    guiName, guiExt = os.path.splitext(guiApp)
    if guiExt.lower() not in [".py", ".pyw"]:
        if os.path.exists(guiName + ".py"):
            guiApp = guiName + ".py"
        elif os.path.exists(guiName + ".pyw"):
            guiApp = guiName + ".pyw"
        else:
            print "invalid file type for file", guiApp
            continue

    print guiApp
    startTime = time.time()
    process = subprocess.Popen([sys.executable, "debugOne.py", guiApp, str(nrOfThingsToChange), str(verbosity), str(timeLimit), str(randomSeed)])

    while process.poll() == None and time.time() - startTime < timeLimit * 60 + 10:
         time.sleep(3)

    successful = 1
    if process.poll() == None:
        if sys.platform == "win32":
            import win32api
            win32api.TerminateProcess(process._handle, 0)
        else:
            os.kill(process.pid, 9)
        successful = 0


    print "Finished. Status:",

    # check output for exceptions
    f = open(guiName + ".txt", "rt")
    content = f.read()
    f.close()
    if content.find("Unhandled exception") != -1 or content.find("Time limit (%d min) exceeded" % (timeLimit)) != -1 or not successful:
        if not successful:
            widgetStatus += guiApp + ": TIMEOUT\n"
            print "TIMEOUT"
        else:
            widgetStatus += guiApp + ": FAILED\n"
            print "FAILED"
        nrOfFailed += 1

        f = open(guiApp)
        script = f.read()
        f.close()
        
        groupedMsg += "=" * 10 + "\n"
        groupedMsg += "Exception in widgets - %s script\n\n" % guiApp if successful else "Time limit (%d min) exceeded in - %s script\n\n" % (timeLimit, guiApp)
        groupedMsg += content
        
        # if we found somebody to bug then send him an email
        search = re.search("contact:(?P<imena>.*)\n", script)
        if sendMail == 1 and search:
            fromaddr = "orange@fri.uni-lj.si"
            toaddrs = search.group("imena").split() #[addr for addr in (search.group("imena").split() if search else []) if addr not in defaultaddrs] + defaultaddrs
#            toaddrs.replace(" ", ",")
            msg = "From: %s\r\nTo: %s\r\nSubject: Exception in widgets - %s script\r\n\r\n" % (fromaddr, ", ".join(toaddrs), guiApp) + content
            server = smtplib.SMTP('212.235.188.18', 25)
            #server.set_debuglevel(0)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
    else:
        widgetStatus += guiApp + ": OK\n"
        print "OK"

if sendMail == 1:
    fromaddr = "orange@fri.uni-lj.si"
    toaddrs = defaultaddrs
    msg = "From: %s\r\nTo: %s\r\nSubject: Widget test status. Number of failed: %d \r\n\r\n" % (fromaddr, ", ".join(toaddrs), nrOfFailed) + widgetStatus + groupedMsg

    server = smtplib.SMTP('212.235.188.18', 25)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()