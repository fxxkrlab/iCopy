# iCopy v0.2 CHANGELOG

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
