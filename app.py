from functools import wraps

from flask import Flask, render_template, request, url_for,\
    redirect, flash, make_response

from auth.crypting import aes_encrypt, aes_decrypt
from auth.model import User, AnonymousUser
from data.data_processing import add_prereqs

app = Flask(__name__)
app.secret_key = '4527e79a-17ef-4749-8dd4-7699e589e2b8'


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
    r = make_response(redirect(url_for('search_courses')))
    r.set_cookie('url', aes_encrypt(url))
    r.set_cookie('year', '2018W1')
    r.set_cookie('term', '1')
    r.set_cookie('campus', 'UBC')
    return r


@app.route('/search_courses')
@login_required
def search_courses():
    return render_template('search_courses.html')


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
