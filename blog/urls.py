from django.urls import path, re_path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(), name='category_posts'),
    path('posts/<int:id>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:id>/edit/',
         views.PostEditView.as_view(), name='edit_post'),
    path('posts/<int:id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:id>/comment/',
         views.AddCommentView.as_view(), name='add_comment'),
    path('posts/<int:id>/comment/edit_comment/<int:comment_id>/',
         views.EditCommentView.as_view(), name='edit_comment'),
    path('posts/<int:id>/comment/delete_comment/<int:comment_id>/',
         views.DeleteCommentView.as_view(), name='delete_comment'),
    re_path(r'profile/(?P<username>[-a-zA-Z0-9]+)/',
            views.ProfileView.as_view(), name='profile'),
    path('profile/edit_profile/',
         views.EditProfileView.as_view(), name='edit_profile'),
]
