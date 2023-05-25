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
        logger.error(
            f"error of type {e.__class__.__name__} occured when parsing image",
            exc_info=True,
        )
        raise ValueError(f"Invalid XML: {e}")
    except Exception as e:
        logger.error(
            f"error of type {e.__class__.__name__} occured when parsing image",
            exc_info=True,
        )
        raise ValueError(f"Unexpected error: {e}") from e

    return tree
