# -*- coding: UTF-8 -*-
# from base_api.api_blueprint import api, api_blueprint
from base_api.custom_cls import CustomMethodView, CustomRequestParser, CustomResource
from flask import Blueprint, Flask, request, session
from utils.orcl_utils import OracleAccess
from flask_mail import Mail, Message
from .custom_cls import Api
from apis.account.api import api as account_ns

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, version="0.0.1", description='',
          title='Kuohwa API Service', doc="/doc")

# init db
OracleAccess.initialise()

# init app
app = Flask(__name__, template_folder="../templates",
            static_folder="../static", static_url_path="")
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config.SWAGGER_UI_REQUEST_DURATION = True
app.secret_key = "test123456789"
app.config['JSON_AS_ASCII'] = False
# app.config['SESSION_CRYPTO_KEY'] = load_aes_key()
# app.config["SESSION_COOKIE_HTTPONLY"] = True
# app.session_interface = EncryptedSessionInterface()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PROT'] = 465
app.config['MAIL_USERNAME'] = 'will901024@gmail.com'
app.config['MAIL_PASSWORD'] = 'tbbnxutumrlblbry'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEBUG'] = True
mail = Mail(app)

# register blueprint
app.register_blueprint(api_blueprint)

# register swagger api
api.add_namespace(account_ns)

# # namespace
# account_api = api.namespace("account", description=u"帳號及權限管理")
# table_api = api.namespace("table", description=u"表格偵測結構")
# cell_api = api.namespace("cell", description=u"單元格類型標記")
# orc_api = api.namespace("orc", description=u"ORC文字辨識")
# history_api = api.namespace("history", description=u"歷史編輯紀錄")


def send_mail(user_id, title, content):  # 我的寄信function
    print("ID:{},Title:{},Content{}".format(user_id, title, content))
    print(type(user_id))
    print(type(title))
    print(type(content))
    msg = Message(title, sender='server@gmail.com', recipients=[user_id])
    print("成功1")
    msg.body = "使用者 {} 您好，您的密碼為: {} ".format(user_id, content)
    print("成功2")
    mail.send(msg)
    print("寄信成功")
    return "OK"
