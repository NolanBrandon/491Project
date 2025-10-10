# Comprehensive Health & Fitness Application Database Schema

This document provides a highly detailed, field-by-field explanation of the database schema for a comprehensive health and fitness application. The schema is designed to manage user data, exercise routines, workout logs, and nutritional information, including meal plans and recipes. The schema is logically divided into three primary modules for clarity.

## 🏛️ 1. User Management & Core Tracking Module

This group of tables stores foundational information about the users, their physical metrics over time, and their high-level fitness goals. It forms the core of the user profile.

---

### **`users` table**

This is the central table for all user account information. Every user who signs up will have a single record in this table.

* **Purpose**: To store the primary, non-volatile details for each registered user.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key**. A unique identifier for each user, specified as a Universally Unique Identifier (UUID) to ensure global uniqueness. It is marked as `NN` (Not Null).
* `username` **(varchar(50), NN)**: The user's public and unique username, limited to 50 characters. It is a required field.
* `email` **(varchar(255), NN)**: The user's unique email address, used for login, password resets, and communication. It is a required field.
* `password_hash` **(varchar(255), NN)**: The user's password, stored securely as a cryptographic hash (e.g., bcrypt or Argon2). The raw password is never stored.
* `gender` **(varchar(50))**: The user's self-identified gender. This field is optional.
* `date_of_birth` **(date)**: The user's date of birth. This is used to calculate age and is optional.
* `last_login_date` **(date)**: The date the user last logged in. This field is useful for tracking user engagement and implementing features like login streaks.
* `login_streak` **(int)**: A counter for consecutive days the user has logged in, which can be used for gamification.
* `created_at` **(timestamptz)**: A timestamp with time zone information that marks the exact moment the user account was created.

#### **Relationships**

* **One-to-Many**: A single record in the `users` table can be associated with many records in the following tables, forming the basis of user-owned data:
    * `user_metrics` (via `user_metrics.user_id`)
    * `goals` (via `goals.user_id`)
    * `workout_log` (via `workout_log.user_id`)
    * `nutrition_log` (via `nutrition_log.user_id`)
    * `workout_plans` (via `workout_plans.user_id`)
    * `meal_plans` (via `meal_plans.user_id`)

---

### **`user_metrics` table**

This table logs a user's physical stats over time, creating a historical record of their physical changes.

* **Purpose**: To track changes in a user's weight, height, and general activity level for progress monitoring.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for this specific metric entry.
* `user_id` **(FK, uuid, NN)**: A **Foreign Key** that references `users.id`. This creates a direct link, ensuring every metric entry belongs to a valid user.
* `date_recorded` **(date, NN)**: The specific date on which these measurements were taken.
* `weight_kg` **(decimal(5,2))**: The user's weight in kilograms, allowing for up to 999.99 kg.
* `height_cm` **(decimal(5,2))**: The user's height in centimeters, allowing for up to 999.99 cm.
* `activity_level` **(varchar(50))**: A descriptor of the user's general activity level (e.g., 'Sedentary', 'Lightly Active', 'Very Active'), which can be used in calorie expenditure calculations.

#### **Relationships**

* **Many-to-One**: Many `user_metrics` entries can belong to a single user (`users`). This allows for a complete history of a user's metrics to be stored and visualized.

---

### **`goals` table**

This table stores the specific, measurable, and time-bound goals set by a user.

