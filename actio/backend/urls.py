from django.urls import path
from . import views

urlpatterns = [
    path("sessions/<str:status>/", views.RetrieveSessionsView.as_view(), name="retrieve-sessions"),
    path("session/<uuid:session_uuid>/", views.RetrieveSessionByUuidView.as_view(), name="retrieve-sessions"),
    path("twilio/calls/video/<uuid:session_uuid>/", views.VideoCallParticipantsByUuidView.as_view(), name="twilio-video"),
    path("twilio/room/<str:action>/<uuid:session_uuid>/", views.TwilioRoomHandlerByUuidView.as_view(), name="twilio-room-handler"),
]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import debug_toolbar
from django.urls import include
from django.conf.urls import url

# jwt endpoints
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]