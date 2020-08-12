# BOT COMMAND

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
    ┖ set web - set web account&password  
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
