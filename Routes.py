from hms import app
from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, session
from .Forms import Login_form,Patient_create,Patient_delete
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from .Config import db



@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def main():
    if session.get('username'):
        return render_template('index.html', user=session['username'])
    form = Login_form()
    if request.method == 'POST':
        # Validate the form
        if form.validate_on_submit():
            # Check the credentials
            if request.form.get('username') == '12345678@A' and request.form.get('password') == '12345678@A':
                flash("Login successful","success")
                #g.user = "Admin"
                session['username'] = request.form.get('username')
                return redirect(url_for('create_patient'))
            else:
                flash("Invalid credentials","danger")
                return render_template('login.html', alert='failed', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/CreatePatient", methods=['GET', 'POST'])
def create_patient():
    if 'username' not in session or not session['username']:
        flash('Please Login first!','danger')
        return redirect('login')
    # If form has been submitted
    form=Patient_create()
    if request.method == 'POST':
        if form.validate_on_submit():
            ssn_id = form.ssn_id.data
            name = form.patient_name.data
            age = form.patient_age.data
            date = form.date.data
            bed_type = form.Type_of_bed.data
            address = form.address.data
            state = request.form.get('state_list')
            city = request.form.get('stt')
            #create_p([ssn_id, name, age, date, bed_type, address, state, city])
            details = Patient_details(
                name, age, ssn_id, date, bed_type, address, city, state, status="Admitted")
            db.session.add(details)
            db.session.commit()
            flash("Patient Succefully Registered","Success")
    return render_template("create_patient.html", title="Create Patient",form=form)


@app.route("/DeletePatient",methods=["GET","POST"])
def delete_patient():
    if 'username' not in session:
        return redirect('login')
    form=Patient_delete()
    if form.validate_on_submit():
        flash("patient found","success")
    

        
    return render_template("delete_patient.html", title="Delete Patient",form=form)


@app.route("/UpdatePatient")
def update_patient():
    if 'username' not in session:
        return redirect('login')
    return render_template("update_patient.html", title="Update Patient")


@app.route("/logout")
def logout():
    if session['username']:
        #return render_template('index.html', user=session['username'])
        session['username'] = None
        return redirect(url_for('main'))