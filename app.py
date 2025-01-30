#!/bin/python3
import os
import argparse
from utils import fetch_files
from pathlib import Path
from flask import Flask, request, render_template, send_from_directory, flash, redirect


OS = os.name
WINDOWS = 'nt'
UNIX_LIKE = 'posix'
SOURCE_FILE_PATH = Path(__file__).resolve().parent
CURRENT_PATH = os.getcwd()
TEMPLATE_DIR = f'{SOURCE_FILE_PATH}/templates'
STATIC_DIR = f'{SOURCE_FILE_PATH}/static'
USERNAME = os.getlogin()
PROGRAM_NAME = 'ShareSphere'
DEFAULT_FOLDER = f"/home/{USERNAME}/Downloads" if OS == UNIX_LIKE else fr'C:\Users\{USERNAME}\Downloads'

class ShareSphere:
  def __init__(self):
    self.app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    self.app.config['UPLOAD_FOLDER'] = DEFAULT_FOLDER
    self.app.secret_key = 'key'

    self.app.add_url_rule('/', 'home', self.home)
    self.app.add_url_rule('/download/<path:name>', 'download_file', self.download_file)
    self.app.add_url_rule('/AboutUs', 'about_us', self.about_us)
    self.app.add_url_rule('/Source', 'source_code', self.source_code)
    self.app.add_url_rule("/Upload", 'upload', self.upload, methods=['GET', 'POST'])

  def run(self, share_path=DEFAULT_FOLDER):
    if share_path[0] == '~' and OS == UNIX_LIKE:
      share_path = os.path.join(f'/home/{USERNAME}/' + share_path[2:])

    elif share_path[0] == '~' and OS == WINDOWS:
      print('< ~ > operator is not supported on windows')
      exit(1)

    if share_path[0] == '.':
      share_path = os.path.abspath(CURRENT_PATH) + share_path[1:]

    if not os.path.isdir(share_path):
      raise 'Directory path is not correct'
    
    self.share_path = share_path
    self.app.run(host='0.0.0.0')

  def home(self):
    return render_template('index.html', files=fetch_files(self.share_path))

  def download_file(self, name):
    print(f'Someone is picking up < {name} > in --> {self.share_path}')
    return send_from_directory(self.share_path, name, as_attachment=True)

  def about_us(self):
    return render_template('about.html')

  def source_code(self):
    return render_template('sourcecode.html')

  # single file fetcher (more than one file just get the first file)
  def upload(self):
    if request.method == 'GET':
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
    file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
    flash('File uploaded successfully')
    return redirect('/')

if __name__ == '__main__':
  a = ShareSphere()
  parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
  parser.add_argument('-d', '--directory', action='store', default=DEFAULT_FOLDER)
  args = parser.parse_args()
  share_path = args.directory
  a.run(share_path)