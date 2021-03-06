import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

# ------------------------------------


def get_sandboxie_exe_path():
  program_files_path = os.getenv('PROGRAMFILES')
  sandboxie_exe_path = program_files_path + '\\Sandboxie\\Start.exe'
  if os.path.exists(sandboxie_exe_path):
    return sandboxie_exe_path
  sandboxie_exe_path = program_files_path + '\\Sandboxie-Plus\\Start.exe'
  if os.path.exists(sandboxie_exe_path):
    return sandboxie_exe_path
  return False


appdata_path = os.getenv('APPDATA')
zoom_exe_path = appdata_path + '\\Zoom\\bin\\Zoom.exe'
sandboxie_exe_path = get_sandboxie_exe_path()

sandboxie_box_prefix = 'SB'

# ------------------------------------


def get_box_name(box_number):
  return sandboxie_box_prefix + str(box_number)


def open_zoom(link):
  subprocess.Popen([zoom_exe_path, '--url=' + link])


def open_zoom_sandboxed(link, box_number):
  subprocess.Popen([sandboxie_exe_path, '/box:' +
                   get_box_name(box_number), zoom_exe_path, '--url=' + link])


def join_meeting():
  num_of_zooms = int(e2.get())
  zoom_link = e1.get()
  main_zoom_unsandboxed = bool(e3.get())
  if main_zoom_unsandboxed:
    open_zoom(zoom_link)
  for cnt in range(2 if main_zoom_unsandboxed else 1, num_of_zooms + 1):
    zoom_link_with_name = zoom_link + '&uname=Zoom+' + str(cnt)
    open_zoom_sandboxed(zoom_link_with_name, cnt)
  master.quit()

# ------------------------------------


def _onKeyPress(event):
  ctrl = (event.state & 0x4) != 0
  if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
    event.widget.event_generate("<<Cut>>")
  if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
    event.widget.event_generate("<<Paste>>")
  if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
    event.widget.event_generate("<<Copy>>")
  if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
    event.widget.select_range(0, 'end')


master = tk.Tk()
master.bind("<Key>", _onKeyPress)
master.title('Zoom Runner')
tk.Label(master, text='Zoom Link').grid(row=0)
tk.Label(master, text='Number of Zooms').grid(row=1)
tk.Label(master, text='Main Zoom NOT sandboxed').grid(row=2)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e3 = tk.IntVar(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master, text='Quit', command=master.quit).grid(
    row=3, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Join', command=join_meeting).grid(
    row=3, column=1, sticky=tk.W, pady=4)
tk.Checkbutton(master, variable=e3).grid(row=2, column=1, sticky=tk.W, pady=4)

try:
  if not sandboxie_exe_path:
    messagebox.showerror(
        "Error", "Sandboxie was not found on your computer!")
  else:
    tk.mainloop()
except:
  pass
