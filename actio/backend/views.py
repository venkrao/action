from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
import traceback

from .utils import *

import logging

logger = logging.getLogger(__name__)


class RetrieveSessionByUuidView(SerializerExtensionsAPIViewMixin, ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActioSessionSerializer
    queryset = ActioSession.objects.all()

    extensions_expand = {'course_category', 'course_subcategory', 'coach'}

    def get_queryset(self):
        queryset = get_list_or_404(self.queryset, session_identifier=self.kwargs.get("session_uuid"))
        return queryset

class RetrieveSessionsView(SerializerExtensionsAPIViewMixin, ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActioSessionSerializer
    queryset = ActioSession.objects.all()

    extensions_expand = {'course_category', 'course_subcategory', 'coach'}

    def get_queryset(self):
        queryset = get_list_or_404(self.queryset, session_identifier=self.kwargs.get("session_uuid"))
        return queryset


class VideoCallParticipantsByUuidView(APIView):
    """ Request from user who is a coach, with a Twilio room name will create a AWS SNS
        push notification per user who's registered for this session. """

    permission_classes = [permissions.IsAuthenticated]

    # TODO: Create a Permission class for Coach. Only a user who's a Coach should be allowed to *generate*
    # TODO: a Twilio access token

    def get(self, request, **kwargs):
        response = {"errors": None, "result": None}
        actio_session = self.kwargs.get("session_uuid", None)

        if actio_session is not None:
            try:
                twilio_call_participants(actio_session=actio_session)
                response["result"] = "success"
            except Exception as e:
                response["errors"] = "Internal server error. Please contact support."
                traceback.print_exc()
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(response)

        return Response(status=status.HTTP_404_NOT_FOUND)


class TwilioRoomHandlerByUuidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # TODO: Create a Permission class for Coach. Only a user who's a Coach should be allowed to *generate*
    # TODO: a Twilio access token

    def get(self, request, **kwargs):
        action = self.kwargs.get("action", None)
        actio_session = self.kwargs.get("session_uuid", None)

        try:
            if action == "create" and actio_session is not None:
                twilio_room = create_twilio_room(actio_session=actio_session)
                return Response(twilio_room)
        except Exception:
            traceback.print_exc()
            return Response({"errors": "Internal server error. Please contact support."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_404_NOT_FOUND)



class RetrieveSessions(SerializerExtensionsAPIViewMixin, ListAPIView):
    serializer_class = ActioSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    extensions_expand = {'course_category', 'course_subcategory', 'coach'}

    valid_session_status = {'completed': "Completed",
                            'scheduled': 'Scheduled',}

    def get_queryset(self):
        if self.request.method == "GET" and ('status' in self.request.GET or 'id' in self.request.GET):
            session_status = self.request.GET.get('status', None)
            if session_status:
                if session_status.lower() in self.valid_session_status:
                    return ActioSession.objects.filter(session_status=self.valid_session_status[session_status.lower()])
                else:
                    raise Http404

            id = self.request.GET.get('id', None)
            if id:
                try:
                    return ActioSession.objects.filter(id=id)
                except ActioSession.DoesNotExist:
                    raise Http404



