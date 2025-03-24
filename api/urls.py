#from django.urls import path
#from .views import HelloWorld, Students, submit, index , ContactListView
#from .exam_views import ChatView
#urlpatterns =  [
#    path('hello/', HelloWorld.as_view(), name= 'hello_world'),
#    path('students/', Students.as_view(), name= 'list_students'),
#    path('submit/', submit, name='Submit'),
#    path('index/', index, name='Index'),
#    path('contact/',ContactListView.as_view(), name='contact_new'),
#    
#    path('/api/exam/chat/',ChatView.as_view(), name = 'chat_view'),

#]

from django.urls import path
from .views import HelloWorld
from .views import ContactListView
from .views import ContactUpdateDetailView
from .exam_views import ChatView

#from . import views
# from . import views

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'), 

    path('/api/exam/chat/',ChatView.as_view(), name = 'chat_view'),
    
   # path('api/exam/', views.exam_view, name='exam'),
   # path('exam/', views.exam_view, name='exam'),
   
]
