"""
Test cases for recent workouts functionality
Tests the ability to retrieve recent workout history and add exercises from it
"""

from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from api.models import User, WorkoutLog
from rest_framework import status
import json


class RecentWorkoutsTestCase(TestCase):
    """Test cases for recent workouts API endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash='test_hash'
        )
        
        # Create session for authenticated requests
        session = self.client.session
        session['user_id'] = str(self.user.id)
        session['username'] = self.user.username
        session.save()
        
        # Create workout logs for different dates
        now = timezone.now()
        
        # Today's workout
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Push-ups',
            date_performed=now,
            sets_performed=3,
            reps_performed=10
        )
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Squats',
            date_performed=now,
            sets_performed=3,
            reps_performed=12
        )
        
        # Yesterday's workout
        yesterday = now - timedelta(days=1)
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Bench Press',
            date_performed=yesterday,
            sets_performed=4,
            reps_performed=8
        )
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Deadlift',
            date_performed=yesterday,
            sets_performed=3,
            reps_performed=5
        )
        
        # Workout from 5 days ago
        five_days_ago = now - timedelta(days=5)
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Pull-ups',
            date_performed=five_days_ago,
            sets_performed=3,
            reps_performed=8
        )
        
        # Workout from 35 days ago (should be excluded by default)
        old_workout = now - timedelta(days=35)
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Old Exercise',
            date_performed=old_workout,
            sets_performed=3,
            reps_performed=10
        )

    def test_get_recent_workouts_requires_authentication(self):
        """Test that recent workouts endpoint requires authentication"""
        unauthenticated_client = Client()
        response = unauthenticated_client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recent_workouts_returns_grouped_sessions(self):
        """Test that recent workouts are grouped by date"""
        response = self.client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)
        self.assertIn('recent_workouts', data)
        
        # Check that workouts are grouped by date
        workouts = data['recent_workouts']
        self.assertGreaterEqual(len(workouts), 2)  # At least today and yesterday
        
        # Verify structure
        for workout in workouts:
            self.assertIn('date', workout)
            self.assertIn('timestamp', workout)
            self.assertIn('exercise_count', workout)
            self.assertIn('exercises', workout)
            self.assertIsInstance(workout['exercises'], list)
            self.assertGreater(len(workout['exercises']), 0)

    def test_recent_workouts_excludes_old_workouts(self):
        """Test that workouts older than the default 30 days are excluded"""
        response = self.client.get('/api/workout-logs/recent-workouts/?days=30')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        workouts = data['recent_workouts']
        
        # Verify old workout is not included
        for workout in workouts:
            for exercise in workout['exercises']:
                self.assertNotEqual(exercise['exercise_name'], 'Old Exercise')

    def test_recent_workouts_respects_limit_parameter(self):
        """Test that limit parameter limits the number of sessions returned"""
        response = self.client.get('/api/workout-logs/recent-workouts/?limit=2')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertLessEqual(data['count'], 2)
        self.assertLessEqual(len(data['recent_workouts']), 2)

    def test_recent_workouts_removes_duplicate_exercises(self):
        """Test that duplicate exercises within the same session are removed"""
        now = timezone.now()
        
        # Add multiple logs for the same exercise on the same date
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Push-ups',
            date_performed=now,
            sets_performed=3,
            reps_performed=10
        )
        WorkoutLog.objects.create(
            user=self.user,
            exercise_name='Push-ups',
            date_performed=now,
            sets_performed=4,
            reps_performed=12
        )
        
        response = self.client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Find today's workout
        today_workout = None
        for workout in data['recent_workouts']:
            if workout['date'] == now.date().isoformat():
                today_workout = workout
                break
        
        if today_workout:
            # Count unique exercises
            exercise_names = [ex['exercise_name'] for ex in today_workout['exercises']]
            unique_exercises = set(exercise_names)
            # Should have unique exercises (each exercise name should appear only once)
            self.assertEqual(len(exercise_names), len(unique_exercises))

    def test_recent_workouts_includes_exercise_details(self):
        """Test that exercise details are included in the response"""
        response = self.client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        workouts = data['recent_workouts']
        
        # Verify exercise details
        for workout in workouts:
            for exercise in workout['exercises']:
                self.assertIn('exercise_name', exercise)
                self.assertIn('sets_performed', exercise)
                self.assertIn('reps_performed', exercise)
                self.assertIsNotNone(exercise['exercise_name'])

    def test_recent_workouts_only_returns_user_workouts(self):
        """Test that users can only see their own recent workouts"""
        # Create another user
        other_user = User.objects.create(
            username='otheruser',
            email='other@example.com',
            password_hash='test_hash'
        )
        
        # Create workout for other user
        now = timezone.now()
        WorkoutLog.objects.create(
            user=other_user,
            exercise_name='Other Exercise',
            date_performed=now,
            sets_performed=3,
            reps_performed=10
        )
        
        # Request as original user
        response = self.client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        workouts = data['recent_workouts']
        
        # Verify other user's workout is not included
        for workout in workouts:
            for exercise in workout['exercises']:
                self.assertNotEqual(exercise['exercise_name'], 'Other Exercise')

    def test_recent_workouts_handles_no_workouts(self):
        """Test that endpoint handles case when user has no recent workouts"""
        # Create user with no workouts
        new_user = User.objects.create(
            username='newuser',
            email='new@example.com',
            password_hash='test_hash'
        )
        
        # Create new client with new user's session
        new_client = Client()
        session = new_client.session
        session['user_id'] = str(new_user.id)
        session['username'] = new_user.username
        session.save()
        
        response = new_client.get('/api/workout-logs/recent-workouts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['recent_workouts']), 0)

