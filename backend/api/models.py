from django.db import models
from django.core.exceptions import ValidationError
import uuid

# -------------------------------
# User Management & Core Tracking Module
# -------------------------------

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True, default='')
    password_hash = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    last_login_date = models.DateField(null=True, blank=True)
    login_streak = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class UserMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_recorded = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    activity_level = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'user_metrics'

    def __str__(self):
        return f"{self.user.username} metrics on {self.date_recorded}"


class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, default='')
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'goals'

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}"


# -------------------------------
# Exercise & Workout Module
# -------------------------------

class Exercise(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('plyometrics', 'Plyometrics'),
        ('stretching', 'Stretching'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exerciseDbId = models.CharField(max_length=50, default='')
    name = models.CharField(max_length=255, default='')
    image_url = models.TextField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES, null=True, blank=True)
    met_value = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    
    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.name


class Muscle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'muscles'

    def __str__(self):
        return self.name


class ExerciseMuscle(models.Model):
    MUSCLE_TYPE_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('stabilizer', 'Stabilizer'),
    ]
    
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE)
    muscle_type = models.CharField(max_length=20, choices=MUSCLE_TYPE_CHOICES, default='primary')
    
    class Meta:
        db_table = 'exercise_muscles'
        unique_together = ('exercise', 'muscle')

    def __str__(self):
        return f"{self.exercise.name} - {self.muscle.name} ({self.muscle_type})"


class Equipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'equipments'

    def __str__(self):
        return self.name


class ExerciseEquipment(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'exercise_equipments'
        unique_together = ('exercise', 'equipment')

    def __str__(self):
        return f"{self.exercise.name} - {self.equipment.name}"


class BodyPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'body_parts'

    def __str__(self):
        return self.name


class ExerciseBodyPart(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'exercise_body_parts'
        unique_together = ('exercise', 'body_part')

    def __str__(self):
        return f"{self.exercise.name} - {self.body_part.name}"


class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keyword = models.TextField(default='')
    
    class Meta:
        db_table = 'keywords'

    def __str__(self):
        return self.keyword


class ExerciseKeyword(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'exercise_keywords'
        unique_together = ('exercise', 'keyword')

    def __str__(self):
        return f"{self.exercise.name} - {self.keyword.keyword}"


class RelatedExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='main_exercise')
    related_exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='related_to')
    
    class Meta:
        db_table = 'related_exercises'
        unique_together = ('exercise', 'related_exercise')

    def __str__(self):
        return f"{self.exercise.name} related to {self.related_exercise.name}"


class WorkoutPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        db_table = 'workout_plans'

    def __str__(self):
        return self.name


class PlanDay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='plan_days')
    day_number = models.IntegerField(default=1)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'plan_days'
        unique_together = ('plan', 'day_number')

    def __str__(self):
        return f"{self.plan.name} - Day {self.day_number}"


class PlanExercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_day = models.ForeignKey(PlanDay, on_delete=models.CASCADE, related_name='plan_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=1)
    sets = models.IntegerField(default=1)
    reps = models.CharField(max_length=50, default='1')  # Allows flexible formats like "8-12", "AMRAP", "30s"
    rest_period_seconds = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'plan_exercises'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.plan_day} - {self.exercise.name}"


class WorkoutLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date_performed = models.DateTimeField(auto_now_add=True)
    sets_performed = models.IntegerField(default=1)
    reps_performed = models.IntegerField(default=1)
    duration_minutes = models.IntegerField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    perceived_effort = models.IntegerField(null=True, blank=True)  # RPE scale 1-10
    
    class Meta:
        db_table = 'workout_log'

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} on {self.date_performed.date()}"


# -------------------------------
# Nutrition & Meal Planning Module
# -------------------------------

class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    serving_size_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    calories = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    protein_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    carbohydrates_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    fat_g = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'foods'

    def __str__(self):
        return self.name


class NutritionLog(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date_eaten = models.DateTimeField()
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # Multiplier of serving size
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES, null=True, blank=True)
    
    class Meta:
        db_table = 'nutrition_log'

    def __str__(self):
        return f"{self.user.username} - {self.food.name} on {self.date_eaten.date()}"


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)  # Cuisine origin
    instructions = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    youtube_url = models.TextField(null=True, blank=True)
    source_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'recipes'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'ingredients'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.CharField(max_length=255, default='')  # e.g., "1 cup", "200g", "2 tbsp"
    
    class Meta:
        db_table = 'recipe_ingredients'
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.recipe.name} - {self.measure} {self.ingredient.name}"


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.tag


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'recipe_tags'
        unique_together = ('recipe', 'tag')

    def __str__(self):
        return f"{self.recipe.name} - {self.tag.tag}"


class MealPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(null=True, blank=True)
    
    # Store complete AI-generated meal plan data as JSON
    meal_plan_data = models.JSONField(default=dict, help_text="Complete meal plan with days, meals, recipes, ingredients, and nutritional data")
    
    # Metadata fields for easy filtering and searching
    daily_calorie_target = models.IntegerField(null=True, blank=True)
    days_count = models.IntegerField(null=True, blank=True)
    dietary_preferences = models.JSONField(default=list, help_text="List of dietary preferences")
    goal = models.CharField(max_length=100, blank=True, help_text="User's fitness/nutrition goal")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        db_table = 'meal_plans'

    def __str__(self):
        return self.name