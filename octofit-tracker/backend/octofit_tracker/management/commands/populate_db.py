from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'dc'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'marvel'},
        ]
        teams = [
            {'name': 'marvel', 'members': ['Iron Man', 'Captain America', 'Black Widow']},
            {'name': 'dc', 'members': ['Superman', 'Batman', 'Wonder Woman']},
        ]
        activities = [
            {'user': 'Superman', 'activity': 'Flight', 'duration': 60},
            {'user': 'Iron Man', 'activity': 'Training', 'duration': 45},
        ]
        leaderboard = [
            {'team': 'marvel', 'points': 120},
            {'team': 'dc', 'points': 110},
        ]
        workouts = [
            {'name': 'Pushups', 'suggested_for': 'marvel'},
            {'name': 'Squats', 'suggested_for': 'dc'},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
