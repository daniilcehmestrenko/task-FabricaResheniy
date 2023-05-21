from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MailingListViewSet,
    ClientViewSet,
    MailingListStatViewSet,
    MailingListStartViewSet
)


router = DefaultRouter()
router.register(r'start_mailing', MailingListStartViewSet, basename='start')
router.register(r'mailinglist', MailingListViewSet)
router.register(r'client', ClientViewSet)
router.register(r'mailinglist_stats', MailingListStatViewSet, basename='stat')

urlpatterns = [
    path('', include(router.urls)),
]