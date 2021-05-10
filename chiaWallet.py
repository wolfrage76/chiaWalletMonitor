import datetime #for reading present date
import time 
import os
import requests #for retreiving coronavirus data from web
from plyer import notification #for getting notification on your PC

enableSysTray = False
if os.name == 'nt':
    from infi.systray import SysTrayIcon
    enableSysTray = True

walletaddress = 'xch1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

sendDiscord = False
discordWebhook = r'https://discord.com/api/webhooks/0000000000000000/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#Send push notification over Pushover?
sendPushover = False
pushoverUserKey = 'xxxxxxxxxx'
pushoverAPIKey = 'xxxxxxxxxxxxxxxx'

#Play a custom sound file?
playSound = False
song = 'audio.mp3'

#Send a slack notification?
sendSlack = False
slack_token = 'xoxb-my-bot-token'
slack_channel = '#my-channel'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Chia Wallet Monitor'


#SendPushBullet notification?
sendPushBullet = False
pbAPIKey = 'XXXXXXXXXXXXXXXXXXXXX'

def on_quit_callback(systray):
    print("QUIT!")
    if systray:
        systray.shutdown()
   

def checkWallet(systray):
    print("Wallet check")

menu_options = (("Check Wallet", None, checkWallet),)
if enableSysTray:
    systray = SysTrayIcon("chia.ico", "ChiaWalletMonitor", menu_options, on_quit=on_quit_callback)



#BEGIN

#let there is no data initially
chiWallet = None
currXCH = 0
netBalance = -1
firstRun = True
if enableSysTray:
    systray.start()

headers = requests.utils.default_headers()
print(headers)      
headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36;"})

while(True):

    try:
        
        chiaWallet = requests.get("https://api2.chiaexplorer.com/address/" + walletaddress, headers=headers)
    except:
        print("Please! Check your internet connection")

    if (chiaWallet != None):
        data = chiaWallet.json()
        netBalance = data['netBalance']/1000000000000

        if (firstRun == True):
            msgTitle = "Your wallet as of {}".format(datetime.date.today())
            msgTxt = "You have a total of {} XCH, Farmer!".format(netBalance)

        else:
            if currXCH != netBalance:
                msgTxt = "Your Chia balance has changed, for a total of {netBalance} XCH, Chia Pet!".format(netBalance = data['netBalance']/1000000000000)
                msgTitle = 'Congrats, Chia Farmer!'
                
                if sendDiscord == True:
                    import discord_notify as dn
                    discord_info = msgTxt
                    notifier = dn.Notifier(discordWebhook)
                    notifier.send(discord_info, print_message=False)
                
                if sendPushover == True:
                    from pushover import init, Client
                    client = Client(pushoverUserKey, api_token=pushoverAPIKey)
                    client.send_message(msgTxt, title=msgTitle) #pip install python-pushover
                        
                if playSound == True:
                    from playsound import playsound #pip install playsound
                    playsound(song)
                
                if sendSlack == True:
                    post_message_to_slack(msgTxt)
                    
                if sendPushBullet == True:
                    from pushbullet import Pushbullet
                    pb = Pushbullet(pbAPIKey)
                    push = pb.push_note(msgTitle, msgTxt)

    notification.notify(
        title = msgTitle,
        message = msgTxt ,
        app_icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chia.ico"),
        app_name = "Chia Wallet Monitor",
        timeout  = 50
    )
    firstRun = False
    currXCH = netBalance
    print(msgTxt)
    time.sleep(10*3)
