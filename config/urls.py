from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from newsly import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Main pages
    path("", views.home, name="home"),
    path("community/", views.community, name="community"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("news/", views.news, name="news"),
    path("topics/", views.topics, name="topics"),
    path("profile/", views.profile, name="profile"),

    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Bookmark
    path(
        "bookmark/<int:article_id>/",
        views.bookmark_article,
        name="bookmark_article"
    ),

    # Article
    path(
        "article/<int:article_id>/",
        views.article_detail,
        name="article_detail"
    ),

    # Comments
    path(
        "article/<int:article_id>/comment/",
        views.add_comment,
        name="add_comment"
    ),

    path(
        "comment/edit/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment"
    ),

    path(
        "comment/delete/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"
    ),

    # Topics
    path(
        "topic/<int:topic_id>/follow/",
        views.follow_topic,
        name="follow_topic"
    ),

    # Poll
    path(
        "poll/<int:poll_id>/vote/",
        views.vote_poll,
        name="vote_poll"
    ),
]


urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]