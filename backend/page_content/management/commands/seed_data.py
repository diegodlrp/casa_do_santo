import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.files import File  # <-- Import File class

from django.contrib.auth.models import User
from page_content.models import Tag, PageContent
# from web_data.models import WebData
from django.conf import settings  # Import settings to get MEDIA_ROOT

# Define the base directory for your seed images
# Adjust this path if your seed_images folder is elsewhere
SEED_IMAGES_DIR = os.path.join(settings.BASE_DIR, "data/img")


class Command(BaseCommand):
    help = "Populates the database with default data for development/testing."

    def add_arguments(self, parser):
        # Optional: Add arguments to control behavior
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before loading new data (for specified models).",
        )
        parser.add_argument(
            "--load-from-json",
            type=str,
            help="Path to a JSON file containing seed data.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not actually modify the database, just show what would be done.",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding..."))

        # Access models here to avoid circular imports if models import settings
        # from django.apps import apps
        # Product = apps.get_model('myapp', 'Product')
        # from myapp.models import Product # Assuming Product is in myapp/models.py

        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            try:
                # Order matters when clearing if there are Foreign Keys or ManyToMany
                PageContent.objects.all().delete()  # Delete pages first
                Tag.objects.all().delete()  # Then delete tags
                User.objects.all().delete()  # Be careful clearing all users! You might want to filter.
                self.stdout.write(self.style.SUCCESS("Cleared existing data."))
            except Exception as e:
                raise CommandError(f"Error clearing data: {e}")

        data_to_load = {}

        if options["load_from_json"]:
            json_path = options["load_from_json"]
            if not os.path.exists(json_path):
                raise CommandError(f"JSON file not found at: {json_path}")
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data_to_load = json.load(f)
                self.stdout.write(
                    self.style.SUCCESS(f"Loaded data from JSON: {json_path}")
                )
            except json.JSONDecodeError as e:
                raise CommandError(f"Invalid JSON file: {e}")
            except Exception as e:
                raise CommandError(f"Error reading JSON file: {e}")
        else:
            # Placeholder for hardcoded data if no JSON specified
            data_to_load = {
                # Ensure you have data structures here if not loading from JSON
                "users": [],  # Example: DEFAULT_USERS_HARDCODED
                "tags": [],  # Example: DEFAULT_TAGS_HARDCODED
                "page_content": [],  # Example: DEFAULT_PAGE_CONTENTS_HARDCODED
            }
            # You should populate these with your actual hardcoded data if you use this branch
            # e.g., data_to_load['users'] = DEFAULT_USERS_HARDCODED
            # e.g., data_to_load['tags'] = DEFAULT_TAGS_HARDCODED
            # e.g., data_to_load['page_content'] = DEFAULT_PAGE_CONTENTS_HARDCODED

        if options["dry_run"]:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n--- DRY RUN: No changes will be made to the database ---"
                )
            )

        try:
            with transaction.atomic():
                # --- 1. Seed Users ---
                users_data = data_to_load.get("users", [])
                if users_data:
                    self.stdout.write(
                        self.style.NOTICE(f"\nSeeding {len(users_data)} User(s)...")
                    )
                    for user_item in users_data:
                        username = user_item["username"]
                        # IMPORTANT: Use create_user for proper password hashing
                        if not User.objects.filter(username=username).exists():
                            if not options["dry_run"]:
                                # Create user by popping password and using create_user
                                password = user_item.pop("password")
                                user = User.objects.create_user(
                                    password=password, **user_item
                                )
                                self.stdout.write(
                                    self.style.SUCCESS(f"  Created User: {username}")
                                )
                            else:
                                self.stdout.write(
                                    self.style.NOTICE(
                                        f"  (Dry Run) Would create User: {username}"
                                    )
                                )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  User already exists, skipping: {username}"
                                )
                            )
                else:
                    self.stdout.write(self.style.WARNING("No User data found to seed."))

                # --- 2. Seed Tags ---
                tags_data = data_to_load.get("tags", [])
                # Store created tag instances in a map for efficient lookup later
                tag_instance_map = {}
                if tags_data:
                    self.stdout.write(
                        self.style.NOTICE(f"\nSeeding {len(tags_data)} Tag(s)...")
                    )
                    for tag_item in tags_data:
                        name = tag_item["name"]
                        # Use get_or_create to ensure tags exist and get their instances
                        tag_obj, created = Tag.objects.get_or_create(
                            name=name,
                            defaults=tag_item,  # Pass full item to defaults if Tag has other fields
                        )
                        tag_instance_map[name] = (
                            tag_obj  # Store the instance for later lookup
                        )
                        if created:
                            if not options["dry_run"]:
                                self.stdout.write(
                                    self.style.SUCCESS(f"  Created Tag: '{name}'")
                                )
                            else:
                                self.stdout.write(
                                    self.style.NOTICE(
                                        f"  (Dry Run) Would create Tag: '{name}'"
                                    )
                                )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Tag already exists: '{name}', skipping creation."
                                )
                            )
                else:
                    self.stdout.write(self.style.WARNING("No Tags data found to seed."))

                # --- 3. Seed Page_content ---
                page_content_data = data_to_load.get("page_content", [])
                if page_content_data:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"\nSeeding {len(page_content_data)} Page Content item(s)..."
                        )
                    )
                    for item in page_content_data:
                        slug = item[
                            "slug"
                        ]  # Assuming slug is unique and used for check
                        if not PageContent.objects.filter(slug=slug).exists():
                            # Extract related data (tags and image) before creating PageContent
                            tags_names_for_page = item.pop(
                                "tags", []
                            )  # List of tag names from JSON
                            image_filename = item.pop(
                                "image", None
                            )  # Image filename from JSON

                            if not options["dry_run"]:
                                # Create the PageContent instance first
                                page_content = PageContent.objects.create(**item)
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"  Created Page Content: '{slug}'"
                                    )
                                )

                                # Process and set tags for the PageContent
                                if tags_names_for_page:
                                    # Collect actual Tag instances
                                    tags_to_set = []
                                    for tag_name in tags_names_for_page:
                                        tag_instance = tag_instance_map.get(tag_name)

                                        if tag_instance:
                                            tags_to_set.append(tag_instance)
                                        else:
                                            self.stdout.write(
                                                self.style.WARNING(
                                                    f"    Tag '{tag_name}' not found for page '{slug}'. Skipping this tag for the page."
                                                )
                                            )

                                    if tags_to_set:
                                        page_content.tags.set(
                                            tags_to_set
                                        )  # Assign all valid tag instances
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f"    Assigned tags to '{slug}': {[t.name for t in tags_to_set]}"
                                            )
                                        )
                                    else:
                                        self.stdout.write(
                                            self.style.WARNING(
                                                f"    No valid tags found to assign for page: '{slug}'."
                                            )
                                        )
                                else:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"    No tags specified in data for page: '{slug}'."
                                        )
                                    )

                                # Handle the image file for the PageContent
                                if image_filename:
                                    image_path = os.path.join(
                                        SEED_IMAGES_DIR, image_filename
                                    )
                                    if os.path.exists(image_path):
                                        with open(image_path, "rb") as f:
                                            # Save the image to the ImageField
                                            page_content.image.save(
                                                image_filename, File(f)
                                            )
                                            # No need for an extra page_content.save() here as .save() on ImageField does it
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f"    Attached image: '{image_filename}' to '{slug}'"
                                            )
                                        )
                                    else:
                                        self.stdout.write(
                                            self.style.WARNING(
                                                f"    Image file not found: {image_path} for page '{slug}'. Skipping image attachment."
                                            )
                                        )
                                else:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"    No image filename provided for page: '{slug}'."
                                        )
                                    )
                            else:  # Dry run for page content
                                self.stdout.write(
                                    self.style.NOTICE(
                                        f"  (Dry Run) Would create Page Content: '{slug}' (Tags: {tags_names_for_page}, Image: {image_filename if image_filename else 'None'})"
                                    )
                                )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Page Content already exists, skipping: '{slug}'"
                                )
                            )
                else:
                    self.stdout.write(
                        self.style.WARNING("No Page Content data found to seed.")
                    )






                # # --- 4. Seed WebData ---
                # web_data_data = data_to_load.get("web_data", [])
                # if web_data_data:
                #     self.stdout.write(
                #         self.style.NOTICE(f"\nSeeding {len(web_data_data)} User(s)...")
                #     )
                #     for item in web_data_data:
                #         name = item["name"]
                #         # IMPORTANT: Use create_user for proper password hashing
                #         if not WebData.objects.filter(name=name).exists():
                #             if not options["dry_run"]:   
                #                 WebData.objects.create(
                #                    **item
                #                 )
                #                 self.stdout.write(
                #                     self.style.SUCCESS(f"  Created User: {name}")
                #                 )
                #             else:
                #                 self.stdout.write(
                #                     self.style.NOTICE(
                #                         f"  (Dry Run) Would create User: {name}"
                #                     )
                #                 )
                #         else:
                #             self.stdout.write(
                #                 self.style.WARNING(
                #                     f"  User already exists, skipping: {name}"
                #                 )
                #             )
                # else:
                #     self.stdout.write(self.style.WARNING("No User data found to seed."))

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"An error occurred during seeding: {e}")
            )
            raise CommandError(f"Seeding failed: {e}")

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding completed!"))
