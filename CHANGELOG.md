### CHANGELOG

* version 0.1.3-beta.2  
FixBug 修正命令分隔符问题 以 jsusplit 替代 空格  

* version 0.1.3-beta.1  
Update Command str --> list, subprocess.Popen 父进程管理任务, Shell=False 安全处理  
Update killmission 采用 Popen.kill() 管理父进程，不再使用 killall -9 gclone 防止误杀  

* version 0.1.2-beta.2  
FixBug 修复任务完成状态判定错误  

* version 0.1.2-beta.1  
Update /cancel 任务开始前取消对话  
Update /kill 任务中取消当前任务  
Update 功能异步处理  
Update Handler 分组优先级处理  
FixBug 当前命令时 Bot 接受命令阻塞问题  

* version 0.1.1-beta.2  
Update requirements.txt  

* version 0.1.1-beta.1  
Update 新增通过 drive.v3 API 获取 foldername(仅团队盘根目录时)  
Update settings 中 新增 sa_path 路径需填写  
Update requirements.txt  
FixBug 团队盘根目录无法获取 name 任务显示空白  
FixBug 代码传参错误导致任务运行失败  

* version 0.1.0-alpha.1  
FixBug 版本号 字符错误  

* version 0.1.0-alpha.0  
Update 采用版本号管理更新  
Update 提取 utils.py 与 iCopy.py 分离  
Update 新增 requirements.txt 安装方式  
FixBug 修复不同入口时功能模块报错   
FixBug 修复所有被影响的 sendMsg 方式  

***  

2020.06.14
* [202006141250]  
修复 转存文件过少时机器人更新信息失败BUG
修正 选择模式后删除 “模式选择按钮”
* [202006140110]
增加 按钮选择模式功能
修正 因增加按钮造成的错误,重构所有Message方式

2020.06.13
* [202006131950]  
修复 转存文件过少时机器人更新信息失败BUG
增加 任务完成后返回START状态

2020.06.11
- [202006110322]  
增加  Copy 模式  
Copy 模式下转存目标目录可输入链接自定义  
- [202006110930]  
修正 [202006110322] 更新带来的错误文字描述以及 README内容  
- [202006111030]  
更新 引导文字
更新 任务文字模版
增加 代码中的注释

2020.06.10
- [202006101830]
重新启用chardet解决 byte 字符问题
导入新进度条 来自 steve x

2020.06.07
- [202006070305]
更新 quick mode 支持默认转存至与分享同名的文件夹内
- [202006071207]
修复 获取 Foldername 失败 BUG

2020.06.06 
- 更新 BOT MESSAGE EDIT 异步处理

2020.06.05 
- 更新 quick mode 完成
- 更新 代码整体更新
- 更新 删除无用演示教程代码

***
2020.06.04以前
- 创建 项目创建
- 项目 意在给群员提供一个可自定义命令的 gclone 转存 gdrive 分享内容的 TGBOT
- 说明 历史版本不做赘述