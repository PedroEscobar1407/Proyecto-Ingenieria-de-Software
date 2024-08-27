from django.conf.urls.static import static
from django.urls import path

from app import views
from project import settings

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_page, name="login"),
    path("patient-register/", views.patient_register, name="patient-register"),
    path("psych-register/", views.psych_register, name="psych-register"),
    path("user-diary/", views.user_diary, name="user-diary"),
    path("psych-diary/", views.psych_diary, name="psych-diary"),
    path("logout/", views.log_out, name="log-out"),
    path('link_psychologist/<int:psych_id>/', views.link_psychologist, name='link_psychologist'),
    path('unlink_psychologist/<int:psych_id>/', views.unlink_psychologist, name='unlink_psychologist'),
    path('remove_all_psychologists/', views.remove_all_psychologists, name='remove_all_psychologists'),
    path('create_entry/', views.create_entry, name='create_entry'),
    path('sort_entries/<str:order>/', views.sort_entries, name='sort_entries'),
    path('search_entries/', views.search_entries, name='search_entries'),
    path('delete_all_diaries/', views.delete_all_diaries, name='delete_all_diaries'),
    path('get_patient_diaries/', views.get_patient_diaries, name='get_patient_diaries'),
    path('sort-patient-entries/<str:order>/', views.sort_patient_entries, name='sort_patient_entries'),
    path('search-patient-entries/', views.search_patient_entries, name='search_patient_entries'),
    path('get_entries_from_psych', views.get_entries_from_psych, name='get_entries_from_psych')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
