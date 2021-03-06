# -*- coding: utf-8 -*-
"""Description: replace sessions location, all neccessary session information will
be stored in database on your server. So it may be safer to store information within
session. It will clear all expired session record in database every time the SSPYMGR
starts (not interval check so the number of records may get bigger and bigger, it 
will be fixed some other time)

Author: BriFuture

Modified: 2019/03/10 20:07
"""

from .models import DB
from flask.sessions import SessionMixin, SessionInterface
from werkzeug import CallbackDict
from uuid import uuid4
from datetime import timedelta, datetime

class Sessions( DB.Model ):
    __tablename__ = 'sessions'
    sid = DB.Column( DB.String( 255 ), primary_key = True )
    expired = DB.Column( DB.DateTime )
    session = DB.Column( DB.Text )

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )
        if 'sid' in kwargs:
            self.sid = kwargs[ 'sid' ]
        
        if 'expired' in kwargs:
            self.expired = kwargs[ 'expired' ]
        else:
            self.expired = datetime.now() + timedelta( minutes = 10 ) # from now

        if 'session' in kwargs:
            self.session = kwargs[ 'session' ]

    def __repr__( self ):
        return '<Session %s %s %s>' % ( self.sid, self.session, self.expired )

class DbSession( CallbackDict, SessionMixin ):
    def __init__( self, initial = None, sid = None, new = False ):
        def on_update( self ):
            self.modified = True

        CallbackDict.__init__( self, initial, on_update )
        self.sid = sid
        self.new = new
        self.modified = False

# def total_seconds( days, seconds = 0 ):
#     return days * 60 * 60 * 24 + seconds
import json

class DatabaseSessionInterface( SessionInterface ):
    serializer = json
    session_class = DbSession

    def __init__( self, database, prefix = 'session:' ):
        self.db = database
        self.prefix = prefix

    def generate_sid( self ):
        return str( uuid4() )
    
    def get_expiration_time( self, app, session ):
        if session.permanent:
            return datetime.now() + app.permanent_session_lifetime
        
        # keep session for 10 minutes
        return datetime.now() + timedelta( minutes = 10 )

    def open_session( self, app, request ):
        sid = request.cookies.get( app.session_cookie_name ) # 尝试从请求中获取存储的 cookie（与 session 相关的 cookie）
        if not sid:
            # 没有从 cookie 中找到相关 sid，说明客户端是第一次访问，需要构造 sid
            sid = self.generate_sid()
            # create new Session representation
            dbrecord = Sessions( sid = sid )
            # db.session.add( dbrecord )
            sc = self.session_class( sid = sid, new = True )
            # print( 'open_new: ', dbrecord, sc.new )
            return sc
        
        # if client have a session_cookie, take relative one from database
        dbrecord = Sessions.query.filter_by( sid = sid ).first()
        
        # print( "open: ", dbrecord )

        if dbrecord is None:
            return self.session_class( sid = sid ) # in case of wrong sid in session_cookie
        else:
            return self.session_class( self.serializer.loads( dbrecord.session ), sid = sid )

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain( app )
        # print( "save ", session, dbrecord )
        # print( 'save new ', session.new )
        dbrecord = Sessions.query.filter_by( sid = session.sid ).first()
        if not session:  
            # session content is empty
            if session.modified:
                # execute deletion if session is empty but modified
                self.db.session.delete( dbrecord )
                self.db.session.commit()
                response.delete_cookie( app.session_cookie_name, domain = domain )

            return 
        
        # update or insert
        if dbrecord is None:
            # in case database is clean
            dbrecord = Sessions( sid = session.sid )
            self.db.session.add( dbrecord )
            
        dbrecord.session = self.serializer.dumps( session )
        sexp = self.get_expiration_time( app, session )
        dbrecord.expired = sexp
        # print( "save:", dbrecord )
        self.db.session.commit()
        response.set_cookie( app.session_cookie_name, session.sid,
            expires = sexp, httponly = True, domain = domain )

import hashlib
from .globalfuncs import getRandomCode

def clearExpired(db):
    now = datetime.now()
    Sessions.query.filter(now > Sessions.expired).delete()
    db.session.commit()
   
def replaceSessionInterface(app):
    app.session_interface = DatabaseSessionInterface( database = app.m_db )
    # app.secret_key = hashlib.sha1( getRandomCode( 24 ).encode() ).hexdigest()
    app.m_events.on('afterCreateDb', clearExpired)
    app.secret_key = hashlib.sha1( 'test'.encode() ).hexdigest()