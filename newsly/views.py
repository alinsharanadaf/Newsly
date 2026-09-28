from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (
    Article,
    Bookmark,
    FollowedTopic,
    ReadingHistory,
    Comment,
    Topic,
    Poll,
    PollOption,
    PollVote,
)


# =========================
# HOME
# =========================

def home(request):

    trending_articles = Article.objects.filter(
        is_trending=True
    ).order_by("-views")[:6]

    latest_articles = Article.objects.all().order_by(
        "-published_at"
    )[:6]

    recommended_articles = Article.objects.none()

    if request.user.is_authenticated:

        read_article_ids = ReadingHistory.objects.filter(
            user=request.user
        ).values_list(
            "article_id",
            flat=True
        )

        followed_topic_ids = FollowedTopic.objects.filter(
            user=request.user
        ).values_list(
            "topic_id",
            flat=True
        )

        followed_topics = Topic.objects.filter(
            id__in=followed_topic_ids
        ).values_list(
            "name",
            flat=True
        )

        recommended_articles = Article.objects.exclude(
            id__in=read_article_ids
        )

        if followed_topics:
            recommended_articles = recommended_articles.filter(
                category__in=followed_topics
            )

        recommended_articles = recommended_articles.order_by(
            "-views",
            "-published_at"
        )[:6]

    return render(
        request,
        "website/home.html",
        {
            "trending_articles": trending_articles,
            "latest_articles": latest_articles,
            "recommended_articles": recommended_articles,
        }
    )


# =========================
# COMMUNITY & POLLS
# =========================

@login_required
def community(request):

    polls = list(
        Poll.objects.filter(
            is_active=True
        ).prefetch_related(
            "options"
        ).order_by(
            "-created_at"
        )
    )

    voted_poll_ids = set(
        PollVote.objects.filter(
            user=request.user,
            poll__in=polls
        ).values_list(
            "poll_id",
            flat=True
        )
    )

    for poll in polls:

        options = list(
            poll.options.all()
        )

        total_votes = sum(
            option.votes
            for option in options
        )

        poll.total_votes = total_votes
        poll.user_voted = poll.id in voted_poll_ids

        for option in options:

            if total_votes > 0:
                option.percentage = round(
                    (option.votes / total_votes) * 100
                )
            else:
                option.percentage = 0

    return render(
        request,
        "website/community.html",
        {
            "polls": polls,
        }
    )


@login_required
def vote_poll(request, poll_id):

    poll = get_object_or_404(
        Poll,
        id=poll_id,
        is_active=True
    )

    if request.method == "POST":

        option_id = request.POST.get("option")

        option = get_object_or_404(
            PollOption,
            id=option_id,
            poll=poll
        )

        already_voted = PollVote.objects.filter(
            user=request.user,
            poll=poll
        ).exists()

        if not already_voted:

            PollVote.objects.create(
                user=request.user,
                poll=poll,
                option=option
            )

            option.votes += 1
            option.save(
                update_fields=["votes"]
            )

    return redirect("community")


# =========================
# STATIC PAGES
# =========================

def about(request):
    return render(
        request,
        "website/about.html"
    )


def contact(request):
    return render(
        request,
        "website/contact.html"
    )


# =========================
# NEWS
# =========================

def news(request):

    articles = Article.objects.all().order_by(
        "-published_at"
    )

    search_query = request.GET.get(
        "q",
        ""
    ).strip()

    selected_category = request.GET.get(
        "category",
        ""
    )

    if search_query:

        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    if selected_category:

        articles = articles.filter(
            category=selected_category
        )

    categories = [
        choice[0]
        for choice in Article.CATEGORY_CHOICES
    ]

    return render(
        request,
        "website/news.html",
        {
            "articles": articles,
            "categories": categories,
            "search_query": search_query,
            "selected_category": selected_category,
        }
    )


# =========================
# TOPICS
# =========================

@login_required
def topics(request):

    topics = Topic.objects.all()

    followed_topics = FollowedTopic.objects.filter(
        user=request.user
    ).values_list(
        "topic_id",
        flat=True
    )

    return render(
        request,
        "website/topics.html",
        {
            "topics": topics,
            "followed_topics": followed_topics,
        }
    )


@login_required
def follow_topic(request, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    followed = FollowedTopic.objects.filter(
        user=request.user,
        topic=topic
    ).first()

    if followed:
        followed.delete()
    else:
        FollowedTopic.objects.create(
            user=request.user,
            topic=topic
        )

    return redirect("topics")


# =========================
# PROFILE
# =========================

@login_required
def profile(request):
    saved_articles = Article.objects.filter(
        bookmark__user=request.user
    ).distinct().order_by("-published_at")

    reading_history = ReadingHistory.objects.filter(
        user=request.user
    ).select_related("article").order_by("-read_at")

    followed_topics = FollowedTopic.objects.filter(
        user=request.user
    ).select_related("topic")

    return render(
        request,
        "website/profile.html",
        {
            "saved_articles": saved_articles,
            "reading_history": reading_history,
            "followed_topics": followed_topics,
        }
    )


# =========================
# BOOKMARK
# =========================

@login_required
def bookmark_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    bookmark = Bookmark.objects.filter(
        user=request.user,
        article=article
    ).first()

    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(
            user=request.user,
            article=article
        )

    return redirect("news")


# =========================
# ARTICLE DETAIL
# =========================

@login_required
def article_detail(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    article.views += 1
    article.save(
        update_fields=["views"]
    )

    ReadingHistory.objects.get_or_create(
        user=request.user,
        article=article
    )

    comments = Comment.objects.filter(
        article=article
    ).select_related(
        "user"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "website/article_detail.html",
        {
            "article": article,
            "comments": comments,
        }
    )


# =========================
# ADD COMMENT
# =========================

@login_required
def add_comment(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":

        comment_text = request.POST.get(
            "comment"
        )

        if comment_text and comment_text.strip():

            Comment.objects.create(
                user=request.user,
                article=article,
                text=comment_text.strip()
            )

    return redirect(
        "article_detail",
        article_id=article.id
    )


# =========================
# DELETE COMMENT
# =========================

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    article_id = comment.article.id

    if request.method == "POST":
        comment.delete()

    return redirect(
        "article_detail",
        article_id=article_id
    )


# =========================
# EDIT COMMENT
# =========================

@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    if request.method == "POST":

        comment_text = request.POST.get(
            "comment"
        )

        if comment_text and comment_text.strip():

            comment.text = comment_text.strip()
            comment.save()

            return redirect(
                "article_detail",
                article_id=comment.article.id
            )

    return render(
        request,
        "website/edit_comment.html",
        {
            "comment": comment,
        }
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("profile")

        return render(
            request,
            "website/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "website/login.html"
    )


# =========================
# REGISTER
# =========================

def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("profile")

    else:

        form = UserCreationForm()

    return render(
        request,
        "website/register.html",
        {
            "form": form
        }
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect("home")