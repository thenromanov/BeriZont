from flask import jsonify
from flask_restful import abort, Resource
from data import dbSession
from data.devices import Device
from .devicesParser import parser


class DevicesResource(Resource):
    def get(self):
        args = parser.parse_args()
        session = dbSession.createSession()
        device = session.query(Device).get(args['id'])
        if not device:
            abort(404, message='Wrong id')
        return jsonify({'state': device.state})
    

    def post(self):
        session = dbSession.createSession()
        device = Device(state=False, count=0)
        session.add(device)
        session.commit()
        return 200
    

    def put(self):
        args = parser.parse_args()
        session = dbSession.createSession()
        device = session.query(Device).get(args['id'])
        if not device:
            abort(404, message='Wrong id')
        device.state = False
        session.commit()
        return 200