from django.contrib import admin
from .models import (
    Topic,
    Article,
    Bookmark,
    FollowedTopic,
    Comment,
    Poll,
    PollOption,
    PollVote,
    ReadingHistory,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "published_at",
        "views",
        "is_trending",
    )
    list_filter = ("category", "is_trending")
    search_fields = ("title", "description", "content", "author")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title")


@admin.register(FollowedTopic)
class FollowedTopicAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "followed_at")
    search_fields = ("user__username", "topic__name")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title", "text")


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("question",)


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ("poll", "option_text", "votes")
    search_fields = ("poll__question", "option_text")


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "poll", "option")
    search_fields = ("user__username", "poll__question")


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "read_at")
    list_filter = ("read_at",)
    search_fields = ("user__username", "article__title")