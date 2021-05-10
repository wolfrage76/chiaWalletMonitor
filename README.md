# chiaWalletMonitor
Get notifications when you get Chia XCH  -- Reach me at chia@ifhya.com


When your wallet gets XCH, you can get a notification via Popup, Push notice through Pushover, Discord, Slack or a custom sound file.

## Usage

First create a virtual env and install de dependencies:
```cli
python3 -m venv --system-site-packages venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Start the application with:
`python ./chiaWallet.py`

Run on windows with `pythonw` instead of `python` to run it in the background on windows.  Linux users have their own ways.

## Notifications supported

Currently notification support is:  `toast, audio file, Pushover push notifications, Slack, Discord, PushBullet` - Let me know any others you'd like integrated!
