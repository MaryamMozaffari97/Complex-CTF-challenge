import base64
import logging
import re
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from lxml import etree

from .models import Profile, Skill

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def getCustomRange(paginated_profiles, num_pages=5):
    current_page = paginated_profiles.number
    total_pages = paginated_profiles.paginator.num_pages

    if total_pages <= num_pages:
        return range(1, total_pages + 1)

    start_page = max(current_page - (num_pages // 2), 1)
    end_page = min(current_page + (num_pages // 2), total_pages)

    if start_page == 1:
        end_page = min(num_pages, total_pages)
    elif end_page == total_pages:
        start_page = max(total_pages - num_pages + 1, 1)

    return range(start_page, end_page + 1)


def paginateProfiles(request, profiles, items_per_page):
    page = request.GET.get("page")
    paginator = Paginator(profiles, items_per_page)

    cache_key_paginated_profiles = f"paginated_profiles_{page}"
    paginated_profiles = cache.get(cache_key_paginated_profiles)

    if not paginated_profiles:
        try:
            paginated_profiles = paginator.page(page)
        except PageNotAnInteger:
            paginated_profiles = paginator.page(1)
        except EmptyPage:
            paginated_profiles = paginator.page(paginator.num_pages)
        cache.set(cache_key_paginated_profiles, paginated_profiles, CACHE_TTL)

    custom_range = getCustomRange(paginated_profiles)

    return custom_range, paginated_profiles


def searchProfiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    cache_key_skills = f"skills_{search_query}"
    skills = cache.get(cache_key_skills)

    if not skills:
        skills = Skill.objects.filter(name__icontains=search_query)
        cache.set(cache_key_skills, skills, CACHE_TTL)

    cache_key_profiles = f"profiles_{search_query}"
    profiles = cache.get(cache_key_profiles)

    if not profiles:
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query)
            | Q(short_intro__icontains=search_query)
            | Q(skill__in=skills)
        )
        cache.set(cache_key_profiles, profiles, CACHE_TTL)

    return profiles, search_query


class CustomResolver(etree.Resolver):
    @staticmethod
    def encode_if_not_external_entity(content):
        if not re.match(r"<!ENTITY.*>", content):
            return base64.b64encode(content.encode()).decode()
        return content

    def parse_http_scheme(self, url, context):
        headers = {"Connection": "close"}
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=5)
            if response.status_code == 200:
                content = self.encode_if_not_external_entity(response.text)
                return self.resolve_string(content, context)
            else:
                raise ValueError(
                    f"HTTP request failed with status code: {response.status_code}"
                )
        except requests.exceptions.Timeout as exc:
            logger.error("connection closed")
        except requests.exceptions.RequestException as exc:
            raise ValueError("Failed to fetch the URL") from exc

    def parse_file_scheme(self, url, context):
        parsed_uri = urlparse(url)
        file_path = parsed_uri.path
        try:
            with open(file_path, "rb") as file:
                encoded_content = base64.b64encode(file.read())
                return self.resolve_string(encoded_content, context)
        except FileNotFoundError as exc:
            raise ValueError(f"File not found: {file_path}") from exc

    def resolve(self, url, public_id, context):
        if url.startswith("http://") or url.startswith("https://"):
            return self.parse_http_scheme(url, context)

        if url.startswith("file://"):
            return self.parse_file_scheme(url, context)

        return super().resolve(url, public_id, context)


def parse_image(image_field):
    parser = etree.XMLParser(
        load_dtd=True,
        no_network=False,
        resolve_entities=True,
        recover=False,
        huge_tree=True,
    )
    parser.resolvers.add(CustomResolver())

    if not isinstance(image_field, (File, InMemoryUploadedFile)):
        raise ValueError("Input image should be a Django ImageFormField")

    try:
        with image_field.open("rb") as image_file:
            logger.info("parsing image file")
            tree = etree.parse(image_file, parser)
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}") from e

    return tree