* **Purpose**: To define and track user fitness goals, providing clear targets for the user to work towards.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the goal.
* `user_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `users.id`, linking the goal to its owner.
* `goal_type` **(varchar(50), NN)**: The category of the goal, such as 'weight_loss', 'muscle_gain', or 'maintenance'.
* `target_weight_kg` **(decimal(5,2))**: The user's desired target weight in kilograms.
* `start_date` **(date)**: The date the user officially initiated the goal.
* `end_date` **(date)**: The target completion date for the goal, making it time-bound.
* `is_active` **(boolean)**: A flag (true/false) to indicate if this is the user's currently active goal. This prevents conflicts if a user has multiple goals.

#### **Relationships**

* **Many-to-One**: Many `goals` can be set by a single user (`users`), allowing them to track past, present, and future goals.

---

## 💪 2. Exercise & Workout Module

This module contains a comprehensive library of exercises, tools for building structured workout plans, and logs for tracking user activity.

---

### **`exercises` table**

This is the master catalog of all exercises available within the application. It is a read-only library for most users.

* **Purpose**: To act as a central, detailed library of exercises that can be referenced by workout plans and logs.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key**. A unique identifier for the exercise.
* `exerciseDbId` **(varchar(50), NN)**: An identifier that may link to an external, third-party exercise database for data synchronization or enrichment.
* `name` **(varchar(255), NN)**: The common name of the exercise (e.g., "Barbell Bench Press", "Treadmill Running").
* `image_url` **(text)**: A URL pointing to a static image demonstrating the exercise form.
* `video_url` **(text)**: A URL pointing to a video (e.g., on YouTube or a hosted service) demonstrating the exercise.
* `overview` **(text)**: A brief, high-level description of the exercise and its benefits.
* `instructions` **(text)**: Detailed, step-by-step instructions on how to perform the exercise safely and effectively.
* `exercise_type` **(enum)**: The category of the exercise, likely from a predefined list such as 'strength', 'cardio', 'plyometrics', 'stretching'.
* `met_value` **(decimal(4,2), NN)**: The Metabolic Equivalent of Task value. This is a scientific measure used to estimate the energy expenditure (calories burned) of an activity.

#### **Relationships**

* **One-to-Many**: A single record in `exercises` can be referenced by many records in `workout_log` and `plan_exercises`.
* **Many-to-Many**: This table has several many-to-many relationships to provide rich, queryable details:
    * With `equipments` via the `exercise_equipments` join table.
    * With `muscles` via the `exercise_muscles` join table.
    * With `body_parts` via the `exercise_body_parts` join table.
    * With `keywords` via the `exercise_keywords` join table.
    * It also has a self-referencing many-to-many relationship with itself via the `related_exercises` table, allowing for suggestions of similar or alternative exercises.

---

### **Lookup & Join Tables for `exercises`**

These tables add descriptive, many-to-many layers of information to the `exercises` table, making it highly searchable and filterable.

* **`muscles`**: A simple lookup table listing all possible muscles.
    * `id` (PK), `name` (varchar).
* **`exercise_muscles`** (Join Table): Links exercises to the muscles they target.
    * `exercise_id` (FK -> `exercises.id`): Points to the exercise.
    * `muscle_id` (FK -> `muscles.id`): Points to the muscle.
    * `muscle_type` (varchar): Describes the role of the muscle (e.g., 'primary', 'secondary', 'stabilizer').
* **`equipments`**: A lookup table for all types of gym equipment.
    * `id` (PK), `name` (varchar, e.g., 'Barbell', 'Dumbbell', 'Kettlebell').
* **`exercise_equipments`** (Join Table): Links exercises to the equipment they require.
    * `exercise_id` (FK -> `exercises.id`), `equipment_id` (FK -> `equipments.id`).
* **`body_parts`**: A lookup table for general body parts.
    * `id` (PK), `name` (varchar, e.g., 'Chest', 'Back', 'Legs').
* **`exercise_body_parts`** (Join Table): Links exercises to the body parts they primarily target.
    * `exercise_id` (FK -> `exercises.id`), `body_part_id` (FK -> `body_parts.id`).
* **`keywords`**: A lookup table for searchable keywords or tags.
    * `id` (PK), `keyword` (text, e.g., 'HIIT', 'powerlifting', 'home_workout').
* **`exercise_keywords`** (Join Table): Links exercises to relevant keywords for better search functionality.
    * `exercise_id` (FK -> `exercises.id`), `keyword_id` (FK -> `keywords.id`).
* **`related_exercises`** (Join Table): A self-referencing join table that links an exercise to other related exercises.
    * `exercise_id` (FK -> `exercises.id`): The base exercise.
    * `related_exercise_id` (FK -> `exercises.id`): The exercise that is related to it.

---

### **`workout_plans` table**

Stores a collection of exercises organized into a structured routine. These can be created by users or provided by the system.

* **Purpose**: To define a structured workout plan that a user can follow over a period of time.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the workout plan.
* `user_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `users.id`, identifying the creator of the plan. This could be nullable if the system provides default plans.
* `name` **(varchar(255), NN)**: The name of the workout plan (e.g., "Beginner Full Body Strength").
* `description` **(text)**: A detailed description of the plan's goals, intended audience, and structure.
* `created_at` **(timestamptz)**: Timestamp of when the plan was created.

