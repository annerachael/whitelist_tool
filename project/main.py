from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import WhitelistedMSISDN, User
from . import db

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():

    return render_template('profile.html', name=current_user.name)

@main.route('/add_msisdn', methods=['GET', 'POST'])
@login_required
def add_msisdn():
    if request.method == 'POST':
        # If form submitted
        if 'msisdn' in request.form:
            msisdn = request.form['msisdn']
            service_line = request.form['service_line']
            # Add code to whitelist the msisdn for the selected service


            new_msisdn = WhitelistedMSISDN(msisdn=msisdn, service_line=service_line)
            db.session.add(new_msisdn)
            db.session.commit()

            flash('MSISDN added successfully!', 'success')
            return redirect(url_for('main.profile'))

        # If file uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                # Process the uploaded file to add MSISDNs to the database
                with open(file_path, 'r') as f:
                    for line in f:
                        msisdn = line.strip()
                        service_line = request.form['service_line']

                        new_msisdn2 = WhitelistedMSISDN(msisdn=msisdn, service_line=service_line)
                        db.session.add_all(new_msisdn2)
                        db.session.commit()
                        # Add code to whitelist the msisdn for the selected service
                flash('File uploaded and MSISDNs added successfully!', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid file type', 'error')
                return redirect(request.url)
    return render_template('add_msisdn.html')

@main.route('/delete_msisdn/<int:msisdn_id>', methods=['POST'])
@login_required
def delete_msisdn(msisdn_id):
    # Add code here to delete the msisdn with the given ID
    flash('MSISDN deleted successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/view_whitelist/')
@login_required
def view_whitelist():
    # Add code here to fetch and display all whitelisted msisdns for each service
    msisdns = WhitelistedMSISDN.query.all()
    return render_template('view_whitelist.html', msisdns=msisdns)



