import datetime #for reading present date
import time 
import requests #for retreiving coronavirus data from web
from plyer import notification #for getting notification on your PC


from infi.systray import SysTrayIcon
def checkWallet(systray):
    print("")
menu_options = []#(("Check Wallet", None, checkWallet),)
systray = SysTrayIcon("chia.ico", "ChiaWalletMonitor", menu_options)
systray.start()

def on_quit_callback(systray):
    program.shutdown()
systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options, on_quit=on_quit_callback)

walletaddress = 'xch1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

sendDiscord = True
discordWebhook = r'https://discord.com/api/webhooks/000000000000000/xxxxxxxxxxxxxxxxxxxxxxxxxxx'

#Send push notification over Pushover?
sendPushover = False
pushoverUserKey = ''
pushoverAPIKey = ''

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
pbAPIKey = 'xxxxxxxxxx'


#BEGIN

#let there is no data initially
chiWallet = None
currXCH = 0
grossBalance = -1
firstRun = True
   
while(True):

    try:
        chiaWallet = requests.get("https://api2.chiaexplorer.com/address/" + walletaddress)
    except:
        print("Please! Check your internet connection")

    if (chiaWallet != None and firstRun == True):

        data = chiaWallet.json()
        grossBalance = data['grossBalance']/1000000000000
        notification.notify(
                title = "Your wallet as of {}".format(datetime.date.today()),
                message = "You have a total of {} XCH, Farmer!".format(data['grossBalance']/1000000000000)
                            ,
                app_icon = "chia.ico",
                timeout  = 10
            )
        currXCH = grossBalance
        time.sleep(10*3)
    
    if (chiaWallet != None and firstRun == False):

        data = chiaWallet.json()
        grossBalance = data['grossBalance']/1000000000000
   
        if currXCH != grossBalance:
            msgTxt = "You got Chia, for a total of {grossBalance} XCH, Chia Pet!".format(grossBalance = data['grossBalance']/1000000000000)
            msgTitle = 'Congrats, Chia Farmer!'
            
            notification.notify(
                title = msgTitle,
                message = msgTxt ,
                app_icon = "chia.ico",
                timeout  = 50
            )
            
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
                
        
    firstRun = False
    currXCH = grossBalance

    time.sleep(10*3)
