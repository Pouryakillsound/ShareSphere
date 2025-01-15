#!/bin/python3

import os
import sys
import array
import atexit
import webbrowser
import tkinter as tk
import multiprocessing as mp
from pathlib import Path
from tkinter import filedialog
from multiprocessing.shared_memory import SharedMemory

from app import ShareSphere, DEFAULT_FOLDER


# copile with: python -m nuitka --standalone --onefile --include-data-dir=templates=templates --include-data-dir=static=static\
#  --enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=static\Assets\favicon1.ico --windows-force-stderr-spec=stderr.txt GUI.py


# So we can read from streams
#sys.stdout = open('stdout.txt', 'a+')
#sys.stderr = open('stderr.txt', 'w+')

class StringSharedMemory:
  def __init__(self):
    self.count = 0

    self.mem = SharedMemory(name='SSshm', create=True, size=10240) # 10240 bytes are probably enough

  def write(self, s: str):
    s = s.encode()
    length = len(s)
    self.mem.buf[self.count: (self.count + length)] = s
    self.count += length

  def read(self):
    return ''.join(list(map(chr, list(array.array('B', self.mem.buf))))).split('\n')

  def flush(self):
    pass # It's not a tty Biaaatch

def run_program(folder_adderss, stderr):
  sys.stderr = stderr
  sys.stdout = stderr
  ShareSphere().run(folder_adderss)

def close_program():
  button.configure(text='Start', command=initializer) 
  p.terminate()
  label_2.configure(text='')
  label_2.bind('<Button-1>', '')


def initializer():
  global p
  button.configure(text='Stop', command=close_program)
  folder_address = filedialog.askdirectory() if sel_dir.get() else DEFAULT_FOLDER
  p = mp.Process(target=run_program, args=[folder_address, shared_mem], daemon=True)
  p.start()

  while True:
    read_mem = shared_mem.read()
    ip = 0
    for output in read_mem:
      if 'Running on' in output and '127' not in output and '0.0.0.0' not in output:
        ip = output[21:]
        break
    if ip:
      break
  label_2.configure(text=ip)
  label_2.bind('<Button-1>', lambda e: webbrowser.open_new_tab(f"http://{ip}"))


def exit_program():
  shared_mem.mem.close()
  shared_mem.mem.unlink()


if __name__ == "__main__":
  shared_mem = StringSharedMemory()
  root = tk.Tk()
  root["bg"] = "#222"
  root.resizable(width=False, height=False)
  root.geometry("450x400")
  root.title("ShareSphere")
  text_var = tk.StringVar(value="ShareSphere")
  label_1 = tk.Label(root,
                    textvariable=text_var, 
                    anchor=tk.CENTER,       
                    bg="#222",      
                    height=6,              
                    width=19,              
                    font=("Arial", 24, "bold"), 
                    cursor="hand2",   
                    fg="#aa9c04",             
                    padx=15,
                  )

  label_2 = tk.Label(root,
                    textvariable=None, 
                    anchor=tk.CENTER,       
                    bg="#222",      
                    height=4,              
                    width=19,              
                    font=("Arial", 10, "bold"), 
                    cursor="hand2",   
                    fg="#aa9c04",             
                    padx=15,
                  )

  sel_dir = tk.IntVar()
  checkbutton = tk.Checkbutton(root, text="Select folder", variable=sel_dir, 
                              onvalue=1, offvalue=0)

  button = tk.Button(root, text="Start",
                      bg="#aa9c04",
                      fg="#222",
                      command=initializer,
                      height=2,
                      width=27,
                      font=24
                    )

  label_1.pack()
  label_2.pack()
  button.pack()
  checkbutton.pack()
  favicon_addr = Path(os.path.join(os.path.dirname(__file__), 'static', 'Assets', 'favicon.ico')).resolve()
  root.iconbitmap(favicon_addr)
  atexit.register(exit_program)
  root.mainloop()
