import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q

from .models import Profile, Skill

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def searchProfiles(request):
    search_query = request.GET.get("search_query", "")

    skills = cache.get(f"skills_{search_query}")
    if skills is None:
        skills = Skill.objects.filter(name__icontains=search_query)
        cache.set(f"skills_{search_query}", skills, CACHE_TTL)

    profiles = cache.get(f"profiles_{search_query}")
    if profiles is None:
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query)
            | Q(short_intro__icontains=search_query)
            | Q(skill__in=skills)
        )
        cache.set(f"profiles_{search_query}", profiles, CACHE_TTL)

    return profiles, search_query


class ForbiddenPathError(Exception):
    pass
