from utils import load
import pymongo

cfg = load.cfg

# ### Mongodb
myclient = pymongo.MongoClient(
    f"{cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{cfg['database']['db_addr']}",
    port=cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[cfg["database"]["db_name"]]

fav_col = mydb["fav_col"]
task_list = mydb["task_list"]
db_counters = mydb["counters"]

def get_drive_list():
    drivelist = {}
    all_drive = load.all_drive

    drivelist['data'] = all_drive
    drivelist['code'] = 20000
    drivelist['message'] = ""

    return drivelist

def cook_fav_info():
    favlist = {}
    fav_info_array = []
    fav_info = fav_col.find({"fav_type":"fav"},{"_id": 0})
    for each in fav_info:
        if 'fav_size' and 'fav_object' in each:
            each['show_size'] = str(each['fav_size']) + "  " +each['fav_size_tail']
            each['percent'] = float(each['fav_object'] / 4000 )
            each['show_percent'] = str(each['percent']) + "%"
        else:
            each['fav_size'] = "UNKNOW"
            each['fav_object'] = "UNKNOW"
            each['show_size'] = "UNKNOW"
            each['show_percent'] = "UNKNOW"
        fav_info_array.append(each)

        favlist['data'] = fav_info_array
        favlist['code'] = 20000
        favlist['message'] = ""

    return favlist

def cook_task_info():
    tasklist = {}
    task_info_array = []
    task_info = task_list.find({"status":1,"error":0})
    for each in task_info:
        each['show_status'] = "Completed"
        if "task_total_prog_size_tail" in each:
            each['show_size'] = str(each['task_total_prog_size']) + " " + each['task_total_prog_size_tail']
        else:
            each['show_size'] = "UNKNOW"
        task_info_array.append(each)

    tasklist['code'] = 20000
    tasklist['data'] = task_info_array
    tasklist['message'] = ""

    return tasklist
