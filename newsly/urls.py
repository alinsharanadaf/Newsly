from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        "",
        views.home,
        name="home"
    ),

    # COMMUNITY
    path(
        "community/",
        views.community,
        name="community"
    ),

    # STATIC PAGES
    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    # NEWS
    path(
        "news/",
        views.news,
        name="news"
    ),

    # TOPICS
    path(
        "topics/",
        views.topics,
        name="topics"
    ),

    # PROFILE
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # LOGIN
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # REGISTER
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    # LOGOUT
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # BOOKMARK
    path(
        "bookmark/<int:article_id>/",
        views.bookmark_article,
        name="bookmark_article"
    ),

    # ARTICLE DETAIL
    path(
        "article/<int:article_id>/",
        views.article_detail,
        name="article_detail"
    ),

    # ADD COMMENT
    path(
        "comment/add/<int:article_id>/",
        views.add_comment,
        name="add_comment"
    ),

    # DELETE COMMENT
    path(
        "comment/delete/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"
    ),

    # EDIT COMMENT
    path(
        "comment/edit/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment"
    ),

    # VOTE POLL
    path(
        "poll/vote/<int:poll_id>/",
        views.vote_poll,
        name="vote_poll"
    ),

    # FOLLOW TOPIC
    path(
        "topic/follow/<int:topic_id>/",
        views.follow_topic,
        name="follow_topic"
    ),
]