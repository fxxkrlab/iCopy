#!/usr/bin/python3
# -*- coding: utf-8 -*-

 
def restricted_msg(_lang,_first_name,_user_id):
    if "cn" == _lang:
        return(f"HI ! {_first_name} 您好\n"
            f"您的用户ID:{_user_id} 未经授权\n"
            "请用正确的方式添加")
    if "eng" == _lang:
        return(f"HI ! {_first_name}\n"
            f"Your user ID:{_user_id} is not allowed\n"
            "Pls set it in the correct way")
    if "jp" == _lang:
        return(f"HI ! {_first_name} こんにちは"
            f"ユーザーID:{_user_id}は許可されていない"
            "正しい方法で追加してください")

def start_msg(_lang, _first_name):
    if "cn" == _lang:
        return(f"Hi\! {_first_name} 欢迎使用 *iCopy*\n"
            "请选择转存模式")
    if "eng" == _lang:
        return(f"Hi\! {_first_name} Welcome to use *iCopy*\n"
            "Pls Choose the Transfer Mode")
    if "jp" == _lang:
        return(f"Hi\! {_first_name} 欢迎使用 *iCopy*\n"
            "ご覧のモードを選んでください")



# ##### /set Messages #####

def set_help(_lang):
    if "cn" == _lang:
        return("命令必须符合'/set' 或 '/set rule'规则")
    if "eng" == _lang:
        return("Only rules in '/set' and '/set rule' is vaild")
    if "jp" == _lang:
        return("'/set'または'/set rule'のルールに準拠する必要がある")

def set_multi_fav_rule():
    return ("\n "
        "`quick \+ folder/drive ID` \n "
        "`drive \+ drive id` \n "
        "`drive \- drive id` \n "
        "`folder \+ folder id` \n "
        "`folder \- folder id` \n"
        "\n")

def set_multi_fav_guide(_lang):

    if "cn" == _lang:
        return ("*请输入需要修改的目标地址* \n "
            "\n"
            "例 : 如下 *\+/\-* \n "
            "_quick \| drive \| folder_ 为对应前缀 \n "
            + set_multi_fav_rule() +
            "说明:"
            "随意组合排序: '*\+*' *_增加_*, '*\-*' *_取消_* \n "
            "_quick_ 只可存在_一个_，为快速目录")
    if "eng" == _lang:
        return ("*pls modify the Dst\\_ID List* \n "
            "\n"
            "e\.g : *\+/\-* \n "
            "_quick \| drive \| folder_ is the prefix \n "
            + set_multi_fav_rule() +
            "explain:"
            "The order does not matter: '*\+*' *_select_*, '*\-*' *_unselect_* \n "
            "_Only one quick\\_id can exist for quick\\_mode_")
    if "jp" == _lang:
        return ("*フォルダーIDやシェアドライバIDを入力してください* \n "
            "\n"
            "例 : 接頭辞 *\+/\-* ID\n "
            "_quick と drive と folder_ は接頭辞です \n "
            + set_multi_fav_rule() +
            "説明:"
            "順番は関係ない: '*\+*' *_增加する_*, '*\-*' *_キャンセル_* \n "
            "「クイックモード」は1つしか存在できません")

def set_single_fav_rule():
    return ("\n "
        "`/set quick\|drive\|folder \+/\- folder/drive ID` \n "
        "\n")

def set_single_fav_guide(_lang):

    if "cn" == _lang:
        return ("*请输入需要修改的目标地址* \n "
            "\n"
            "例 : 如下 *\+/\-* \n "
            + set_single_fav_rule())
    if "eng" == _lang:
        return ("*pls modify the Dst\\_ID List* \n "
            "\n"
            "e\.g : *\+/\-* \n "
            + set_single_fav_rule())
    if "jp" == _lang:
        return ("*フォルダーIDやシェアドライバIDを入力してください* \n "
            "\n"
            "例 : 接頭辞 *\+/\-* ID\n "
            + set_single_fav_rule())

def get_fav_len_invaild(_lang, each):
    if "cn" == _lang:
        return(f"您提交的 ID:{each[6:]} 不是有效的")
    if "eng" == _lang:
        return(f"ID:{each[6:]} is not vaild")
    if "jp" == _lang:
        return(f"入力したID:{each[6:]}は無効です")
