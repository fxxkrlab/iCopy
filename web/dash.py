import json, logging, hashlib
from sanic import Sanic, response
from sanic_cors import CORS, cross_origin
from utils import load
from web import cook_resp as _resp

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

app = Sanic(__name__)
CORS(app)
_cfg = load.cfg

async def get_vaild_info():
    mydb = _resp.mydb
    login_col = mydb["login_col"]
    vaild_usr_doc = login_col.find_one({"_id": "login_info"})
    vaild_username = vaild_usr_doc["username"]
    vaild_password = vaild_usr_doc["password"]
    vaild_info = {"vaild_username":vaild_username,"vaild_password":vaild_password}
    return vaild_info

async def auth(token):
    result = {}
    vaild_info = await get_vaild_info()
    vaild_username = vaild_info['vaild_username']
    vaild_password = vaild_info['vaild_password']
    vaild_token = hashlib.md5((str(vaild_username) + str(vaild_password)).encode('utf-8')).hexdigest()
    if token != vaild_token:
        result['code'] = 50008
        result['message'] = "login faild"

        return response.json(result)

    else:
        return True

# ### login&auth route.v1
@app.route("/v1/login", methods=["POST",])
async def login(request):
    result = {}
    vaild_info = await get_vaild_info()
    current_username = request.json['username']
    current_password = request.json['password']
    vaild_username = vaild_info['vaild_username']
    vaild_password = vaild_info['vaild_password']
    if vaild_username == current_username and vaild_password == current_password:
        token = hashlib.md5((str(vaild_username) + str(vaild_password)).encode('utf-8')).hexdigest()
        result['code'] = 20000
        result['data'] = {"token":token}
        result['message'] = "login success"
        
    else:
        result['code'] = 20001
        result['message'] = "login faild"

    return response.json(result)

@app.route("/v1/userinfo")
async def userinfo(request):
    result = {}
    vaild_info = await get_vaild_info()
    vaild_username = vaild_info['vaild_username']
    await auth(request.args['token'])
    result['code'] = 20000
    result['data'] = {"name":vaild_username,"avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"}
    result['message'] = ""
        
    return response.json(result)

# ### api route.v1

@app.route("/v1/drivelist")
async def drivelist(request):
    x_auth = await auth(request.headers['X-Token'])
    if x_auth != True:
        return x_auth

    drivelist = _resp.get_drive_list()

    return response.json(drivelist, ensure_ascii=False)


@app.route("/v1/favlist")
async def sanic_fav_info(request):
    x_auth = await auth(request.headers['X-Token'])
    if x_auth != True:
        return x_auth
 
    fav_info = _resp.cook_fav_info()

    return response.json(fav_info, ensure_ascii=False)

@app.route("/v1/tasklist")
async def sanic_task_info(request):
    x_auth = await auth(request.headers['X-Token'])
    if x_auth != True:
        return x_auth

    task_info = _resp.cook_task_info()

    return response.json(task_info, ensure_ascii=False)

@app.route("/v1/currenttask")
async def taskdetail(request):
    x_auth = await auth(request.headers['X-Token'])
    if x_auth != True:
        return x_auth

    task_sum = load.task_list.find()
    y = len(list(task_sum))
    x = "Current Task SUM"

    return response.json({x: y})

app.static("/", "./web/vue-admin-simple/dist/")
app.static("/", "./web/vue-admin-simple/dist/index.html", content_type="text/html; charset=utf-8")
web_port = _cfg['web']['port']
def dashboard():
    app.run(host="0.0.0.0", port=web_port)