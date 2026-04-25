import json
from flask import Blueprint, jsonify, request
from models import Router, db

router_blueprint = Blueprint('routers', __name__)

@router_blueprint.route('', methods=['POST'])
def create():
    data: dict = request.get_json()

    try:
        data["interfaces"] = str(json.dumps(data["interfaces"]))

        router = Router(**data)

        db.session.add(router)
        db.session.commit()

        return jsonify(router.serialize()), 201

    except KeyError as k:
        return {"message": f"missing property key: {k}"}, 400


@router_blueprint.route('', methods=['GET'])
def get_all():
    routers = Router.query.all()
    return jsonify([router.serialize() for router in routers]) 

@router_blueprint.route('/<id>', methods=['GET'])
def one(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400
    # search by id
    router = Router.query.filter_by(id=int(id)).first()

    # return not found if not exists
    if router is None: 
        return jsonify({
            'error': 'not found'
        }), 404

    return jsonify(router.serialize())

@router_blueprint.route('/<id>', methods=['DELETE'])
def delete(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400

    router = Router.query.filter_by(id=int(id)).delete()
    db.session.commit()

    if router == 0:
        return jsonify({
            'error': 'not found'
        }), 404

    return '', 204

@router_blueprint.route('/<id>', methods=['PUT'])
def update(id: str):
    if not id.isdigit():
        return jsonify({
            'error': 'id must be an integer'
        }), 400
    
    data: dict = request.get_json()

    # search by id
    router = Router.query.filter_by(id=int(id)).first()

    # return not found if not exists
    if router is None: 
        return jsonify({
            'error': 'not found'
        }), 404
    
    try:

        # update fields
        router.motd = data["motd"]
        router.hostname = data["hostname"]
        router.interfaces =  str(json.dumps(data["interfaces"]))

    except KeyError as k:
        return {"message": f"missing property key: {k}"}, 400

    # save result
    db.session.add(router)
    db.session.commit()

    return jsonify(router.serialize()), 200
