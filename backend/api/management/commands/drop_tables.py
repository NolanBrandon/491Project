from django.core.management.base import BaseCommand
from django.db import connection
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Drop all API-related tables to prepare for schema restructure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to drop all tables (required for safety)',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    'This command will DROP ALL API TABLES and ALL DATA will be LOST!\n'
                    'Add --confirm flag if you really want to proceed.'
                )
            )
            return

        self.stdout.write(self.style.WARNING('Starting table drop process...'))

        # List of tables to drop (based on the existing schema)
        tables_to_drop = [
            'exercise_keywords',
            'exercise_muscles', 
            'exercise_equipments',
            'exercise_body_parts',
            'related_exercises',
            'plan_exercises',
            'plan_days',
            'workout_plans',
            'workout_log',
            'exercises',
            'muscles',
            'equipments', 
            'body_parts',
            'keywords',
            'meal_plan_entries',
            'meal_plan_days', 
            'meal_plans',
            'recipe_tags',
            'recipe_ingredients',
            'recipes',
            'ingredients',
            'tags',
            'nutrition_log',
            'foods',
            'goals',
            'user_metrics',
            'users',
            'api_userprofile'
        ]

        with connection.cursor() as cursor:
            dropped_count = 0
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                    dropped_count += 1
                    self.stdout.write(f"Dropped table: {table}")
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Could not drop table {table}: {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== Table Drop Complete ===\n'
                f'Attempted to drop {len(tables_to_drop)} tables\n'
                f'Successfully processed {dropped_count} tables\n'
                f'Database is now ready for fresh migrations'
            )
        )