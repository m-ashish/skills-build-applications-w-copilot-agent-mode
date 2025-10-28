from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (super heroes)
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team': 'marvel'},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team': 'marvel'},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team': 'dc'},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team': 'dc'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'marvel', 'members': ['tony@marvel.com', 'steve@marvel.com']},
            {'name': 'dc', 'members': ['bruce@dc.com', 'clark@dc.com']},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user_email': 'tony@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'steve@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'bruce@dc.com', 'activity': 'Swimming', 'duration': 25},
            {'user_email': 'clark@dc.com', 'activity': 'Flying', 'duration': 60},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'marvel', 'points': 75},
            {'team': 'dc', 'points': 85},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user_email': 'tony@marvel.com', 'workout': 'Chest Day', 'suggestion': 'Bench Press'},
            {'user_email': 'steve@marvel.com', 'workout': 'Leg Day', 'suggestion': 'Squats'},
            {'user_email': 'bruce@dc.com', 'workout': 'Cardio', 'suggestion': 'Treadmill'},
            {'user_email': 'clark@dc.com', 'workout': 'Full Body', 'suggestion': 'Super Sets'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
