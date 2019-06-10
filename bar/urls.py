from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from .views import *
from bar import views

router = routers.DefaultRouter()
# router.register(r'account', UsersViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('link_user', LinkUser.as_view()),
    path('unlink_user', UnlinkUser.as_view()),
    path('get_user_data', GetUserData.as_view()),
    path('linked_users_list', LinkedUsersGetList.as_view()),
    path('is_linked_user', IsLinkedUser.as_view()),
    path('get_notification/<int:message_id>', NotificationManage.as_view()),
    path('send_notification', NotificationSend.as_view()),
    path('update_notification', NotificationUpdate.as_view()),
]
