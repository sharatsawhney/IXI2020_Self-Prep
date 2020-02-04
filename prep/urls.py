from django.conf.urls import url, include
from prep.views import index, UserData

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^userdata/', UserData.as_view(), name='userdata'),
]