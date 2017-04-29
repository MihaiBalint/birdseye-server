# -*- coding: utf-8 -*-
'''
Conventions
-----------

* Unless otherwise specified, the response is always a JSON object
* A successful response is always a dictionary with the following keys: \
'status', 'count', 'data' (in this order). Example:

.. code:: Javascript

    {
      "status": "success",
      "count": "1",
      "data": ["AnImportantValue"]
    }

* An error response is always a dictionary with the following keys: \
'status', 'message'. Example:

.. code:: Javascript

    {
      "status": "error",
      "message": "Not Found"
    }

'''
from flask import request
from flask_restful import Resource, Api, representations
import types
from birdseye import app, db
import birdseye.models as bm


api = Api(app)
representations.json.settings = {'indent': 4}


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)


def not_found():
    return {'status': 'error', 'message': 'Found no matches'}, 404


@api.route('/v1/users')
class Users(Resource):

    def post(self):
        data = request.get_json()
        user = bm.User(data['credentials'], data['secret'])
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return {'status': 'success', 'count': '1', 'data': [user.user_id]}, 201

    def get(self):
        # TODO: check admin
        users = bm.User.find_all()
        return {'status': 'success', 'count': str(len(users)), 'data': [
            u.as_public_dict for u in users]}

    def delete(self):
        # TODO: check admin
        count = bm.User.delete_all()
        return {'status': 'success', 'count': '1', 'data': [count]}


@api.route('/v1/users/{user_id}')
class User(Resource):

    def get(self, user_id):
        # TODO: check session
        user = bm.User.find_by_id(user_id)
        return {'status': 'success', 'count': '1', 'data': [
            user.as_public_dict()]}


@api.route('/v1/sessions')
class Sessions(Resource):

    def post(self):
        data = request.get_json()
        user = bm.User.find_by_credentials(
            data['credentials'], data['secret']).first()
        if user is None:
            return {'status': 'error', 'message': 'No user.'}, 403
        ses = bm.Session(user, data.get('tokens'))
        db.session.add(ses)
        db.session.commit()
        db.session.refresh(ses)
        return {'status': 'success', 'count': '1', 'data': [ses.session_id]}

    def delete(self):
        # TODO: Admin
        count = bm.Session.delete_all()
        db.session.commit()
        return {'status': 'success', 'count': '1', 'data': [count]}


@api.route('/v1/sessions/{session_id}')
class Session(Resource):

    def get(self, session_id):
        # TODO: check session
        session = bm.Session.find_by_id(session_id)
        return {'status': 'success', 'count': '1', 'data': [
            session.as_public_dict()]}

    def delete(self, session_id):
        # TODO: check session
        count = bm.Session.delete(session_id)
        return {'status': 'success', 'count': '1', 'data': [count]}


@api.route('/v1/observations/{observation_id}')
class Observation(Resource):

    def get(self, observation_id):
        return []

    def put(self, observation_id):
        return


@api.route('/v1/observations')
class Observations(Resource):

    def get(self):
        return []

    def post(self):
        return {}

    def delete(self):
        count = bm.Observation.delete_all()
        return {'status': 'success', 'count': '1', 'data': [count]}


def noqa():
    pass
