from django.urls import path
from polls.views import vote, results, detail, index

app_name = 'polls'
urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', detail, name='detail'),
    path('<int:pk>/results/', results, name='results'),
    path('<int:question_id>/vote/', vote, name='vote'),
]