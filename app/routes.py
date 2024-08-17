from flask import Blueprint, render_template, jsonify, session, redirect, url_for

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/courses', methods=['GET'])
def get_courses():
    if 'username' in session:
        from app import mongo  # Flytt importen her
        courses = list(mongo.db.courses.find())
        return jsonify(courses)
    return redirect(url_for('auth.login'))