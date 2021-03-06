from flask import render_template,request, redirect, url_for, flash, abort, session, jsonify,Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp= Blueprint('urlshort',__name__)

@bp.route('/')
def home():
    return render_template('home.html',codes=session.keys())

@bp.route('/your-url', methods=['GET','POST']) #methods is a list of methods you want to allow, if you dont specify it, it will give an error
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash("This short name has already been assigned. Please use another one.")
             #if the code already exists in the dictionary it will not be overwritten
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']} #for every key we have a value
        else:
            f=request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/abhinav/Desktop/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name} #for every key we have a value

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']]=True
        return render_template('your_url.html',code=request.form['code']) #request.args for get

    else:
        return redirect(url_for('urlshort.home')) #best out of all three
        #return redirect('/') # redirect because it is more helpful to the user, render_template will leave them confused
        #return render_template('home.html')

@bp.route('/<string:code>')
def redirect_to_code(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls=json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
