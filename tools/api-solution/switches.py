import json
from flask import Blueprint, jsonify, request
from models import Switch, db

switches_blueprint = Blueprint('switches', __name__)

@switches_blueprint.route('', methods=['POST'])
def create():
    data: dict = request.get_json()

    try:
        data["ports"] = str(json.dumps(data["ports"]))
        data["interfaces"] = str(json.dumps(data["interfaces"]))
        switch = Switch(**data)
        db.session.add(switch)
        db.session.commit()
        return jsonify(switch.serialize()), 201
    except KeyError as k:
        return {"message": f"missing property key: {k}"}, 400

@switches_blueprint.route('/', methods=['GET'])
def get_all():
    switches = Switch.query.all()
    return jsonify([switch.serialize() for switch in switches])  

@switches_blueprint.route('/<id>', methods=['GET'])
def one(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400
    # search by id
    switch = Switch.query.filter_by(id=int(id)).first()

    # return not found if not exists
    if switch is None: 
        return jsonify({
            'error': 'not found'
        }), 404

    return jsonify(switch.serialize())


@switches_blueprint.route('/<id>', methods=['DELETE'])
def delete(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400

    switch = Switch.query.filter_by(id=int(id)).delete()
    db.session.commit()

    if switch == 0:
        return jsonify({
            'error': 'not found'
        }), 404

    return '', 204

@switches_blueprint.route('/<id>', methods=['PUT'])
def update(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400
    
    data: dict = request.get_json()

    # search by id
    switch = Switch.query.filter_by(id=int(id)).first()

    # return not found if not exists
    if switch is None: 
        return jsonify({
            'error': 'not found'
        }), 404
    
    try:

        # update fields
        switch.motd = data["motd"]
        switch.hostname = data["hostname"]
        switch.interfaces =  str(json.dumps(data["interfaces"]))
        switch.ports =  str(json.dumps(data["ports"]))

    except KeyError as k:
        return {"message": f"missing property key: {k}"}, 400

    # save result
    db.session.add(switch)
    db.session.commit()

    return jsonify(switch.serialize()), 200
