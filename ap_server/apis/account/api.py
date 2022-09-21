from asyncio.windows_events import NULL
from apis.account.model import *
from apis.account.module import *
from flask import session, request
from base_api.__init__ import CustomResource, send_mail
from utils.orcl_utils import *
from utils.authorization import *
from werkzeug.datastructures import FileStorage
ROLE_ADMIN = "Admin"
# @api.route("/test")
# class Login2(CustomResource):
#     allow_roles = [ROLE_ADMIN]
#     def post(self):
#         print(api.payload)
#         return "OK"
# @api.route("/login")
# class Login(CustomResource):
#     @api.expect(account_input_payload)
#     @api.marshal_with(account_output_payload)
#     def post(self):
#         session["roles"] = [ROLE_ADMIN]
#         data = api.payload
#         return Account.login(username=data["username"], passwd=data["passwd"])


@api.route("/Forget_Api")  # 9/2 忘記密碼(不確定)
class Forget_Api(CustomResource):
    @api.expect(forget_Api_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data_json = request.get_json()
        Use_orlc = OracleAccess()
        try:
            # 使用者抓取輸入信箱
            user_id = data_json.get('user_id', None)
            # 判斷是否有該使用者
            sql = """SELECT PASSWORD_ FROM KUOHWA_LOGIN WHERE USER_='{}'""".format(
                user_id)
            val = Use_orlc.query(sql)
            if val == []:
                print("抱歉，無此使用者")
            else:
                print("您好! {}".format(user_id))
                # 信件
                title = "使用者您好，您的使用者密碼為....."
                content = val[0]
                send_mail(user_id, title, content[0])
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
        return msg


@api.route("/add_account_list")  # 9/12 新增使用者
class Add_account_list(CustomResource):
    @api.expect(add_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            # 取得輸入資料
            data_json = request.get_json()
            user_id = data_json.get('user_id', None)
            role = data_json.get('role', None)
            email = data_json.get('email', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            # 放入資料庫
            Use_orlc = OracleAccess()
            data_list = [user_id, email, role[0], role[1], role[2], ""]
            sql = "INSERT INTO KUO_add_account VALUES (:1, :2, :3, :4, :5, :6)"
            Use_orlc.insert(sql, data_list)
            Use_orlc.close()
        finally:
            return msg


@api.route("/delete_account_list")  # 9/12 刪除使用者
class Delete_account_list(CustomResource):
    @api.expect(delete_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            # 取得輸入資料
            data_json = request.get_json()
            user_id = data_json.get('user_id', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            # 刪除USER_ID資料庫
            Use_orlc = OracleAccess()
            sql = "DELETE FROM KUO_add_account WHERE USER_ID='{}'".format(
                user_id)
            print(sql)
            Use_orlc.delete(sql)
            Use_orlc.close()
        finally:
            return msg


@api.route("/update_account_list")  # 9/12 更新使用者
class Update_account_list(CustomResource):
    @api.expect(update_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            # 取得輸入資料
            data_json = request.get_json()
            old_user_id = data_json.get('old_user_id', None)
            update_data = data_json.get('data', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            # 更新資料庫的舊資料
            Use_orlc = OracleAccess()
            sql = "UPDATE KUO_add_account SET USER_ID='{}', EMAIL='{}', ROLE_1='{}', ROLE_2='{}',ROLE_3='{}' WHERE USER_ID='{}'".format(
                update_data['new_user_id'], update_data['new_email'], update_data['new_role'][0], update_data['new_role'][1], update_data['new_role'][2], old_user_id)
            Use_orlc.update(sql)
            Use_orlc.close()
        finally:
            return msg


@api.route("/get_account_list")  # 9/13取得使用者資料
class Get_account_list(CustomResource):
    @api.expect(get_account_list_input_payload)
    @api.marshal_with(get_account_list_output_payload)
    def post(self):
        try:
            Use_orlc = OracleAccess()
            sql = "SELECT * FROM KUO_add_account"
            val = Use_orlc.query(sql)
            data_list = []
            for i in val:
                test = 0
                data = {
                    "user_id": "",
                    "email": "",
                    "role": [],
                    "update_time": ""
                }
                for x in data:
                    if x == "role":
                        for y in range(3):
                            data["role"].append(i[test])
                            test += 1
                    else:
                        data[x] = i[test]
                        test += 1
                data_list.append(data)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": "", "data": data_list}
        finally:
            return msg


@api.route("/autosave_detect_table")  # 自動偵測儲存(以優化)
class Autosave_detect_table(CustomResource):
    @api.expect(autosave_detect_table_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            data_json = request.get_json()
            uuid = data_json.get('uuid', None)
            data = data_json.get('data', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            Use_orlc = OracleAccess()
            data_table_id = data["page_number"]["table_id"]
            data_table_id_cells = data_table_id["cells"][0]
            data_list = [uuid]
            for i in data_table_id:
                if i != "cells":
                    data_list.append(data_table_id[i])
                else:
                    for j in data_table_id_cells:
                        data_list.append(data_table_id_cells[j])
            sql = "INSERT INTO KUO_autosave_detect_table VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)"
            Use_orlc.insert(sql, data_list)
            Use_orlc.close()
        finally:
            return msg


@api.route("/get_detect_table")  # 自動偵測取得
class Get_detect_table(CustomResource):
    @api.expect(get_detect_input_payload)
    @api.marshal_with(get_detect_output_payload)
    def post(self):
        try:
            Use_orlc = OracleAccess()
            data_json = request.get_json()
            uuid = data_json.get('uuid', None)
            sql = "SELECT * FROM KUO_autosave_detect_table WHERE UUID='{}'".format(
                uuid)
            val = Use_orlc.query(sql)[0]
            data = {
                "page_number": {
                    "table_id": {
                        "upper_left": "",
                        "upper_right": "",
                        "lower_right": "",
                        "lower_left": "",
                        "cells": [
                            {
                                "name": "",
                                "upper_left": "",
                                "upper_right": "",
                                "lower_right": "",
                                "lower_left": "",
                                "start_row": "",
                                "end_row": "",
                                "start_col": "",
                                "end_col": "",
                                "content": ""
                            }
                        ]
                    }
                }
            }
            test = 1
            for i in data["page_number"]["table_id"]:
                if i != "cells":
                    data["page_number"]["table_id"][i] = val[test]
                    test += 1
                else:
                    for j in data["page_number"]["table_id"]["cells"][0]:
                        data["page_number"]["table_id"]["cells"][0][j] = val[test]
                        test += 1
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": "", "data": data}
        finally:
            return msg


@api.route("/autosave_key_value_mapping")  # 單元格偵測自動儲存
class Autosave_key_value_mapping(CustomResource):
    @api.expect(autosave_key_value_mapping_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            # 取得輸入資料
            data_json = request.get_json()
            data = data_json.get('data', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            Use_orlc = OracleAccess()
            field = data[0].get('field', None)
            fieldvalue = data[0].get('fieldvalue', None)
            vendor = data[0].get('vendor', None)
            file_type = data[0].get('file_type', None)
            fieldvalue_str = ",".join(fieldvalue)
            data_list = [field, fieldvalue_str, vendor, file_type]
            sql = "INSERT INTO Kuo_key_value VALUES (:1, :2, :3, :4)"
            Use_orlc.insert(sql, data_list)
            Use_orlc.close()
        finally:
            return msg


@api.route("/get_key_value_mapping")  # ERP Key-Value對照表API
class Get_key_value_mapping(CustomResource):
    @api.expect(get_key_value_mapping_input_payload)
    @api.marshal_with(get_key_value_mapping_output_payload)
    def post(self):
        try:
            Use_orlc = OracleAccess()
            data_json = request.get_json()
            data = data_json.get('data', None)
            vendor = data.get('vendor', None)
            file_type = data.get('file_type', None)
            if vendor == '' and file_type == '':
                sql = "SELECT * FROM Kuo_key_value WHERE VENDOR IS NULL AND FILE_TYPE IS NULL"
            elif vendor == '' and file_type != '':
                sql = "SELECT * FROM Kuo_key_value WHERE VENDOR IS NULL AND FILE_TYPE='{}'".format(
                    file_type)
            elif vendor != '' and file_type == '':
                sql = "SELECT * FROM Kuo_key_value WHERE VENDOR='{}' AND FILE_TYPE IS NULL".format(
                    vendor)
            else:
                sql = "SELECT * FROM Kuo_key_value WHERE VENDOR='{}' AND FILE_TYPE='{}'".format(
                    vendor, file_type)
            val = Use_orlc.query(sql)
            data_dict = {}
            for i in val:
                print(i[0])
                data_dict[i[0]] = [i[1]]
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": "", "data": data_dict}
        finally:
            return msg


@api.route("/autosave_image_path")  # 自動儲存圖片路徑
class Autosave_image_path(CustomResource):
    @api.expect(autosave_image_path_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        try:
            data_json = request.get_json()
            uuid = data_json.get('uuid', None)
            front_path = data_json.get('front_path', None)
            back_path = data_json.get('back_path', None)
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": ""}
            Use_orlc = OracleAccess()
            sql = """SELECT * FROM image_path WHERE UUID='{}'""".format(
                uuid)
            val = Use_orlc.query(sql)
            if val == []:
                data_list = [uuid, front_path, back_path]
                sql = "INSERT INTO image_path VALUES (:1, :2, :3)"
                Use_orlc.insert(sql, data_list)
            else:
                sql = "UPDATE image_path SET FRONT_PATH='{}', BACK_PATH='{}' WHERE UUID='{}'".format(
                    front_path, back_path, uuid)
                Use_orlc.update(sql)
            Use_orlc.close()
        finally:
            return msg


@api.route("/get_image_path")  # 取得圖片路徑
class Get_image_path(CustomResource):
    @api.expect(autosave_image_path_intput_payload)
    @api.marshal_with(autosave_image_path_output_payload)
    def post(self):
        try:
            Use_orlc = OracleAccess()
            data_json = request.get_json()
            uuid = data_json.get('uuid', None)
            sql = "SELECT * FROM image_path WHERE UUID='{}'".format(
                uuid)
            val = Use_orlc.query(sql)[0]
            print(val)
            data = {
                "uuid": "",
                "front_path": "",
                "back_path": ""
            }
            test = 0
            for i in data:
                data[i] = val[test]
                test += 1
        except Exception:
            msg = {"result": 1, "message": "error"}
        else:
            msg = {"result": 0, "message": "", "data": data}
        finally:
            return msg
