# -*- coding: utf-8 -*-
"""Description: This module is used for providing api interface for both admin and user frontend.
When providing apis with normal users, use decorator ``api.route_user``, 
while providing apis with administrator, use decorator ``api.route_admin``
It also provides a convinient function getPageArgs for requesting paged information.

Author: BriFuture

Modified: 2019/03/10 19:33
"""

from flask import Blueprint, request

api = Blueprint('api', __name__)

from datetime import timedelta, datetime
from functools import wraps
from flask import session, jsonify


def identify_user(func):
    """judge whether a user has signed in or not, 
    if he has signed in and he is administrator, redirect the page to admin_index
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'status': 'Bad Request'})
        return func(*args, **kwargs)

    return wrapper


def user_route(rule, methods):
    def __user_route(func):
        @api.route('/user{}'.format(rule), methods=methods)
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'status': 'Bad Request'})
            return func(*args, **kwargs)

        return wrapper

    return __user_route


api.route_user = user_route

from . import isManager

def identify_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isManager():
            # no need to redirect to similar page because there may be no such page for admin
            return jsonify({'status': 'Bad Request'})
        return func(*args, **kwargs)

    return wrapper


def admin_route(rule, methods):
    def __admin_route(func):
        @api.route('/admin{}'.format(rule), methods=methods)
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isManager():
                # no need to redirect to similar page because there may be no such page for admin
                return jsonify({'status': 'Bad Request'})
            return func(*args, **kwargs)

        return wrapper

    return __admin_route


api.route_admin = admin_route

from flask import request


def getPageArgs():
    page = request.form.get('page', 1)
    per_page = request.form.get('perPage', 20)
    try:
        page = int(page)
        per_page = int(per_page)
    except:
        page = 1
        per_page = 20
    return page, per_page


api.getPageArgs = getPageArgs
