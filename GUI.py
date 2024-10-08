import atexit
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog


prog_running = False
proc = None
root = tk.Tk()
root["bg"] = "#222"
root.resizable(width=False, height=False)
root.geometry("450x400")
root.title("ShareSphere")
root.iconbitmap("static/Assets/favicon.ico")


def run_program():
  global prog_running, proc
  if not prog_running:
    button.configure(text="Stop", command=close_program, state="active")
    prog_running = True
    if sel_dir.get() == 1:
      folder_path = filedialog.askdirectory()
      proc = subprocess.Popen(["python", "app.py", "-d", folder_path], stdout=subprocess.PIPE,  stderr=subprocess.PIPE,  text=True)
    else:
      proc = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True)

    for _ in range(5):
      output = proc.stderr.readline()

      if "Running on http" in output:
        ip = output[21:]
    label_2.configure(text=ip)
    label_2.bind("<Button-1>", lambda e: webbrowser.open_new_tab(f"http://{ip}"))


def close_program():
  global prog_running, proc
  if prog_running:
    proc.kill()
    prog_running = False
    button.configure(text="Create a share room", command=run_program)
    label_2.configure(text="")


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
button = tk.Button(root, text="Create a share room",
                    bg="#aa9c04",
                    fg="#222",
                    command=run_program,
                    height=2,
                    width=27,
                    font=24
                  )

label_1.pack()
label_2.pack()
button.pack()
checkbutton.pack()

atexit.register(close_program)
root.mainloop()