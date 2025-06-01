from django.urls import include, path
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/vote/', views.vote_question, name='vote_question'),
    path('question/<int:question_id>/mark_correct/', views.mark_correct_answer, name='mark_correct_answer'),
    path('answer/<int:answer_id>/vote/', views.vote_answer, name='vote_answer'),
    path('edit/', views.settings, name='settings'),
    path('signup/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_title>', views.tag, name='tag'),
    path('uploads/<path:path>', serve, {'document_root': settings.BASE_DIR / 'uploads'})
]