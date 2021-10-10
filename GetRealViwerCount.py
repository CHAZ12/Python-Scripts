import os
import re
from datetime import date
from tkinter import filedialog
import sys
import subprocess
import time
# ask user to Choose a File
# Code is ripped from ActiveState to install esaygui
print("------THIS IS A SCRIPT TO GET THE USERS IN CHAT VS ViEWERS WATCHING FROM TWITCH-----")
try:
    import easygui
    print('module easygui is install')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'easygui'])
try:
    import requests_html
    print('module requests_html is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests_html'])
try:
    import requests
    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])

import easygui as easygui
OpenedFile = filedialog.askopenfilename(filetypes=(("TextFile", ".txt"), ("ALL files", "*")))  # User chooses a file
if OpenedFile == "":
    print('User aborted. Closing program...')
    time.sleep(2)
    exit()
with open(OpenedFile) as StreamName:  # Keep teh file open so we can use it later
    BlenderFile = StreamName.read()  # read opened file
    fileNew = re.sub(r"Broadcaster|Moderators|VIPs|Users|\n", ' ', BlenderFile)  # replace certain strings
    val = easygui.integerbox("Insert Viewer count", "", 0, 0, 99999)  # Pop up a dialog box if user is using bat file
    UserCount = str(len(fileNew.split()))  # split of each word as own string
    file1 = open("Fill", "a+")
    file1.write("Created on: {0}, {1} is number of User(s) in Chat, {2} is viewer count.".format(date.today(), UserCount, val))
    #print(UserCount)
    file1.write(fileNew + "\n\n")
    time.sleep(2)
    print('Process done. Closing Program if not already..')
    os.system('file.py')