from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/new/', views.PostCreateView.as_view(), name='post_create'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/lab/input/request/', views.lab_input_request, name='lab_input_request'),
    path('api/lab/input/provide/', views.lab_input_provide, name='lab_input_provide'),
    path('stackframe.js', views.stackframe_root),
]
