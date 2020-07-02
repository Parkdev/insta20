from django.urls import path
from rest_framework import routers
from members.views import UserModelViewAPI, FollowModelViewAPI

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'list', UserModelViewAPI)
router.register(r'follow', FollowModelViewAPI)

urlpatterns = router.urls