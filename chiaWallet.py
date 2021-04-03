#This script for Windows runs in the background and tells you with a popup when you've gotten Chia XCH!
#
#Only working on windows! Cross platform version coming shortly
#
#You will need to do 'pip install pywin32' as that is needed to hide the process in the background.
#Also for playsound, pushover,and any other modules you might be missing.
#
#Run from normal command prompt
#
#Come join us on the Flexpool Discord #CHIA channel! https://discord.gg/JESmva9R
#

#By Wolfrage - xch1dylvrjqwsfjywy9a4swx4armnde9jdar4g2e9muxzgd7dnl0gstsxjx3p0

#Chi chi chi Chia!

ver = ".07"

#Display Popup when you get XCH?
showPopup = True

#Send push notification over Pushover?
sendPushover = False
pushoverUserKey = ''
pushoverAPIKey = ''

#Play a custom sound?
playSound = False
song = 'audio.mp3'

#Send a slack notification?
sendSlack = False
slack_token = 'xoxb-my-bot-token'
slack_channel = '#my-channel'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Chia Wallet Monitor'

#Location of your chia executable - CHECK THE VERSION NUMBER in app-XXX as it will change with Chia updates
chialoc = "c:\\Users\\Wofl\\AppData\\Local\\chia-blockchain\\app-1.0.2\\resources\\app.asar.unpacked\\daemon\\chia.exe"

#Set XCH to 0 to test it at launch, set it to 'X' for normal operation
XCH = 'X'

import requests
import json
import subprocess
import sys,os
import re
import time
import ctypes

#currently Windows only -- will change ability to hide and do popup on Linux as well shortly
import win32gui, win32console, win32api, win32con #pip install these
  
    
def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_url': slack_icon_url,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()	
    
    
# start program
try:  
    os.unlink('lock') 
    fd=os.open("lock", os.O_CREAT|os.O_EXCL) 
except: 
    try: fd=os.open("lock", os.O_CREAT|os.O_EXCL) 
    except:  
        print ("ChiaWalletMonitor version "+ ver +" is already running, ya goof!")  
        sys.exit()  



win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)

ctypes.windll.user32.MessageBoxW(0, "Script is now running in the background!  You'll be notified of new Chia XCH in your wallet!", "ChiaWalletMonitor "+ ver + " is running!", 0)

pattern = re.compile('-Confirmed: [0-9]+ mojo \(([0-9]*\.[0-9]+) xch\)')

while True:
    m=pattern.search(subprocess.run(chialoc +" wallet show", stdout=subprocess.PIPE).stdout.decode('utf-8'))
    
    if XCH != 'X':
        if m.group(1) != XCH:
            XCH = m.group(1)
            msgTxt = 'You got ' + m.group(1) + ' XCH from Chia! Way to go, buddy!'
            msgTitle = 'Congrats, Chia Farmer!'
            
            if showPopup == True:
                ctypes.windll.user32.MessageBoxW(0, msgTxt, msgTitle, 0)
                
            if sendPushover == True:
                from pushover import init, Client
                client = Client(pushoverUserKey, api_token=pushoverAPIKey)
                client.send_message(msgTxt, title=msgTitle) #pip install python-pushover
                    
            if playSound == True:
                from playsound import playsound #pip install playsound
                playsound(song)
            
            if sendSlack == True:
                slack_info = 'You got *{}* XCH from Chia! Congrats, Buddy!|Chia Wallet Monitor>.'.format(m.group(1))
                post_message_to_slack(slack_info)
            
                
    if XCH == 'X':
       XCH = m.group(1)  
 
    time.sleep(30)
# exit program
try: os.close(fd)  # (6)
except: pass
try: os.unlink('lock')  
except: pass
sys.exit()  
