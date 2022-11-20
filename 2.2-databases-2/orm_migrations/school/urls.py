import debug_toolbar
from school.views import students_list
from django.urls import include, path

urlpatterns = [
    path('', students_list, name='students'),
    path('__debug__/', include(debug_toolbar.urls)),
]
