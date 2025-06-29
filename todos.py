from flask import Blueprint,Flask, request, session,jsonify
from models import User
from models import Task
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

todo = Blueprint("todo",__name__)


@todo.route("/todo",methods = ["GET","POST"])
@jwt_required()
def create_todo():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    user_id = get_jwt_identity()

    new_todo = Task(title=title, description=description, user_id=user_id)

    db.session.add(new_todo)
    db.session.commit()


    return jsonify({
        "id": new_todo.id,
        "title": new_todo.title,
        "description": new_todo.description
    }), 201

    



@todo.route("/todo/<int:task_id>",methods = ["PUT"])
@jwt_required()
def update(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id = task_id,user_id = user_id).first()

    if not task:
        return jsonify({"message": "Task not found or not authorized"}), 404
    
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")

    if title:
        task.title = title
    if description:
        task.description = description




    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description
    }), 200




@todo.route("/todo/<int:task_id>",methods = ["DELETE"])
@jwt_required()
def delete(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id = task_id,user_id = user_id).first()

    if not task:
        return jsonify({"message": "Task not found or not authorized"}), 404

    db.session.delete(task)

    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200

