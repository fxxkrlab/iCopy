# iCopy v0.2 CHANGELOG

## version 0.2.0-beta.6.4

+ Fixbugs:
  + FIX : "/set" function "import as name" error  
  
## version 0.2.0-beta.6.3

+ Update :  
  + ADD : "/kill size","/kill purge","/kill dedupe" was added to terminate the execution of these tasks  

+ Root Command：

  + start - nothing just say hello  
  + menu - main entry point  
quick - quick mode  
copy - full mode  
set - customize settings  
task - task query  
reset - restore task  
size - just size task  
dedupe - dedupe drives and folders  
purge - delete files and folder in specified fav trash bin  
cancel - cancel TG conversation  
kill - kill task  
ver - check iCopy version  
restart - restart iCopy  

  + Child Command:

    + set - customize settings  
    ┖ set - batch way  
    ┖ set rule - rules  
    ┖ fav|quick +/- id - single way  
    ┖ set purge - purge favorites  
    + size - size query  
    ┖ size - size the shared resource  
    ┖ size id - size specified task  
    ┖ size fav - size specified favorites  
    + dedupe - dedupe drives and folders  
    ┖ dedupe - dedupe specified favorites  
    ┖ dedupe id - dedupe specified task  
    + task - task query  
    ┖ task - task in processing  
    ┖ task list - future 10 tasks  
    ┖ task id - show the specified task
    + reset - restore task  
    ┖ reset - restore current task  
    ┖ reset id  - restore the specified task  
    + kill - kill task  
    ┖ kill - kill current transferring task  
    ┖ kill task - kill current transferring task  
    ┖ kill size - kill sizing task  
    ┖ kill purge - kill purge task  
    ┖ kill dedupe - kill dedupe task  

## version 0.2.0-beta.6.2

+ Update :  
  + ADD : Add "rmdir" operation to the "/Purge" function to clear the empty folder in the root directory.  

+ Fixbugs :  
  + FIX : "/dedupe" sendMsg error.  
  + FIX : Insert DATABASE error while dedupe payload finished.  

## version 0.2.0-beta.6.1

+ Update :  
  + ADD : "/dedupe" Now you can choose favorites to dedupe  
  + CHANGE : Move the stage tag uniformly to new file “utils/callback_stage.py"  

+ Fixbugs :  
  + Judge select favorites if is shared drive when you use "/purge" mode.  
  + Separately define bot variables in asynchronous-process to prevent errors in connecting Telegram.  

+ Root Command：

  + start - nothing just say hello  
  + menu - main entry point  
quick - quick mode  
copy - full mode  
set - customize settings  
task - task query  
reset - restore task  
size - just size task  
dedupe - dedupe drives and folders  
purge - delete files and folder in specified fav trash bin  
cancel - cancel TG conversation  
kill - kill task which is in processing  
ver - check iCopy version  
restart - restart iCopy  

  + Child Command:

    + set - customize settings  
    ┖ set - batch way  
    ┖ set rule - rules  
    ┖ fav|quick +/- id - single way  
    ┖ set purge - purge favorites  
    + size - size query  
    ┖ size - size the shared resource  
    ┖ size id - size specified task  
    ┖ size fav - size specified favorites  
    + dedupe - dedupe drives and folders  
    ┖ dedupe - dedupe specified favorites  
    ┖ dedupe id - dedupe specified task via task id  
    + task - task query  
    ┖ task - task in processing  
    ┖ task list - future 10 tasks  
    ┖ task id - show the specified task
    + reset - restore task  
    ┖ reset - restore current task  
    ┖ reset id  - restore the specified task  

## version 0.2.0-beta.6

+ Update :  
  + ADD : insert more details into Database and more initializated data  
  + ADD : feedback dst endpoint link when task end normally  
  + ADD : "/task id" only support the task which is start after v0.2.0b6  
  + ADD : mark tasks that have been reset in the database  
  + ADD : "/size id" & "/size fav"  
  + ADD : "/purge" to empty shared drive trash bin  
  + ADD : "/dedupe id" to dedupe task  
  + ADD : Record the last time of size and dedupe  

+ Fix :
  + FIX : Update RegEX Rules  

+ Root Command：

  + start - nothing just say hello  
  + menu - main entry point  
