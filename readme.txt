This is a step-by-step guide on how to create a script that will be
tested automatically using this module.

1. Create a schema in Orange Canvas that contains a group of widgets
   that you want to test. Save the schema (as .ows schema) and as a
   gui application (either with tabs or buttons).

2. Create a snapshot of the canvas schema (File / Print Schema / Save
   image) with the same name.

3. Following are changes that you can add on top of the schema if you
   want to modify its execution:

- add a comment like this: # contact: email_address1, email_address2
to specify email addresses that will receive am email in case testing
of this schema fails (usually only one email address).

- add a comment like: # datasets: class, noclass to specify if your
schema should be tested only on datasets with class variable (class),
on datasets without class variable (noclass) or on both (class,
noclass). If you don't specify this, datasets with and without a class
will be used in testing the schema.

- add a comment like: # ignore: titanic.tab, iris.tab to specify exact
names of datasets in Datasets folder that should not be used in the
test (for instance because they take up too much time).

For an example of this possible comments see "visualizations.py"

4. Commit files to cvs (.py (gui schema), .ows (canvas schema), .sav
   (settings of the widgets in schema) and .png (schema's
   screenshot)).

The script that you will put to cvs will be automatically executed by
debugWidgets.py script. In case your script fails (one or more
exceptions happen during the testing) a mail will be sent to the
contact authors. The mail you will receive will contain the log of
execution - including all the exceptions that happened.

The debugWidgets.py script will randomly select different datasets
from the Datasets folder. It will also randomly change gui components
in your schema. The only GUI components that will be randomly changed
are those that were created using the OWGUI module. When a component
is created using this module, a tuple containing all the necessary
information is added to the widgets list called _guiElements. If you
create a component using the OWGUI module and specifically don't want
it to be used in debugging add debuggingEnabled = 0 as one of the
parameters, e.g.:

self.optimizationDlgButton = OWGUI.button(self.optimizationButtons, self, "VizRank", callback = self.optimizationDlg.reshow, debuggingEnabled = 0)

NOTE:

There are some cases when you HAVE TO set debbugingEnabled = 0. One
example are components where the call of the callback function would
disrupt normal message processing by opening a MessageBox dialog or
something similar. Another example are time expensive callback
functions - for example VizRank's button would call a function that
could possibly take hours (or days to compute) to compute all possible
projections. We will not be able to debug such functions.

Calling debugWidgets.py on a custom schema:

Sometimes you want to see if one schema finishes without
exceptions. You can test this by calling "debugWidgets.py
name_of_schema.py". This will call debugWidgets only on the specified
schema. More schemas can be tested by simply listing their names,
e.g. "debugWidgets.py name1.py name2.py name3.py".

Additional flags that can be used in debugWidgets.py:

- sendmail: specify this flag if you want to notify the authors
  (specified in the schemas using "contact: name1 name2) in case
  exceptions happen while testing the script

- verbose: specify this if you want to see in the output file
  ("schema_name.txt") a detailed information on what was clicked,
  changed, selected while performing the test

- Verbose: speficy this if you want to see even more details on what
  is going on while testing - writes also passing and processing of
  signals between widgets

- changes=X : you can specify a custom number of changes (X) that will
  be tested while runing the schema (default: 2000)
