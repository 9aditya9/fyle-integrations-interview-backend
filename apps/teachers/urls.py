from django.urls import path, include
from .views import AssignmentView

urlpatterns = [
    path('assignments/', AssignmentView.as_view(), name='teachers-assignments')
]
