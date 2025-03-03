from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ui_library.db'

db = SQLAlchemy()
admin = Admin()
ckeditor = CKEditor(app)

class MyForm(FlaskForm):
    name = StringField('name')
    code = CKEditorField('code')
    tailwind = StringField('tailwind')
    inspiration = StringField('inspiration')
    inspiration_link = StringField('inspiration_link')
    category = StringField('category')
    tags = StringField('tags')
    submit = SubmitField('Submit')

class UI_Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(1000))
    tailwind = db.Column(db.String(1000))
    inspiration = db.Column(db.String(50))
    inspiration_link = db.Column(db.String(500))
    category = db.Column(db.String(50))
    tags = db.Column(db.String(500))

admin.add_view(ModelView(UI_Library, db.session))

@app.route("/",methods=['GET', 'POST'])
def index():
    u = UI_Library.query.all()
    form = MyForm()
    if form.validate_on_submit():
        # Create a new UI_Library entry
        new_entry = UI_Library(
            name=form.name.data,
            code=form.code.data,
            tailwind=form.tailwind.data,
            inspiration=form.inspiration.data,
            inspiration_link=form.inspiration_link.data,
            category=form.category.data,
            tags=form.tags.data
        )

        # Add and commit to the database
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for("index"))


    return render_template('home.html', u=u,  form = form)

if __name__ == '__main__':
    # app.app_context().push()

    db.init_app(app)
    # db.create_all()
    admin.init_app(app)
    app.run(debug=True)
