import mimetypes
import os

from django.core.exceptions import ValidationError
from django.db.models import Model, DateTimeField, CharField, ForeignKey, CASCADE, FileField, BigIntegerField

from airbox.iam.models import Member, Organisation


class Node(Model):

    class Meta:
        abstract = True

    name = CharField(max_length=200)
    owner = ForeignKey(Member, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Folder(Node):
    organisation = ForeignKey(Organisation, on_delete=CASCADE)
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE, related_name='children')


ALLOWED_MIME_TYPES = [
    mimetypes.types_map['.jpg'],
    mimetypes.common_types['.jpg'],
    mimetypes.types_map['.jpeg'],
    mimetypes.types_map['.png'],
    mimetypes.types_map['.pdf'],
    mimetypes.types_map['.txt']
]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit


def path_generator(instance, filename):
    return os.path.join(str(instance.folder.organisation.id), str(instance.owner.id), instance.folder.name, filename)


class File(Node):
    file = FileField(upload_to=path_generator)
    size = BigIntegerField(editable=False)
    mime_type = CharField(max_length=100, editable=False)
    folder = ForeignKey(Folder, on_delete=CASCADE, related_name='files')

    def clean(self):
        super().clean()
        if not self.file:
            raise ValidationError('file was not provided')
        mime_type, _ = mimetypes.guess_type(self.file.name)
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(f'mime type {mime_type} is not allowed')
        if self.file.size > MAX_FILE_SIZE:
            raise ValidationError(f'file size exceeds {MAX_FILE_SIZE / (1024 * 1024)} MB limit')

    def save(self, *args, **kwargs):
        if not self.file:
            raise ValidationError('file was not provided')
        self.size = self.file.size
        mime_type, _ = mimetypes.guess_type(self.file.name)
        self.mime_type = mime_type
        super().save(*args, **kwargs)