#### **Relationships**

* **Many-to-One**: Many `workout_plans` can be created by a single user (`users`).
* **One-to-Many**: One `workout_plans` record is the parent to many `plan_days` records, which represent the individual days of the routine.

---

### **`plan_days` table**

Represents a single day's workout session within a larger `workout_plan`.

* **Purpose**: To break a multi-day workout plan into distinct, individual daily routines.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for this specific day within a plan.
* `plan_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `workout_plans.id`, linking this day to its parent plan.
* `day_number` **(int, NN)**: The sequence of the day within the plan (e.g., Day 1, Day 2, Day 3).
* `name` **(varchar(100))**: An optional, descriptive name for the day's workout (e.g., "Push Day", "Leg Day", "Active Recovery").

#### **Relationships**

* **Many-to-One**: Many `plan_days` records belong to one `workout_plans` record.
* **One-to-Many**: One `plan_days` record is the parent to many `plan_exercises` records, which detail the actual exercises for that day.

---

### **`plan_exercises` table**

This table details a specific exercise to be performed on a specific `plan_day`, including the prescribed volume.

* **Purpose**: To list the exercises for a given day in a plan and specify the target sets, repetitions, and rest times.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for this specific exercise entry within a plan day.
* `plan_day_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `plan_days.id`.
* `exercise_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `exercises.id`.
* `display_order` **(int, NN)**: The order in which this exercise should appear in the user interface for that day (e.g., 1st, 2nd, 3rd).
* `sets` **(int, NN)**: The target number of sets to be performed.
* `reps` **(varchar(50))**: The target number of repetitions. This is a `varchar` to allow for flexible formats like "8-12", "AMRAP" (As Many Reps As Possible), or "30s".
* `rest_period_seconds` **(int)**: The recommended rest time in seconds between each set.

#### **Relationships**

* **Many-to-One**: Many `plan_exercises` entries belong to one `plan_days` entry.
* **Many-to-One**: Many `plan_exercises` entries can reference the same exercise from the master `exercises` table.

---

### **`workout_log` table**

This table records a user's actual performance for a completed exercise, creating a historical workout journal.

* **Purpose**: To create a historical log of every workout a user completes, which is essential for tracking progress and performance.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the log entry.
* `user_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `users.id`, linking the log to the user who performed the workout.
* `exercise_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `exercises.id`, identifying the specific exercise that was performed.
* `sets_performed` **(int, NN)**: The actual number of sets the user completed.
* `reps_performed` **(int, NN)**: The total number of repetitions the user completed across all sets.
* `duration_minutes` **(int)**: The duration of the exercise in minutes (especially useful for cardio or timed exercises).
* `calories_burned` **(int)**: An estimation of the calories burned during the exercise, likely calculated using the `met_value` from the `exercises` table and user metrics.
* `perceived_effort` **(int)**: A user-reported score for the difficulty of the exercise, typically on a scale of 1-10 (Rate of Perceived Exertion or RPE).

#### **Relationships**

* **Many-to-One**: Many `workout_log` entries belong to one `users` record.
* **Many-to-One**: Many `workout_log` entries can reference the same `exercises` record.

---

## 🥗 3. Nutrition & Meal Planning Module

This module manages all data related to food, recipes, meal plans, and nutritional logs, allowing for comprehensive diet tracking.

---

### **`foods` table**

A master catalog of individual food items and their core nutritional information.

* **Purpose**: To serve as a searchable database of generic foods that users can log as part of their diet.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the food item.
* `name` **(varchar(255), NN)**: The common name of the food (e.g., "Apple", "Chicken Breast").
* `serving_size_g` **(decimal(7,2))**: The standard serving size in grams for the given nutritional data.
* `calories` **(decimal(7,2))**: The number of calories per serving.
* `protein_g` **(decimal(7,2))**: Grams of protein per serving.
* `carbohydrates_g` **(decimal(7,2))**: Grams of carbohydrates per serving.
* `fat_g` **(decimal(7,2))**: Grams of fat per serving.

#### **Relationships**

* **One-to-Many**: One `foods` item can be included in many `nutrition_log` entries and many `meal_plan_entries`.

---

### **`nutrition_log` table**

Records each instance of a food item that a user has consumed.

* **Purpose**: To track a user's daily food intake and calculate total calories and macronutrients consumed.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the log entry.
* `user_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `users.id`.
* `food_id` **(FK, uuid, NN)**: A **Foreign Key** referencing `foods.id`.
* `date_eaten` **(timestamptz, NN)**: The precise date and time the food was consumed.
* `quantity` **(decimal(5,2), NN)**: The quantity of the serving size consumed. For example, if the serving size is 100g and the user ate 150g, this value would be 1.5.
* `meal_type` **(varchar(50))**: The meal this food was part of (e.g., 'Breakfast', 'Lunch', 'Dinner', 'Snack').

