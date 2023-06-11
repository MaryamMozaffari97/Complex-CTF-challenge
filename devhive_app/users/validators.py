import logging

import magic
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from lxml import etree

logger = logging.getLogger(__name__)


class SVGFileValidator(FileExtensionValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xml_parser = etree.XMLParser(
            encoding="UTF-8",
            load_dtd=True,
            no_network=False,
            resolve_entities=True,
            recover=False,
            huge_tree=True,
        )

    def __call__(self, value):
        if value.name.endswith(".svg") and isinstance(
            value, (File, InMemoryUploadedFile)
        ):
            try:
                with value.open("rb") as image_file:
                    etree.parse(image_file, self.xml_parser)

            except etree.XMLSyntaxError as exc:
                logger.error(str(exc), exc_info=True)
                raise ValidationError(str(exc))

        super().__call__(value)


class MimeTypeValidator(FileExtensionValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_types = ["image/jpeg", "image/svg+xml", "text/xml"]

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(), mime=True)
            if mime not in self.allowed_types:
                raise TypeError("forbidden file type")

        except TypeError as exc:
            raise ValidationError(str(exc))
        super().__call__(value)
