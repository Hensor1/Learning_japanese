from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request, flash
from bson import ObjectId
from .auth import admin_required

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/courses', methods=['GET'])
def get_courses():
    if 'username' in session:
        #Importing mongo here to avoid circular dependecies
        from app import mongo
        # Getting course from mongo
        courses = list(mongo.db.courses.find())
        return render_template('courses.html', courses=courses)
    else:
        flash('You have to log in to see courses', 'warning')
        return redirect(url_for('auth.login'))


@main_blueprint.route('/courses/new', methods=['GET', 'POST'])
@admin_required
def create_course():
    from app import mongo
    if request.method == 'POST':
        course_name = request.form.get('name')
        description = request.form.get('description')
        
        if course_name and description:
            # Adding course in mongo
            mongo.db.courses.insert_one({'name': course_name, 'description': description})
            flash('Course created!', 'success')
            return redirect(url_for('main.get_courses'))
        else:
            flash('All fields must be populated', 'danger')
    
    return render_template('create_course.html')

@main_blueprint.route('/courses/edit/<course_id>', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    from app import mongo
    course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_description = request.form.get('description')

        if new_name and new_description:
            mongo.db.courses.update_one(
                {'_id': ObjectId(course_id)},
                {'$set': {'name': new_name, 'description': new_description}}
            )
            flash('Course updated!', 'success')
            return redirect(url_for('main.get_courses'))
        else:
            flash('All fields must be populated', 'danger')

    return render_template('edit_course.html', course=course)

@main_blueprint.route('/courses/delete/<course_id>', methods=['GET', 'POST'])
@admin_required
def delete_course(course_id):
    from app import mongo
    mongo.db.courses.delete_one({'_id': ObjectId(course_id)})
    flash('Course deleted!', 'success')
    return redirect(url_for('main.get_courses'))

