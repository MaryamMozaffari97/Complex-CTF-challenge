from django.db.models import Q
from .models import Profile, Skill

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    page = request.GET.get("page")
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = int(page) - 4

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(short_intro__icontains=search_query)
        | Q(skill__in=skills)
    )
    return profiles, search_query


from urllib.parse import urlparse
from lxml import etree
import socket
import base64


class CustomResolver(etree.Resolver):
    def parse_http_scheme(self, url):
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.split(":")[0]
        port = parsed_url.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((hostname, port))
                request = f"GET / HTTP/1.1\r\nHost: {url}\r\n\r\n"
                s.sendall(request.encode())
            except BrokenPipeError as exc:
                pass
            except Exception as exc:
                raise ValueError

    def parse_file_scheme(self, url):
        parsed_uri = urlparse(url)
        file_path = parsed_uri.path
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read())
        except FileNotFoundError:
            raise ValueError

    def resolve(self, url, public_id, context):
        if url.startswith("http://") or url.startswith("https://"):
            self.parse_http_scheme(url)

        if url.startswith("file://"):
            encoded_string = self.parse_file_scheme(url)
            if encoded_string is not None:
                return self.resolve_string(encoded_string, context)

        super().resolve(url, public_id, context)


def parse_image(image_file):
    parser = etree.XMLParser(
        load_dtd=True,
        no_network=False,
        resolve_entities=True,
        recover=False,
        huge_tree=True,
    )
    parser.resolvers.add(CustomResolver())
    try:
        tree = etree.parse(image_file, parser)
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML: {e}")