#### **Relationships**

* **Many-to-One**: Many `nutrition_log` entries belong to one `users` record.
* **Many-to-One**: Many `nutrition_log` entries can reference one `foods` item.

---

### **`recipes` table**

Stores detailed recipes that are composed of multiple ingredients from the `ingredients` table.

* **Purpose**: To provide users with structured recipes they can cook and log as a single meal.

#### **Fields**

* `id` **(PK, uuid, NN)**: The **Primary Key** for the recipe.
* `mealDbId` **(varchar(50), NN)**: An identifier that may link to an external recipe database (like TheMealDB).
* `name` **(varchar(255), NN)**: The name of the recipe.
* `category` **(varchar(100))**: The recipe category (e.g., 'Dessert', 'Seafood', 'Vegetarian').
* `area` **(varchar(100))**: The cuisine's geographical origin (e.g., 'Italian', 'Mexican', 'Thai').
* `instructions` **(text)**: Step-by-step cooking instructions.
* `image_url` **(text)**: A URL to an image of the finished dish.
* `youtube_url` **(text)**: A URL to a video of the recipe being prepared.
* `source_url` **(text)**: A URL to the original source of the recipe online.

#### **Relationships**

* **One-to-Many**: One `recipes` record can be included in many `meal_plan_entries`.
* **Many-to-Many**: Has a many-to-many relationship with `ingredients` via the `recipe_ingredients` join table.
* **Many-to-Many**: Has a many-to-many relationship with `tags` via the `recipe_tags` join table.

---

### **`ingredients`, `recipe_ingredients`, `tags`, `recipe_tags`**

These tables add descriptive, many-to-many details to recipes.

* **`ingredients`**: A lookup table of all possible recipe ingredients.
    * `id` (PK), `name` (varchar).
* **`recipe_ingredients`** (Join Table): Links recipes to their constituent ingredients and specifies the amount.
    * `recipe_id` (FK -> `recipes.id`): Points to the recipe.
    * `ingredient_id` (FK -> `ingredients.id`): Points to the ingredient.
    * `measure` (varchar): The quantity and unit required (e.g., "1 cup", "200g", "2 tbsp").
* **`tags`**: A lookup table for descriptive tags (e.g., 'Vegan', 'High-Protein', 'Gluten-Free').
    * `id` (PK), `tag` (varchar).
* **`recipe_tags`** (Join Table): Links recipes to relevant tags for filtering and searching.
    * `recipe_id` (FK -> `recipes.id`), `tag_id` (FK -> `tags.id`).

---

### **`meal_plans`, `meal_plan_days`, `meal_plan_entries`**

This set of tables allows for the creation of structured meal plans, mirroring the structure of the workout plans.

* **`meal_plans`**: The top-level table for a meal plan.
    * `id` (PK, uuid, NN), `user_id` (FK -> `users.id`, NN), `name` (varchar, NN), `description` (text), `created_at` (timestamptz).
* **`meal_plan_days`**: Represents a single day's meals within a `meal_plan`.
    * `id` (PK, uuid, NN), `meal_plan_id` (FK -> `meal_plans.id`, NN), `day_number` (int, NN).
* **`meal_plan_entries`**: Assigns a specific food or recipe to a day and meal type within a plan.
    * `id` (PK, uuid, NN), `meal_plan_day_id` (FK -> `meal_plan_days.id`, NN), `food_id` (FK -> `foods.id`, nullable), `recipe_id` (FK -> `recipes.id`, nullable), `meal_type` (varchar, NN).
    * **Note**: The `food_id` and `recipe_id` fields are mutually exclusive and nullable. An entry in this table represents either a single food item *or* a full recipe for a given meal, but not both simultaneously.