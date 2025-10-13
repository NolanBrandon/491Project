# Generated manually on 2025-10-13
# Drop foods table and update nutrition_log to use food_name instead of foreign key

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_drop_exercise_tables'),
    ]

    operations = [
        # Drop the foods table
        migrations.RunSQL("DROP TABLE IF EXISTS foods CASCADE;"),
        
        # Update nutrition_log table structure
        migrations.RunSQL("ALTER TABLE nutrition_log DROP COLUMN IF EXISTS food_id CASCADE;"),
        migrations.RunSQL("ALTER TABLE nutrition_log ADD COLUMN IF NOT EXISTS food_name VARCHAR(255) DEFAULT '';"),
        migrations.RunSQL("ALTER TABLE nutrition_log ADD COLUMN IF NOT EXISTS food_data JSONB DEFAULT '{}';"),
    ]