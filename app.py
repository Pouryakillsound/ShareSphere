#!/bin/python3
import os
import argparse
from utils import fetch_files
from pathlib import Path
from flask import Flask, render_template, send_from_directory, request, flash, redirect

OS = os.name
WINDOWS = 'nt'
UNIX_LIKE = 'posix'
SOURCE_FILE_PATH = Path(__file__).resolve().parent
CURRENT_PATH = os.getcwd()
TEMPLATE_DIR = f'{SOURCE_FILE_PATH}/templates'
STATIC_DIR = f'{SOURCE_FILE_PATH}/static'
USERNAME = os.getlogin()
PROGRAM_NAME = 'ShareSphere'
UPLOAD_FOLDER = f"/home/{USERNAME}/Downloads" if OS == UNIX_LIKE else fr'C:\Users\{USERNAME}\Downloads'

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
parser = argparse.ArgumentParser(prog=PROGRAM_NAME)

if OS == UNIX_LIKE:
  parser.add_argument('-d', '--directory', action='store', default='~/Downloads')
elif OS == WINDOWS:
  parser.add_argument('-d', '--directory', action='store', default=fr'C:\Users\{USERNAME}\Downloads')
args = parser.parse_args()

share_path = args.directory

if share_path[0] == '~' and OS == UNIX_LIKE:
  share_path = share_path[1:]
  share_path = os.path.join(f'/home/{USERNAME}/' + share_path[1:])
elif share_path[0] == '~' and OS == WINDOWS:
  print('< ~ > operator is not supported on windows')
  exit(1)

if share_path[0] == '.':
    share_path = os.path.abspath(CURRENT_PATH) + share_path[1:]

if not os.path.isdir(share_path):
  raise 'Directory path is not correct'

@app.route('/')
def hello_world():
  return render_template('index.html', files=fetch_files(share_path))

@app.route('/download/<path:name>')
def download_file(name, path=share_path):
  print(f'Someone is picking up < {name} > in --> {path}')
  return send_from_directory(path, name, as_attachment=True)

@app.route('/AboutUs')
def about_us():
  return render_template('about.html')

@app.route('/Source')
def source_code():
  return render_template('sourcecode.html')


# single file fetcher (more than one file just get the first file)
@app.route("/Upload", methods=["POST", "GET"])
def upload():
  if request.method == "GET":
    return render_template('upload.html')
  print(request.files)
  if 'file' not in request.files:
    flash('No file part')
    return redirect(request.url)
  file = request.files['file']
  if file.filename == '':
    flash('No selected file')
    return redirect(request.url)
  filename = file.filename
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  flash('File uploaded successfully')
  return redirect("/")

if __name__ == '__main__':
  app.secret_key = 'key'


  app.run(host='0.0.0.0')
