from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .models import Project, Tag

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def getCustomRange(paginated_projects, num_pages=5):
    current_page = paginated_projects.number
    total_pages = paginated_projects.paginator.num_pages

    if total_pages <= num_pages:
        return range(1, total_pages + 1)

    start_page = max(current_page - (num_pages // 2), 1)
    end_page = min(current_page + (num_pages // 2), total_pages)

    if start_page == 1:
        end_page = min(num_pages, total_pages)
    elif end_page == total_pages:
        start_page = max(total_pages - num_pages + 1, 1)

    return range(start_page, end_page + 1)


def paginateProjects(request, projects, items_per_page):
    page = request.GET.get("page")
    paginator = Paginator(projects, items_per_page)

    cache_key_paginated_projects = f"paginated_projects_{page}"
    paginated_projects = cache.get(cache_key_paginated_projects)

    if not paginated_projects:
        try:
            paginated_projects = paginator.page(page)
        except PageNotAnInteger:
            paginated_projects = paginator.page(1)
        except EmptyPage:
            paginated_projects = paginator.page(paginator.num_pages)
        cache.set(cache_key_paginated_projects, paginated_projects, CACHE_TTL)

    custom_range = getCustomRange(paginated_projects)

    return custom_range, paginated_projects


def searchProjects(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    cache_key_tags = f"tags_{search_query}"
    tags = cache.get(cache_key_tags)

    if not tags:
        tags = Tag.objects.filter(name__icontains=search_query)
        cache.set(cache_key_tags, tags, CACHE_TTL)

    cache_key_projects = f"projects_{search_query}"
    projects = cache.get(cache_key_projects)

    if not projects:
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(owner__name__icontains=search_query)
            | Q(tags__in=tags)
        )
        cache.set(cache_key_projects, projects, CACHE_TTL)

    return projects, search_query
