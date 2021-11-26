import time
import requests
from plyer import notification  # For getting notification on your PC

def streamer_data():
    # Data to fill up
    client_id = 'XXXX'
    client_secret = 'XXXX'
    streamer_name = 'XXXX'

    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }

    req = requests.post('https://id.twitch.tv/oauth2/token', body)

    # Data output
    keys = req.json();

    headers = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }

    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
    stream_data = stream.json();
    streaming_state = len(stream_data['data']) # Save whether the streamer is streaming or not (1 = Streaming, 0 = not streaming)
    return streaming_state, streamer_name      # Return the values to use it in the other function

def stream_notification():
    streaming_state, streamer_name = streamer_data() # Declare the value which it's going to be needed
    notified = 0
    if streaming_state == 1:       # Enter to the statement if it's streaming
        for repeat in range(1):
            notifyMe("Twitch", f"{streamer_name} is live")
        notified = streaming_state # Update the state of variable after have been sent the notification

    while notified == 1:           # Keep the programme waiting unit the streamer disconnect
        streaming_state, streamer_name = streamer_data()
        if streaming_state == 0:
            notified = 0
    time.sleep(1)

def notifyMe(title,message):
    notification.notify(
        title = title,
        message = message,
        app_icon = 'Clock_icon.ico',
        timeout = 1
    )

if __name__ == '__main__':
    while True:
        stream_notification()