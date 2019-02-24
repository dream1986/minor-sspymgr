# -*- coding: utf-8 -*-
from sspymgr import db, createLogger
from sqlalchemy.sql import text
from base64 import b64decode

logger = createLogger('plugin_settings', stream=False, logger_prefix="[Plugin Settings]")

class WebguiSetting( db.Model ):
    """
    Type (can be ignored, just used as utility):
        String: Value type by default, should be processed by other logic
        Image: Value are encoded with base64 format
        Number: Treat value as number( use float builtin function), 
        Boolean: are stored in number with only two candicates (0 or 1)
        Json: Value are encoded with json format
        Hidden: Not visible for even manager
    """
    __tablename__ = 'webguiSetting'
    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    key = db.Column( db.String( 255 ), unique = True )
    value = db.Column( db.Text )
    type = db.Column( db.String( 32 ), default = 'String' )

    def getTypedValue( self ):
        if not self.type:
            return self.value
        if self.type == 'Boolean':
            return self.value == '1'
        if self.type == 'Number':
            try:
                return int( self.value )
            except Exception:
                return float( self.value )
        return self.value
    
    @staticmethod
    def count():
        sql = 'SELECT count(*) FROM %s' % WebguiSetting.__tablename__
        res = db.engine.execute( text( sql ) ).first()
        return res[ 0 ]

    @staticmethod
    def getSetting(key, default_value=None, default_type="String"):
        setting = WebguiSetting.query.filter_by(key=key).first()
        if setting is None and default_value is not None :
            setting = WebguiSetting(key=key, value=default_value, type=default_type)
            db.session.add(setting)
            db.session.commit()
        return setting

    def to_dict(self):
        di = {
            'id': self.id,
            'key': self.key,
            'value': self.value if type(self.value) is str else self.value.decode() ,
            'type': self.type,
        }
        return di

def init_webgui_setting():
    """
    alipay_enabled: bool default false
    wechatpay_enabled: bool default false
    alipay_qrcode: image data with base64 encode
    wechatpay_qrcode: image data with base64 encode
    signup_enabled: bool default true
    signup_without_invitation: int  default 8
    signup_email_limit: int  default 2
    shadowsock_port_range_start: Number default '50000'
    """
    if WebguiSetting.count() != 0:
        return
    settings = [
        ( "alipay_enabled",    "0", "Boolean" ),
        ( "wechatpay_enabled", "0", "Boolean" ),
        ( "signup_enabled", "1", "Boolean" ),
        ( "signup_without_invitation", "8", "Number" ),
        ( "signup_email_limit", "2", "Number" ),
        ( "shadowsock_port_range_start", "45000", "Number" ),
    ]
    for setting in settings:
        wgs = WebguiSetting( key = setting[0], value = setting[1], type = setting[2] )
        db.session.add( wgs )
    
    db.session.commit()

def init(app):
    app.m_events.on('beforeRegisterApi', registerApi)
    init_webgui_setting()
    logger.debug("inited")

from flask import jsonify

def registerApi(api):
    # TODO change setting item
    @api.route_admin('/setting/getAll', methods=['POST'])
    def get_all_settings():
        all = WebguiSetting.query.all()
        settings = [s.to_dict() for s in all]
        # for s in all:
        #     settings.append(s.to_dict())
        return jsonify({
            'status': 'success',
            'setting': settings
        })
    logger.debug("api registered.")