# Building Suites

The Suite class creates a suite using the ecflow open source software. The Suite class creates a suite using a configuration file sent as an argument to the constructor. The configuration file needs to contain different fields to setup mostly directories where the suite will find files, the server name and port which is running the ecflow server. An example of a configuration file is given in this directory.

## Creating families in the suite

In order to create a family in the suite created by the Suite class using a configuration file, you need to call the method Suite.createFamilyLoop() which will create a family under the suite which will loop over time. The arguments are:

- name: the name of family, it has to be unique in the current suite
- loop_type: the type of time requested, at the moment two types are supported:
    * daily: when all the tasks in the family are complete, the suite moves to the next day
    * weekly: when all the tasks in the family are complete, the suite moves to the next week
- python_scripts: an absolute path to a directory structure where python scripts are to be found. A bash 'find' is used to perform this operation
- start_date: the date when the family should start. If not specified, the system date is used
- duration: how long the family should run for in days. If not specified, 25 years is the default value.

## Defining a family

Here is an example about how to define a family in the suite using the Suite class:

```python
import ecflow
from suites.suite import Suite

class Import(object):

    def __call__(self,parent):
        import_data = parent.add_task('import_data')
        import_data.add_time('13:00')
        check_data = parent.add_task('check_import')
        check_data.add_trigger('import_data == complete')

factory = Suite.createFamilyLoop('import','daily','/home/platin/warehouse/database')
factory.register('import',Import)
```

The parent argument is the ecflow suite object created by the Suite object. For more information about what can be done here:

https://software.ecmwf.int/wiki/display/ECFLOW/Documentation

## Defining triggers

Triggers are what enables a task to run. By default, tasks are run in the order of definition, in parallel if not triggers are defined. Triggers are described in the ecflow documentation, there is a custom implementation of some triggers in this framework

### Dependency trigger
It is handled by ecflow, for a task t:

    t.add_trigger('/mysuite/polling/greenlight==complete')


### Time trigger
It is handled by ecflow, for a family or a task t:

    t.add_time('13:45')

The task will start at 13:45, system time.

### Weekday trigger
this is handled by this framework, for a famlily or a task t:

    t.add_days_of_week(['monday','wednesday','saturday']) # only runs on those 3 days

### Day of month trigger
this is handled by this framework, for a famlily or a task t:

    t.add_days_of_month([2,4,25]) # only runs on those 3 days in the month

### Combined triggers
this is handled both by this framework and ecflow, for a famlily or a task t:

    t.add_trigger('the_previous_task == complete') # will only trigger when this is verified
    t.add_days_of_week('wednesday') 
    t.add_days_of_month(15)

this taks t will run on wednesdays, on the 15th of the month, only as soon as the previous task is complete. If the 15th is a Wednesday, then both conditions are verified.

## Dealing with emails
The framework implements sending emails using gmail accounts. In order to authenticate, the framework looks for the file ~/.dbs/.gmail.yaml which should have the following structure:

```yaml

credentials:
    "email address1": password1
    "email address2": password2
```

There are two types of emails handled by the frameword:
- administrative emails
- end user emails

### Sending administrative emails

The configuration file sent to the Suite object should contain an entry similar to:

```yaml
    email:
        from: platin.pulse@gmail.com
        to:
            - a.b@gmail.com
```

By default, if a task fails, an email is sent using those parameters, indicating which task failed in the subject and the last 25 lines of the log file in the body of the email.

In the file <head.h> there is a function which can be called to send administrative emails, it is called "send_admin_email". It takes two arguments:
- subject of the email
- body of the email
- additional files are considered to be full paths to files to attach to the email, supported types:.txt .png. .jpg .jpeg .pdf .csv

If you need to attach a text file which doesn't have the .txt extension, like a log file:

```bash
ln -s $my_file_to_attach ./$my_file_to_attach.txt
send_admin_email "$subject" $body ./$my_file_to_attach.txt
```
Remember that because the subject and the body may contain spaces and \n characters, the function should be called as follows:

```bash

send_admin_email "$subject" "$body"
```

### Sending end user emails

To handle end user emails, there are two utilities in place:

- an email status, either global or local which determines how emails should be handled
- an send_email function which is able to handle email groups and email templates

#### Email status

The method "add_email_status_task()" is available from suite and family objects. It creates a task called email, with the right label and variable. The email.ecf task still needs to be created in the directory which contains all the tasks. A sample email taks is:

```
%include% <head.h>
%include% <email.h>

toggle_email_status

%include% <tail.h>
```

The toggle_email_status bash function which is included in the email.h file does two things:
- it updates an ecflow variable EMAIL_STATUS which is reflected in the bash as a variable with the same name. It takes three different values: 1, 2, 3
- it updates a label associated with the task called "recipients"

The different values of this variable and associated label reflect the following:
- 1: none. End user emails sent by tasks will not actually be sent. Good in debug mode
- 2: admin. End user emails sent by tasks will be sent to the admin group in the email configuration file (see below)
- 3: all: End user emails sent by tasks will be sent to all groups listed in the template file and bcc'ed to the admin group

The label associated with the task show in which state the vaiable is. It is probably a good idea to have an email task at the top level of the suite so that the global state affected all tasks in the suite. If you want to control this in a family separately from the global state, call the add_email_status_task() in the family where you want to have separate control.

#### Sending emails to end users

In order to send emails to end users,the framework needs to be notified by calling a function which involves configuration files. Thoses files are expected to be found in the "config" entry of the configuration file.

The function "send_email" received the folowing arguments:
- name of the product. Each email sent represents a product, more about this below
- name of the template file where this product will be found
- any number of extra arguments, each representing a full path to a file to attach to the email. Supported file extensions are .png .csv .txt .pdf .jpg .peg. Files to attach should have the right extension, use symbolic links to add the required extension.

The function "send_email" relies on the existence of a file in the "config" directory, called email.yaml. This file should contain email groups, for exmaple:

```yaml
#--------------------------------------------------------------
# Configuration file email addresses and group
#--------------------------------------------------------------

#--------------------------------------------------------------
# People who need to receive everything
#--------------------------------------------------------------
admin:
    - a.b@gmail.com

#--------------------------------------------------------------
# By groups
#--------------------------------------------------------------
products:
    - a.b@gmail.com

```

Email template files are needed for this function to operate: any file in the config directoy given as an argument to the function will do. A template file contains different elements:

```yaml
product_name:
    sender: platin.dw@gmail.com
    recipients:
        - marketing
        - sales
    subject:
        Look at those marvelous plots and spreadsheets today ${YYYYMMDD}
    body:
        |
        From the Platform Intelligence Team.
        Automated email, please address queries or comments to platin@datadist.com
        This is how we do variables: ${TASK}
    bcc: []
```

The different fields should be staightforward to understand, a few comments:
- the subject and the body can contain environment variables which can be susbstituted. If you introduce variables, make sure to export them in your task before calling the function.
- the bcc field is populated with the admin group by default, any addreses added here will be added to the list.

