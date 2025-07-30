# myapp/management/commands/import_gallery_images.py
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from page_content.models import Image # Make sure this path is correct for your Image model!
from django.utils.translation import gettext_lazy as _ # For verbose_name translation if you use it

class Command(BaseCommand):
    help = _('Imports all image files from a specified folder into the Image model, setting caption to folder name.')

    def add_arguments(self, parser):
        parser.add_argument(
            'source_folder',
            type=str,
            help=_('The path to the folder containing images to import (relative to MEDIA_ROOT). Example: "to_import/vacation_photos"'),
        )
        parser.add_argument(
            '--recursive',
            action='store_true',
            help=_('Recursively import images from subfolders. If used, the caption will be the immediate parent folder name of the image.'),
        )
        parser.add_argument(
            '--delete-after-import',
            action='store_true',
            help=_('Delete the original image file after successful import.'),
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help=_('Skip images that already exist in the database (based on exact file name in image_file field).'),
        )


    def handle(self, *args, **options):
        source_folder_input = options['source_folder']
        recursive = options['recursive']
        delete_after_import = options['delete_after_import']
        skip_existing = options['skip_existing']

        source_path_abs = os.path.normpath(os.path.join(settings.BASE_DIR, "data/img/"+source_folder_input))
        

        if not os.path.isdir(source_path_abs):
            raise CommandError(_(f'Source folder "{source_path_abs}" does not exist or is not a directory.'))
        
        self.stdout.write(self.style.NOTICE(_(f'Starting image import from: {source_path_abs}')))

        imported_count = 0
        skipped_count = 0
        failed_count = 0

        walker = os.walk(source_path_abs) if recursive else [(source_path_abs, [], os.listdir(source_path_abs))]

        for root, aux, files in walker:

            for filename in files:
                if not self.is_image_file(filename):
                    self.stdout.write(self.style.NOTICE(_(f'Skipping non-image file: {filename}')))
                    continue
                full_file_path = os.path.join(root, filename)
                print("full_file_path",full_file_path)
                target_image_path = os.path.join("gallery_images", filename)

                self.stdout.write((f'Processing: {full_file_path}'))

                # Check if an image with this exact file name already exists in the database
                # This checks the 'image_file' field directly.
                 # It relies on the assumption that filename is unique within 'gallery_images/'
                if Image.objects.filter(image_file=target_image_path).exists():
                    self.stdout.write(self.style.WARNING(_(f'Skipping "{filename}" (already exists in database as {target_image_path}).')))
                    skipped_count += 1
                    continue
                
                try:
                    with open(full_file_path, 'rb') as f:
                        django_file = File(f)
                        
                        # Construct the caption: "Folder Name - Original Filename"
                        # Or just "Folder Name" if you prefer
                        image_caption = f"{source_folder_input}-{imported_count}"
                        # Alternatively, just use the folder name:
                        # image_caption = source_folder_input

                        # Create a new Image instance
                        image_instance = Image(
                            caption=image_caption,
                        )
                        
                        # Save the image using the ImageField
                        # The .save() method with a File object handles moving/copying the file
                        # to MEDIA_ROOT/gallery_images/ and setting the image field's path.
                        # It will automatically use the filename provided.
                        image_instance.image_file.save(filename, django_file, save=True)

                    self.stdout.write(self.style.SUCCESS(_(f'Successfully imported: {filename} with caption "{image_instance.caption}"')))
                    imported_count += 1

                    if delete_after_import:
                        os.remove(full_file_path)
                        self.stdout.write(self.style.WARNING(_(f'Deleted original file: {full_file_path}')))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(_(f'Failed to import "{filename}": {e}')))
                    failed_count += 1
                

    def is_image_file(self, filename):
        """Checks if a file has a common image extension."""
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))