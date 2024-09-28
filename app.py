#!/bin/python3
import os
import argparse
from utils import fetch_files
from sys import exit
from pathlib import Path
from collections import deque
from flask import Flask, render_template, send_from_directory

OS = os.name
WINDOWS = 'nt'
UNIX_LIKE = 'posix'
SOURCE_FILE_PATH = Path(__file__).resolve().parent
CURRENT_PATH = os.getcwd()
TEMPLATE_DIR = f'{SOURCE_FILE_PATH}/templates'
USERNAME = os.getlogin()
PROGRAM_NAME = 'ShareSphere'
app = Flask(__name__, template_folder=TEMPLATE_DIR)
#app.config["SEND_FILE_MAX_AGE_DEFAULT"] = -1 we should disable resending the static data that has been once sent. 
parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
if OS == UNIX_LIKE:
  parser.add_argument('-d', '--directory', action='store', default='~/Downloads')
elif OS == WINDOWS:
  parser.add_argument('-d', '--directory', action='store', default=fr'C:\Users\{USERNAME}\Downloads')

args = parser.parse_args()
share_path = deque([i for i in args.directory])

if share_path[0] == '~' and OS == UNIX_LIKE:
  share_path.popleft()
  share_path.appendleft(f'/home/{USERNAME}')
elif share_path[0] == '~' and OS == WINDOWS:
  print('< ~ > operator is not supported on windows')
  exit(1)

if share_path[0] == '.':
    share_path.popleft()
    share_path.appendleft(os.path.abspath(CURRENT_PATH))

share_path = ''.join(share_path)

try:
  files = fetch_files(share_path)
except FileNotFoundError:
  print('This directory doesn\'t exist')
  exit(1)

@app.route('/')
def hello_world():
  return render_template('index.html', files=files)


@app.route('/download/<path:name>')
def download_file(name, path=share_path):
  print(f'Someone is picking up <{name}> in >> {path}')
  return send_from_directory(path, name, as_attachment=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
