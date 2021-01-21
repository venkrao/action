from django.urls import path
from . import views
import debug_toolbar
from django.urls import include
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Actio API",
      default_version='v1',
      description="Actio API Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("sessions/status/<str:status>/", views.RetrieveSessionsByStatusView.as_view(), name="retrieve-sessions"),
    path("session/<uuid:session_uuid>/", views.RetrieveSessionByUuidView.as_view(), name="retrieve-sessions"),
    path("twilio/calls/video/<uuid:session_uuid>/", views.VideoCallParticipantsByUuidView.as_view(), name="twilio-video"),
    path("twilio/room/<str:action>/<uuid:session_uuid>/", views.TwilioRoomHandlerByUuidView.as_view(), name="twilio-room-handler"),
]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# jwt endpoints
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
