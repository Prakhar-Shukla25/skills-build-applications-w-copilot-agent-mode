from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        marvel_team = {'name': 'Team Marvel', 'members': ['Iron Man', 'Captain America', 'Thor', 'Hulk', 'Black Widow']}
        dc_team = {'name': 'Team DC', 'members': ['Superman', 'Batman', 'Wonder Woman', 'Flash', 'Aquaman']}
        teams = [marvel_team, dc_team]
        db.teams.insert_many(teams)

        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'hulk@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'Team DC'},
            {'name': 'Flash', 'email': 'flash@dc.com', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'aquaman@dc.com', 'team': 'Team DC'},
        ]
        db.users.insert_many(users)

        activities = [
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Batman', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Swimming', 'duration': 60},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {'team': 'Team Marvel', 'points': 150},
            {'team': 'Team DC', 'points': 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {'name': 'Full Body Blast', 'suggested_for': 'Team Marvel'},
            {'name': 'Speed & Agility', 'suggested_for': 'Team DC'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
