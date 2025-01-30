#!/bin/python3

import sys
import atexit
import webbrowser
import tkinter as tk
import multiprocessing as mp
from typing import Union
from pathlib import Path
from tkinter import filedialog

from app import *


r'''copile with: python -m nuitka --standalone --onefile --include-data-dir=templates=templates --include-data-dir=static=static
--enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=static\Assets\favicon1.ico  GUI.py'''


class StringSharedMemory:
  def __init__(self, q: mp.Queue): self.queue = q

  def write(self, s: Union[str, bytes]):
    s = s.decode() if type(s) == bytes else s
    self.queue.put(s)

  def read(self): return self.queue.get().split('\n')

  # Not needed
  def flush(self): pass


def run_program(folder_adderss, queued_stream):
  sys.stderr =  queued_stream
  sys.stdout = queued_stream
  ShareSphere().run(folder_adderss)


def initializer():
  global p, p_alive, shared_mem
  button.configure(text='Stop', command=close_process)
  if sel_dir.get():
    folder_address = filedialog.askdirectory()
    if not folder_address:
      folder_address = DEFAULT_FOLDER
  else:
    folder_address = DEFAULT_FOLDER

  p = mp.Process(target=run_program, args=[folder_address, shared_mem], daemon=True)
  p.start()
  p_alive = True

  while True:
    read_mem = shared_mem.read()
    ip = None
    
    for output in read_mem:
      if 'Running on' in output and '127' not in output and '0.0.0.0' not in output:
        ip = output[21:]
        break

    if ip:
      break

  label_2.configure(text=ip)
  label_2.bind('<Button-1>', lambda e: webbrowser.open_new_tab(f"http://{ip}"))

def close_process():
  global p_alive
  button.configure(text='Start', command=initializer) 
  label_2.configure(text='')
  label_2.bind('<Button-1>', '')
  if p_alive:
    p.terminate()
    p_alive = False



if __name__ == "__main__":
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

  mp.set_start_method('fork') if OS == UNIX_LIKE else mp.set_start_method('spawn')
  q = mp.Queue()
  shared_mem = StringSharedMemory(q)

  label_1.pack()
  label_2.pack()
  button.pack()
  checkbutton.pack()
  favicon_addr = Path(os.path.join(os.path.dirname(__file__), 'static', 'Assets', 'favicon.xbm' if OS==UNIX_LIKE else 'favicon.ico'))
  root.iconbitmap(favicon_addr)

  p_alive = False
  atexit.register(lambda: p.terminate if p_alive else None)

  root.mainloop()
