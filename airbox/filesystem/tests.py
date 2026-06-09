import os
import shutil
import tempfile
import uuid
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from airbox.filesystem.models import File, Folder, path_generator
from airbox.iam.models import Organisation, User, Member, Role


class FileTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_directory = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_directory)

    def setUp(self):
        self.user = User.objects.create_user(email=f'{uuid.uuid4()}@outlook.com', password='password1234!.', first_name='John', last_name='Doe')
        self.organisation = Organisation.objects.create(name=str(uuid.uuid4()))
        self.member = Member.objects.create(user=self.user, organisation=self.organisation, role=Role.ADMIN.name)

    def test_clean_no_file_raises_validation_error(self):
        file = File()
        with self.assertRaises(ValidationError) as exception:
            file.clean()
        self.assertEqual('file was not provided', exception.exception.args[0])

    def test_clean_unsupported_mime_type_raises_validation_error(self):
        file = File(file=SimpleUploadedFile('file.exe', b'This is some content!'))
        with self.assertRaises(ValidationError) as exception:
            file.clean()
        self.assertEqual('mime type application/x-msdos-program is not allowed', exception.exception.args[0])

    def test_clean_max_size_exceeded_raises_validation_error(self):
        upload = MagicMock()
        upload.name = 'file.text'
        upload.size = 11 * 1024 * 1024
        file = File(file=upload)
        with self.assertRaises(ValidationError) as exception:
            file.clean()
        self.assertEqual('file size exceeds 10.0 MB limit', exception.exception.args[0])

    def test_save(self):
        folder = Folder.objects.create(name='folder', owner=self.member, organisation=self.organisation)
        file = File(file=SimpleUploadedFile('test.txt', b'This is some content!'), folder=folder, owner=self.member)
        with override_settings(MEDIA_ROOT=self.test_directory):
            file.save()
        other = File.objects.get(id=file.id)
        self.assertEqual(file.mime_type, other.mime_type)
        self.assertTrue(os.path.exists(os.path.join(self.test_directory, path_generator(file, file.name))))
