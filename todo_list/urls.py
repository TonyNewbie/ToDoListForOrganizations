from django.urls import path
from todo_list.views import UserAuthenticationView, LogoutView, TaskListView, SingleTaskView

# API endpoints
urlpatterns = [
    path('auth/login/', UserAuthenticationView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('user/todo/', TaskListView.as_view()),
    path('user/todo/<int:pk>', SingleTaskView.as_view()),
]
