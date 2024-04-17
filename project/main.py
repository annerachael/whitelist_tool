from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import WhitelistedMSISDN, User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #renders the main index.html
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    #renders the users profile
    return render_template('profile.html', name=current_user.name)

@main.route('/add_msisdn_single', methods=['GET', 'POST'])
@login_required
def add_msisdn():
    #add only a single msisdn onto the database
    if request.method == 'POST':
        # If form submitted
        if 'msisdn' in request.form:
            msisdn = request.form['msisdn']
            service_line = request.form['service_line']
            new_msisdn = WhitelistedMSISDN(msisdn=msisdn, service_line=service_line)
            db.session.add(new_msisdn)
            db.session.commit()
            return redirect(url_for('main.profile'))
    return render_template('add_msisdn_single.html')

@main.route('/add_msisdn_bulk', methods=['GET', 'POST'])
@login_required
def add_msisdn_bulk():
    #add bulk msisdns from a file onto the database
    if request.method == 'POST':
        print(request.files)
        file = request.files.get('file')

        if file:
            # Check if the file has a txt extension
            if file.filename.endswith('.txt'):
                # Securely save the file
                filename = secure_filename(file.filename)
                file.save(f'project/uploads/{file.filename}')
                print("File saved successfully.")
                with open(f'project/uploads/{file.filename}', 'r') as f:
                    for line in f:
                        msisdn = line.strip()
                        service_line = request.form['service_line']
                        new_msisdn2 = WhitelistedMSISDN(msisdn=msisdn, service_line=service_line)
                        db.session.add(new_msisdn2)
                        db.session.commit()
                        flash('File uploaded and MSISDNs added successfully!', 'success')
                return redirect(url_for('main.profile'))

    return render_template('add_msisdn_bulk.html')

@main.route('/delete_msisdn', methods=['GET', 'POST'])
@login_required
def delete_msisdn():
    #delete a single msisdn from the database
    if request.method == 'POST':
        msisdn = request.form.get('msisdn')
        if msisdn:
            msisdn_to_delete = WhitelistedMSISDN.query.filter_by(msisdn=msisdn).first()
            if msisdn_to_delete:
                db.session.delete(msisdn_to_delete)
                db.session.commit()
                flash('MSISDN deleted successfully.', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('MSISDN not found.', 'error')
        else:
            flash('Please provide an MSISDN.', 'error')
    return render_template('delete_msisdn.html')

from flask import request

@main.route('/delete_msisdn_bulk', methods=['GET', 'POST'])
@login_required
def delete_msisdn_bulk():
    #delete bulk records of msisdns from the database
    if request.method == 'POST':
        # Process the uploaded file
        file = request.files.get('file')
        if file:
            # Check if the file has a txt extension
            if file.filename.endswith('.txt'):
                # Securely save the file
                filename = secure_filename(file.filename)
                file.save(f'project/uploads/{file.filename}')
                print("File saved successfully.")
                with open(f'project/uploads/{file.filename}', 'r') as f:
                    for line in f:
                        msisdn = line.strip()
                        # Delete MSISDN from the database
                        msisdn_to_delete = WhitelistedMSISDN.query.filter_by(msisdn=msisdn).first()
                        if msisdn_to_delete:
                            db.session.delete(msisdn_to_delete)
                            db.session.commit()
                # Delete the uploaded file after processing
                os.remove(f'project/uploads/{file.filename}')
                return redirect(url_for('main.profile'))
    return render_template('delete_bulk_msisdn.html')

@main.route('/view_whitelist/')
@login_required
def view_whitelist():
    # Add code here to fetch and display all whitelisted msisdns for each service
    msisdns = WhitelistedMSISDN.query.all()
    return render_template('view_whitelist.html', msisdns=msisdns)