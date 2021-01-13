from django.urls import path
from . import views

urlpatterns = [
    path("session/retrieve/", views.RetrieveSessions.as_view(), name="retrieve-sessions"),
    path("twilio/room/", views.TwilioRoomHandlerView.as_view(), name="twilio-room-handler"),
    path("twilio/calls/video/", views.VideoCallParticipantsView.as_view(), name="twilio-video"),
]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# jwt endpoints
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]