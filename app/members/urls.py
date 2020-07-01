from django.urls import path
from rest_framework import routers
from members.views import UserModelViewAPI

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', UserModelViewAPI)
urlpatterns = router.urls