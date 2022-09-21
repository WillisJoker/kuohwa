from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})

base_output_payload = api.model(u'基礎輸出參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})

account_output_payload = api.clone(u'帳號output', base_input_payload, {
    'data': fields.String(required=True),
    "test": fields.String(required=True)
})

forget_Api_input_payload = api.model(u'忘記input', {
    'user_id': fields.String(required=True, example="will901024@gmail.com")})

add_input_payload = api.model(u'新增input', {
    'user_id': fields.String(required=True, example="account"),
    'role': fields.String(required=True, example=["super user", "admin", "general user"]),
    'email': fields.String(required=True, example="account@mail.com")
})

delete_input_payload = api.model(u'刪除input', {
    'user_id': fields.String(required=True, example="account")})

update_input_payload = api.model(u'更新input', {
    'old_user_id': fields.String(required=True, example="account"),
    'data': fields.String(required=True, example={"new_user_id": "new_account",
                                                  "new_role": ["super user", "admin", "general user"],
                                                  "new_email": "new_account@mail.com"})
})

get_account_list_input_payload = api.model(u'取得input', {})

get_account_list_output_payload = api.model(u'取得output', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data': fields.String(required=True, example=[{"user_id": "", "role": ["super user", "admin"], "email": "", "update_time":""}]), })

autosave_detect_table_input_payload = api.model(u'自動更新儲存input', {
    'uuid': fields.String(required=True, example="sa5e122hy215cb3degrt"),
    'data': fields.String(required=True, example={
        "page_number": {
            "table_id": {
                "upper_left": "99,82",
                "upper_right": "99,857",
                "lower_right": "2356,857",
                "lower_left": "2356,82",
                "cells": [
                    {
                        "name": "cell_id1",
                        "upper_left": "99,82",
                        "upper_right": "99,857",
                        "lower_right": "2356,857",
                        "lower_left": "2356,82",
                        "start_row": 0,
                        "end_row": 2,
                        "start_col": 0,
                        "end_col": 3,
                        "content": "example"
                    }
                ]
            }
        }
    }
    )
}
)

get_detect_input_payload = api.model(u'表格偵測input', {
    'uuid': fields.String(required=True, example="sa5e122hy215cb3degrt")})

get_detect_output_payload = api.model(u'表格偵測output', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data': fields.String(required=True, example={
        "page_number": {
            "table_id": {
                "upper_left": "99,82",
                "upper_right": "99,857",
                "lower_right": "2356,857",
                "lower_left": "2356,82",
                "cells": [
                    {
                        "name": "cell_id1",
                        "upper_left": "99,82",
                        "upper_right": "99,857",
                        "lower_right": "2356,857",
                        "lower_left": "2356,82",
                        "start_row": 0,
                        "end_row": 2,
                        "start_col": 0,
                        "end_col": 3,
                        "content": "example"
                    }
                ]
            }
        }
    }
    ),
}
)

autosave_key_value_mapping_input_payload = api.model(u'單元格偵測自動儲存input', {
    'data': fields.String(required=True, example=[
        {
            "field": "epr_key1",
            "fieldvalue": [
                "Bo",
                "Borad"
            ],
            "vendor":"",
            "file_type":""
        }
    ]
    )})

get_key_value_mapping_input_payload = api.model(u'ERP Key-Value對照表input', {
    'data': fields.String(required=True, example={
        "vendor": '',
        "file_type": ''
    }
    )}
)

get_key_value_mapping_output_payload = api.model(u'ERP Key-Value對照表output', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data': fields.String(required=True, example={"epr_key1": [
        "Bo",
        "Borad",
        "Boardnum"
    ],
        "epr_key2": [
        "sta",
        "status",
        "status1"
    ]
    }
    )}
)

autosave_image_path_input_payload = api.model(u'自動儲存圖片路徑input', {
    'uuid': fields.String(required=True, example=" "),
    'front_path': fields.String(required=True, example=" "),
    'back_path': fields.String(required=True, example=" ")
}
)
autosave_image_path_intput_payload = api.model(u'取得自動儲存圖片路徑input', {
    'uuid': fields.String(required=True, example=" ")
}
)

autosave_image_path_output_payload = api.model(u'取得自動儲存圖片路徑output', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data': fields.String(required=True, example={"uuid": "",
                                                  "front_path": "",
                                                  "back_path": ""})
}
)
