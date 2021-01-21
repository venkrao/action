from .models import *
from django.db.models.functions import Now
from .aws import *
from .twilio_wrapper import *
from twilio.base.exceptions import *
from boto3.exceptions import *

import logging
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


def get_coach_uid_from_username(username=None):
    """
    :param username:
    :return:
    """

    try:
        coach = Coach.objects.get(username=username)
        return coach
    except:
        return None


def add_twilio_room_to_db(actio_session=None, unique_name=None, display_name=None, access_token=None):
    twilio_room = None
    try:
        actio_session_obj = ActioSession.objects.filter(session_identifier=actio_session)[0]
        twilio_room = TwilioRoom(actio_session=actio_session_obj, unique_name=unique_name, access_token=access_token,
                                 display_name=display_name)
        twilio_room.save()
    except Exception:
        logger.exception("Could not make a db entry for session: {}".format(actio_session))
        raise

    return twilio_room


def update_twilio_room_in_db(room_name=None, access_token=None, coach=None):
    """
    :param room_name:
    :param access_token:
    :param coach:
    :return:
    """
    room = {"room_created": False, "errors": None, "access_token": None}
    coach = get_coach_uid_from_username(username=coach)
    try:
        twilio_room = TwilioRoom.objects.get(room=room_name)
        twilio_room.access_token = access_token
        twilio_room.coach = coach
        twilio_room.save()
    except:
        logger.exception("Could not update Twilio Room: {}".format(room_name))
        raise

    room["room_created"] = True
    room["access_token"] = twilio_room.access_token
    room["room_sid"] = twilio_room.room

    return room


def retrieve_twilio_access_token_from_db(room=None, coach=None):
    """
    Retrieve latest access token for the given room_sid, assigned to given coach.
    :param room_sid:
    :param coach:
    :return: access_token:
    """
    coach = get_coach_uid_from_username(username=coach)
    try:
        room = TwilioRoom.objects.get(room=room, assigned_to_coach=coach)
    except:
        raise

    return room.access_token


def close_twilio_room(access_token=None):
    """
    Set the status of the room to Completed.
    :param access_token:
    :return:
    """
    pass


def get_course_subcategory_id_from_course_subcategory_name(course_subcategory=None):
    course_subcategory = CourseSubcategory.objects.get(subcategory=course_subcategory)

    return course_subcategory.id


def get_session_participants(actio_session=None):
    """
    :param actio_session:
    :return:
    """
    participants = ActioSession.objects.filter(session_identifier=actio_session).values('user')
    print(participants)
    participants_list = []
    for i in participants:
        participants_list.append(i["user"])

    return participants_list


def get_aws_arn(user=None):
    resource_object = AmazonResourceName.objects.get(user=user)

    return resource_object.arn


def send_sns_push_notification(users=None, message=None):
    boto = Boto3Wrapper()
    for user in users:
        arn = get_aws_arn(user=user)
        print("send push notification to {}".format(arn))
        boto.sns_publish(message=str(message), target_arn=arn)


def create_twilio_room(actio_session=None):
    twilio_room = {"errors": {}}

    actio_session_info = ActioSession.objects.filter(session_identifier=actio_session)[0]
    unique_name = "{}-{}-{}-{}-{}-1".format(str(actio_session_info.course_subcategory).replace(" ", "-"),
                                          actio_session_info.coach, actio_session_info.conducted_on,
                                          actio_session_info.start_time, actio_session_info.end_time)
    display_name = actio_session_info.course_subcategory

    try:
        room_sid = twilio_create_room(room_name=unique_name)
        access_token = twilio_create_access_token(room=unique_name)

        room = add_twilio_room_to_db(actio_session=actio_session, unique_name=unique_name, display_name=display_name,
                                     access_token=access_token)
        twilio_room["unique_name"] = room.unique_name
        twilio_room["display_name"] = str(room.display_name)
        twilio_room["access_token"] = room.access_token
    except TwilioRestException as twilio_exception:
        twilio_room["errors"]["message"] = twilio_exception.msg
    except Exception as e:
        twilio_room["errors"]["message"] = str(e)

    return twilio_room

def twilio_call_participants(actio_session=None):
    """
    :param actio_session:
    :return:
    """
    response = {"errors": {}, "message": ""}
    try:
        actio_session_info = ActioSession.objects.filter(session_identifier=actio_session)[0]

        twilio_room_info = TwilioRoom.objects.filter(actio_session=actio_session_info.id)[0]
        sns_message_body = {"unique_name": twilio_room_info.unique_name, "conducted_on": actio_session_info.conducted_on,
                           "start_time": actio_session_info.start_time, "end_time": actio_session_info.end_time,
                            "access_token": twilio_room_info.access_token, "coach": actio_session_info.coach}
        logger.info(sns_message_body)

        session_participants = get_session_participants(actio_session=actio_session_info.session_identifier)
        print("participants of session {}: {}".format(actio_session, session_participants))
        logger.info(session_participants)
        send_sns_push_notification(users=session_participants, message=sns_message_body)
        response["message"] = "Push notification sent to all participants."
    except Boto3Error as e:
        response["errors"]["message"] = "Could not send push notifications"
    except Exception as e:
        response["errors"]["message"] = "Internal server error."

    return response