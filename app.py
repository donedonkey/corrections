from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

errors = [
    {'incorrect sentence': 'Do you like cook?', 'correct sentence': ['Do you like to cook?']},
    {'incorrect sentence': 'It\'s depend of the person.', 'correct sentence': ['It depends on the person.']}
]

class ErrorsForm(FlaskForm):
    error = StringField("Error:", validators=[DataRequired()])
    correction = TextAreaField("Correction:", validators=[DataRequired()])
    submit = SubmitField("Add Sentences")

class EditForm(FlaskForm):
    error = StringField("Error:", validators=[DataRequired()])
    correction = TextAreaField("Correction:", validators=[DataRequired()])
    submit = SubmitField("Change Sentences")

class RemoveForm(FlaskForm):
    submit = SubmitField("Remove")

@app.route('/', methods=["GET", "POST"])
def index():
    form = ErrorsForm(csrf_enabled=False)
    if form.validate_on_submit():
        new_error = {}
        new_error['incorrect sentence'] = request.form['error']
        new_corrections = request.form['correction'].split('\n')
        new_error['correct sentence'] = new_corrections
        errors.append(new_error)
    return render_template('index.html', errors=errors, template_form=form)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm(csrf_enabled=False)
    if form.validate_on_submit():
        error_index = int(request.form['error_index'])
        new_error = request.form['error']
        new_corrections = request.form['correction'].split('\n')
        errors[error_index]['incorrect sentence'] = new_error
        errors[error_index]['correct sentence'] = new_corrections
    return render_template('edit.html', errors=errors, template_form=form, remove_form=RemoveForm())

@app.route('/remove_error', methods=['POST'])
def remove_error():
    remove_form = RemoveForm(csrf_enabled=False)
    if remove_form.validate_on_submit():
        remove_index = int(request.form['remove_index'])
        if 0 <= remove_index < len(errors):
            del errors[remove_index]
    return redirect(url_for('edit'))