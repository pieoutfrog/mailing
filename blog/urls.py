from django.urls import path

from blog.views import BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blog'

urlpatterns = [
    path('blogpost/view/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blogpost/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('blogpost/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    path('blogpost/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blogpost/view/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_view'),
]
