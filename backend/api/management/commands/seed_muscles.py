from django.core.management.base import BaseCommand
from api.models import Muscle
from api.services.exercise_service import ExerciseDBService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed the Muscle table with data from ExerciseDB API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing muscle data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting muscle seeding process...'))

        try:
            # Initialize the exercise service
            exercise_service = ExerciseDBService()

            # Test connection first
            success, message = exercise_service.test_connection()
            if not success:
                self.stdout.write(
                    self.style.ERROR(f'Failed to connect to ExerciseDB API: {message}')
                )
                return

            self.stdout.write(self.style.SUCCESS('Connected to ExerciseDB API successfully'))

            # Clear existing data if requested
            if options['clear']:
                self.stdout.write('Clearing existing muscle data...')
                deleted_count = Muscle.objects.all().delete()[0]
                self.stdout.write(
                    self.style.WARNING(f'Deleted {deleted_count} existing muscle records')
                )

            # Get muscles from the API
            self.stdout.write('Fetching muscle data from ExerciseDB API...')
            result = exercise_service.get_muscles()

            if not result.get('success', False):
                self.stdout.write(
                    self.style.ERROR(f'Failed to fetch muscles: {result.get("error", "Unknown error")}')
                )
                return

            muscles_data = result.get('data', {}).get('data', [])
            self.stdout.write(f'Retrieved {len(muscles_data)} muscles from API')

            # Seed the muscles
            created_count = 0
            updated_count = 0

            for muscle_data in muscles_data:
                muscle_name = muscle_data.get('name', '').strip()
                
                if not muscle_name:
                    self.stdout.write(
                        self.style.WARNING(f'Skipping muscle with empty name: {muscle_data}')
                    )
                    continue

                # Create or update muscle
                muscle, created = Muscle.objects.get_or_create(
                    name=muscle_name,
                    defaults={'name': muscle_name}
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'Created muscle: {muscle_name}')
                else:
                    updated_count += 1
                    self.stdout.write(f'Muscle already exists: {muscle_name}')

            # Summary
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n=== Muscle Seeding Complete ===\n'
                    f'Total muscles processed: {len(muscles_data)}\n'
                    f'New muscles created: {created_count}\n'
                    f'Existing muscles found: {updated_count}\n'
                    f'Total muscles in database: {Muscle.objects.count()}'
                )
            )

        except Exception as e:
            logger.error(f'Error during muscle seeding: {e}')
            self.stdout.write(
                self.style.ERROR(f'An error occurred during seeding: {str(e)}')
            )
            raise e