quick - quick mode  
copy - full mode  
set - customize settings  
task - task query  
reset - restore task  
size - just size task  
dedupe - dedupe specified task  
purge - delete files and folder in specified fav trash bin  
cancel - cancel TG conversation  
kill - kill task which is in processing  
ver - check iCopy version  
restart - restart iCopy  

  + Child Command:

    + set - customize settings  
    ┖ set - batch way  
    ┖ set rule - rules  
    ┖ fav|quick +/- id - single way  
    ┖ set purge - purge favorites  
    + size - size query
    ┖ size - size the shared resource  
    ┖ size id - size specified task  
    ┖ size fav - size specified favorites  
    + task - task query  
    ┖ task - task in processing  
    ┖ task list - future 10 tasks  
    ┖ task id - show the specified task
    + reset - restore task  
    ┖ reset - restore current task  
    ┖ reset id  - restore the specified task  

## version 0.2.0-beta.5.1

+ Update :
  + ADD : More task info into Database  

+ Fixbugs :
  + FIX : delete "directly in" mode keyboard after selection is choosen
  + FIX : Purge local var after Conversation END
  The task will not be committed twice now
  + FIX : "/task list" error
  Now "/task list" will display up to 10 tasks pending

+ Root Command：

  + start - nothing just say hello  
  + menu - main entry point  
quick - quick mode  
copy - full mode  
set - customize settings  
task - task query  
reset - restore task  
size - just size task  
cancel - cancel TG conversation  
kill - kill task which is in processing  
ver - check iCopy version  
restart - restart iCopy  

  + Child Command:

    + set - customize settings  
    ┖ set - batch way  
    ┖ set rule - rules  
    ┖ fav|quick +/- id - single way  
    ┖ set purge - purge favorites
    + task - task query  
    ┖ task - task in processing  
    ┖ task list - future 10 tasks  
    + reset - restore task  
    ┖ reset - restore current task  
    ┖ reset id  - restore the specified task  

## version 0.2.0-beta.5

+ Update :  
  + ADD : directly input sharelink then choose mode.

+ Fixbugs :
  + FIX : get shared drive name failed when the shared drive is temporarily granted permission for an outside party.
  + FIX : Fix the error of repeated tasks when entering multiple tasks at the same time.  
  + FIX : "reset" notice msg error
  
## version 0.2.0-beta.4.1  

+ Fixbugs :  
  + FIX : "/reset task_id" Database operation error

## version 0.2.0-beta.4  

+ Update :  
  + ADD "/size" a function to get simple size info  
  
+ Fixbugs :  
  + FIX : "/reset" send notice msg error
  + FIX : get shared drive name failed when the shared drive is temporarily granted permission for an outside party.  

***

## version 0.2.0-beta.3  

Notice : The new "conf.toml" should be replaced or you could modify the "conf.toml" by referring to the "example" one.  

+ Update :
  + ADD "/set purge"  
  Allow to Purge Favorties Setting Now.  
  this will not delete quick mode setting.
  + Now '--drive-server-side-across-configs' is Built in the iCopy. Remove from conf.toml  
  + '--ignore-checksum' is write in conf.toml default
  + ADD "/reset" and "/reset id" command.
  You could restore task with the command

***

## version 0.2.0-beta.2  

  Update : send confirm msg after task added  
  Update : '/start' is not in Conversation Handle any more  
  Update : Use '/menu' to select run mode instead of '/start'  

***

## version 0.2.0-beta.1  

The first beta version of v0.2  
β1 is a relatively stable without bugs version  
The following Command is Supported  

+ Root Command：

  + start - main entry point  
quick - quick mode  
copy - full mode  
set - customize settings  
task - task query  
cancel - cancel TG conversation  
kill - kill task which is in processing  
ver - check iCopy version  
restart - restart iCopy  

  + Child Command:

    + set - ustomize settings  
    ┖ set - batch way  
    ┖ set rule - rules  
    ┖ set fav|quick +/- id - single way  
task - task query  
    ┖ task - task in processing  
    ┖ task list - future 10 tasks  

***

## version 0.2.0-alpha.1 ～ alpha.15  

iCopy rebuild basework finished

## version 0.1.7-beta.3

Archived version
...
