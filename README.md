# chiaWalletMonitor
Get notifications when you get Chia XCH  -- Reach me at chia@ifhya.com

Currently this only works in Windows but I will update it to work cross platform shortly.

When your wallet gets XCH, you can get a notification via Popup, Push notice through Pushover, Slack or a cusotm sound file.

run with: python chiaWallet.py

Currently notification support is: Windows toast, audio file, Pushover push notifications, slack.

Needs work:
- Need to make it cross platform and not windows only
- Make it so it can only be run once
- Add a --stop command
- Add more notification types

If you want to test, change the line XCH='X' to XCH=0 and run it (IF you have at least 1 XCH already) and then change back once done testing.



