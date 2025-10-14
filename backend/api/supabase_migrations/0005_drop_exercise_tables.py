# Generated manually on 2025-10-13
# Drop exercise metadata tables that are no longer needed

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_simplify_workout_plan_schema'),
    ]

    operations = [
        # Drop junction tables first to avoid foreign key constraints
        migrations.RunSQL("DROP TABLE IF EXISTS exercise_muscles CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS exercise_equipment CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS exercise_body_parts CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS exercise_keywords CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS related_exercises CASCADE;"),
        
        # Drop main exercise metadata tables
        migrations.RunSQL("DROP TABLE IF EXISTS exercises CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS muscles CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS equipment CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS body_parts CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS keywords CASCADE;"),
        
        # Update workout_log table structure
        migrations.RunSQL("ALTER TABLE workout_log DROP COLUMN IF EXISTS exercise_id CASCADE;"),
        migrations.RunSQL("ALTER TABLE workout_log ADD COLUMN IF NOT EXISTS exercise_name VARCHAR(255) DEFAULT '';"),
        migrations.RunSQL("ALTER TABLE workout_log ADD COLUMN IF NOT EXISTS exercise_data JSONB DEFAULT '{}';"),
    ]