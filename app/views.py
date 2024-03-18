import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import UploadForm
from werkzeug.security import check_password_hash
from flask import send_from_directory

###
# Routing for your application.
###
def get_uploaded_image():
    uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'])
    uploaded_images = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    return uploaded_images

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     form = UploadForm()

#     if form.validate_on_submit():
#         f = form.image.data
#         filename = secure_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         flash('File Saved', 'success')
#         return redirect(url_for('home'))  # or some route where you display images

#     return render_template('upload.html', form=form)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/files')
def files():
    images = get_uploaded_image()
    return render_template('files.html', images= images)

@app.route('/properties/create', methods=['POST', 'GET'])
def create_properties():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        num_rooms = request.form['num_rooms']
        num_bathrooms = request.form['num_bathrooms']
        price = request.form['price']
        property_type = request.form['type']
        location = request.form['location']
        photo = request.files['photo']
        
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            
            # Create new Property instance
            new_property = Property(
                title=title, 
                description=description, 
                num_rooms=num_rooms, 
                num_bathrooms=num_bathrooms, 
                price=price.replace('$', '').replace(',', ''), 
                type=property_type, 
                location=location, 
                photo=filename  # Store the filename, not the full path
            )
            
            # Add new Property to database
            db.session.add(new_property)
            db.session.commit()

            flash('Property added successfully!', 'success')
            return redirect(url_for('home'))  # Redirect to home or any other page

        else:
            flash('You must upload a photo.', 'danger')

    return render_template('upload.html')  # or the template that contains the form

@app.route('/properties')
def properties():
    # Query all the properties from the database
    property_list = Property.query.all()
    # Render a template and pass the properties to it
    return render_template('properties.html', properties=property_list)

@app.route('/properties/<int:property_id>')
def property_detail(property_id):
    # Query the specific property from the database using its ID
    property = Property.query.get_or_404(property_id)
    # Render the detailed property view template with the property data
    return render_template('property.html', property=property)
