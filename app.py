from functools import wraps

from flask import Flask, render_template, request, url_for,\
    redirect, flash, make_response
from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField, BooleanField
from wtforms import validators

from auth.crypting import aes_encrypt, aes_decrypt
from auth.model import User, AnonymousUser
from data.data_processing import add_prereqs
from data.user_pre_reqs import fill_user_prereq
from data.select_all_sections import select_all_sections

app = Flask(__name__)
app.secret_key = '4527e79a-17ef-4749-8dd4-7699e589e2b8'


class URLForm(Form):
    url = StringField('URL to Google Spreadsheet', [validators.Length(min=10, max=55)])


class SearchForm(Form):
    subject_code = StringField('Subject code', [validators.Length(min=3, max=5)])
    course_number = StringField('Section number', [validators.Length(min=3, max=3)])


@app.before_request
def get_current_user():
    encrypted_url = request.cookies.get('url')
    try:
        request.user = User(aes_decrypt(encrypted_url))
    except:
        request.user = AnonymousUser()


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not request.user.is_authenticated():
            r = make_response(redirect(url_for('getting_started')))
            r.delete_cookie('url')
            flash('Please enter the link to Google Spreadsheet')
            return r
        else:
            return func(*args, **kwargs)
    return wrapped


@app.route('/')
@app.route('/getting_started')
def getting_started():
    return render_template('getting_started.html')


@app.route('/getting_started/processing', methods=["POST"])
def login_processing():
    url = request.form['url']
    print(f'url is {url}')
    r = make_response(redirect(url_for('search_courses')))
    r.set_cookie('url', aes_encrypt(url))
    r.set_cookie('year', '2018W1')
    r.set_cookie('term', '1')
    r.set_cookie('campus', 'UBC')
    fill_user_prereq(url=url)
    return r


@app.route('/search_courses')
@login_required
def search_courses():
    searchform = SearchForm(request.form)
    return render_template('search_courses.html', searchform=searchform)


@app.route('/view_course')
@login_required
def view_course():
    subject_code = request.args.get('subject_code')
    course_number = request.args.get('course_number')
    courses = select_all_sections(subject_code, course_number)
    if not courses:
        flash('No such courses found!')
        return redirect(url_for('search_courses'))
    return render_template('view_course.html', courses=courses)


@app.route('/update_course_calendar')
def update_course_calendar():
    return render_template('update_course_calendar.html')


@app.route('/update_course_calendar/processing', methods=['POST'])
def update_course_calendar_processing():
    add_prereqs()
    return redirect(url_for('search_courses'))


@app.route('/credentials')
def credentials():
    return 'Thank you!'


if __name__ == '__main__':
    app.run()
