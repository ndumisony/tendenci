import os
import chardet

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Command(BaseCommand):
    """
    Pre-precess the chapter memberships import:

        1) Encode the uploaded file.
        2) Dump data to table chaptermembershipimportdata

    Usage:
        python manage.py chapter_membership_import_preprocess [mimport_id]

        example:
        python manage.py chapter_membership_import_preprocess 1
    """

    def add_arguments(self, parser):
        parser.add_argument('import_id', type=int)

    def handle(self, *args, **options):
        from tendenci.apps.chapters.models import ChapterMembershipImport, ChapterMembershipImportData
        from tendenci.apps.memberships.utils import memb_import_parse_csv

        import_id = options['import_id']
        mimport = get_object_or_404(ChapterMembershipImport,
                                        pk=import_id)
        if mimport.status == 'not_started':
            if mimport.upload_file:
                mimport.status = 'preprocessing'
                mimport.save()

                # encode to utf8 and write to path2
                path2 = '%s_utf8%s' % (os.path.splitext(
                                        mimport.upload_file.name))
                default_storage.save(path2, ContentFile(b''))
                f = default_storage.open(mimport.upload_file.name)
                f2 = default_storage.open(path2, 'wb+')
                encoding_updated = False
                encoding = chardet.detect(f.read())['encoding']
                if encoding == 'ISO-8859-1' or \
                    encoding == 'ISO-8859-2':
                    encoding = 'latin-1'
                for chunk in f.chunks():
                    if encoding not in ('ascii', 'utf8'):
                        chunk = chunk.decode(encoding)
                        chunk = chunk.encode('utf8')
                        encoding_updated = True
                    f2.write(chunk)
                f2.close()
                if encoding_updated:
                    mimport.upload_file.file = f2
                    mimport.upload_file.name = f2.name
                    mimport.save()
                else:
                    default_storage.delete(path2)

                # dump data to the table membershipimportdata
                # note that row_num starts with 2 because the first row
                # is the header row.
                header_line, data_list = memb_import_parse_csv(mimport)
                mimport.header_line = ','.join(header_line)

                for i, memb_data in enumerate(data_list):

                    import_data = ChapterMembershipImportData(
                                    mimport=mimport,
                                    row_data=memb_data,
                                    row_num=i+2)
                    import_data.save()

                mimport.status = 'preprocess_done'
                mimport.save()
