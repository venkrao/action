from twilio.rest import Client

from actio.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from actio import settings


def twilio_create_room(room_name=None):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    room = client.video.rooms.create(unique_name=room_name)

    print(room)
    return room


def twilio_set_room_status(room_sid=None, status=None):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    room = client.video.rooms(room_sid).update(status=status)


def twilio_create_access_token(room=None):
    # required for all twilio access tokens
    # # TODO: Store them in the database instead of settings?
    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET

    identity = 'actio_api_key'

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity, ttl=600)

    # Create a Video grant and add to token
    video_grant = VideoGrant(room=room)
    token.add_grant(video_grant)

    # Return token info as JSON
    return token.to_jwt()


def twilio_retrieve_rooms(unique_name=None):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    rooms = client.video.rooms.list(unique_name=unique_name, limit=20)

    for record in rooms:
        print(record.sid)
