import os
from flask import render_template, flash, request, redirect, url_for, session
from flask import send_from_directory, abort
from jarbegone import app, cache
from .forms import FileForm, SummaryConfigForm
from .scripts import utils
from .scripts.textrank import TextRank

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

@app.before_first_request
def generate_word_embeddings():
    word_embeddings = utils.get_word_embeddings()
    app.config['WORD_VECTORS'] = word_embeddings

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.route('/<filename>')
def show_pdf(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    f = None
    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        if not utils.allowed_file(f.filename):
            form.file.data = None
            flash("Sorry, only PDF files are allowed. Please upload a new file.")
            return redirect(request.url)
        else:
            utils.remove_uploads()
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            return redirect(url_for('config_summary'))
    return render_template('index.html', form=form)

@app.route('/summary-config', methods=['GET', 'POST'])
def config_summary():
    if os.listdir(app.config['UPLOAD_PATH']) == []:
        return abort(400)
    file = os.listdir(app.config['UPLOAD_PATH'])[0]
    form = SummaryConfigForm()
    if form.validate_on_submit():
        session['length'] = form.length.data
        form.length.data = None
        return redirect(url_for('print_summary', length=session.get('length')))
    return render_template('upload.html', file=file, form=form)

@app.route('/summary/<length>', methods=['GET', 'POST'])
@cache.memoize()
def print_summary(length):
    pdf = os.listdir(app.config['UPLOAD_PATH'])[0]
    txt_file = utils.get_matching_txt(pdf)
    tr = TextRank('preprocessed/' + txt_file, app.config['WORD_VECTORS'])
    summary = tr.get_summary(length)
    return render_template('summary.html', summary=summary, file=pdf)
