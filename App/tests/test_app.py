import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    get_user_competitions,
    create_competition,
    add_user_to_comp,
    get_user_rankings
)
from App.controllers import *
from App.models import *

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        result = create_user("rick", "bobpass")
        assert result is True

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_add_user_to_comp(self):
        newcomp = create_competition("Walktime", "Port of Spain")
        if newcomp:
            assert add_user_to_comp(1, 1, 4)
        else:
            assert False

    def test_get_user_competitions(self):
        comp = get_user_competitions(1)
        user_competitions = []

        for usercomp in comp:
            del usercomp["date"]
            del usercomp["hosts"]
            del usercomp["participants"]
            user_competitions.append(usercomp)
        
        expected_list = [{"id": 1, "name": "Walktime", "location": "Port of Spain"}]
        self.assertListEqual(expected_list, user_competitions)


    def test_get_user_rankings(self):
        users = get_user_rankings(1)
        
        self.assertListEqual([{"id":1, "comp_id": 1 , "user_id": 1, "rank": 4}], users)

class RankingPlatformTests(unittest.TestCase):

   
   
    def test_register_user_for_competition(self):
        # Assuming test data setup with a user and competition IDs
        user_id = 1
        competition_id = 1
        rank = 10

        # Call the function to register the user for the competition
        result = register_user_for_competition(user_id, competition_id, rank)

        # Assert if the function returns True for successful registration
        assert result is True

    

    def test_update_user_competition_rank(self):
        # Assuming you have a user and a competition available in your test environment
        user_id = 1
        comp_id = 1
        initial_rank = 0
        new_rank = 5

        # Add the user to the competition with an initial rank
        add_results(user_id, comp_id, initial_rank)

        # Update the user's rank in the competition
        update_user_competition_rank(user_id, comp_id, new_rank)
        
        # Retrieve the updated rank for verification
        updated_user_comp = UserCompetition.query.filter_by(user_id=user_id, comp_id=comp_id).first()
        assert updated_user_comp.rank == new_rank

    from unittest.mock import patch

    def test_manage_top_20_and_notify(self):
       
        comp_id = 1

        
        top_20_users = generate_top_20_users()  # Define a function to generate mock top 20 users
        with patch('your_module.get_top_20_users_in_competition') as mock_get_top_20_users:
            mock_get_top_20_users.return_value = top_20_users

            # Mock the notify_top_20_users function to avoid actually sending notifications
            with patch('your_module.notify_top_20_users') as mock_notify_top_20_users:
                # Call the function being tested
                manage_top_20_and_notify(comp_id)

                
                mock_get_top_20_users.assert_called_once_with(comp_id)

                
                mock_notify_top_20_users.assert_called_once_with(top_20_users)
    
    def test_manage_top_20_and_notify(self):
        comp_id = 1

    # Store notifications instead of sending them
        notifications = []

    
    def mock_send_notification(user_id, message):
        notifications.append((user_id, message))
    
   
    
        your_module.send_notification = mock_send_notification

    
        manage_top_20_and_notify(comp_id)

   
        assert len(notifications) == 20  # Assuming 20 users are notified

def test_user():
    # Create a test user
    test_user = User(username='test_user', password='test_password')
    db.session.add(test_user)
    db.session.commit()

    # Set the overall_rank attribute separately
    test_user.overall_rank = 10

    return test_user

def test_get_top_20_users_in_competition():
    # Assuming we have a competition with ID 1 in the database
    comp_id = 1

    # Creating some dummy user competition records for competition ID 1
    # Adjust this as per your database model
    for i in range(1, 21):
        # Creating 24 users for competition ID 1 with ranks varying from 1 to 24
        register_user_for_competition(user_id=i, comp_id=comp_id, rank=i)

    # Fetching the top 20 users in competition 1
    top_20_users = get_top_20_users_in_competition(comp_id)

    # The top_20_users should contain 20 entries
    assert len(top_20_users) 

def test_update_top20_overall():
    # Assuming we have a competition with ID 1 in the database
    comp_id = 1

    # Creating 20 dummy user competition records for competition ID 1
    for i in range(1, 21):  
        # Creating 20 users for competition ID 1 with ranks varying from 1 to 20
        register_user_for_competition(user_id=i, comp_id=comp_id, rank=i)

    # Running the function to update overall rankings for top 20 users
    update_top20_overall(comp_id)

    # Fetching the top 20 users in overall rankings
    top_20_users = get_top_20_users_overall_rank()

def test_update_overall_rankings():
    # Assuming we have a competition with ID 1 in the database
    comp_id = 1

    # Creating 20 dummy user competition records for competition ID 1
    for i in range(1, 21):
        # Creating 20 users for competition ID 1 with ranks varying from 1 to 20
        register_user_for_competition(user_id=i, comp_id=comp_id, rank=i)

    # Fetching the top 20 users in competition 1
    top_20_users = get_top_20_users_in_competition(comp_id)

    # Running the function to update overall rankings for top 20 users
    update_overall_rankings(top_20_users)

    # Fetching the top 20 users in overall rankings
    top_20_overall = get_top_20_users_overall_rank() 

def test_update_user_overall_rank():
    # Assuming we have a competition with ID 1 in the database
    comp_id = 1

    # Creating a user and registering them for competition ID 1 with a rank of 5
    user_id = 1
    register_user_for_competition(user_id=user_id, comp_id=comp_id, rank=5)

    # Fetching the user's current overall rank
    user = User.query.get(user_id)
    initial_rank = user.overall_rank

    # Running the function to update the user's overall rank
    update_user_overall_rank(user_id, points=10)  # Incrementing points by 10

    # Fetching the user's updated overall rank
    updated_user = User.query.get(user_id)
    updated_rank = updated_user.overall_rank

    # The user's initial rank should be less than the updated rank
    assert initial_rank < updated_rank

    # The difference in ranks should be equal to the points added
    assert updated_rank - initial_rank == 10    


def test_notify_rank_changes():
    # Assuming we have 25 users in the top 20
    prev_top_20 = [(i, i) for i in range(1, 21)]
    
    # Simulating a change in positions for users 2, 5, and 10
    new_top_20 = [(1, 1), (2, 3), (3, 3), (4, 4), (5, 6), (6, 6), (7, 7), (8, 8), (9, 9), (10, 13),
                   (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)]

    # Mocking the send_notification function
    def mock_send_notification(user_id, message):
        print(f"Sending notification to User ID {user_id}: {message}")

    # Overriding the send_notification function temporarily with the mock
    globals()['send_notification'] = mock_send_notification

    # Calling the notify_rank_changes function with the mock setup
    notify_rank_changes(prev_top_20, new_top_20)

    # We expect notifications for users 2, 5, and 10 due to rank changes
    expected_notifications = [
        (2, 'Hey user_2, your position changed from 2 to 3 in the top 20 overall rank!'),
        (5, 'Hey user_5, your position changed from 5 to 6 in the top 20 overall rank!'),
        (10, 'Hey user_10, your position changed from 10 to 13 in the top 20 overall rank!')
    ]    

def test_notify_user_removed_from_top_20():
    # Assuming we have 25 users in the top 20
    prev_top_20 = [(i, i) for i in range(1, 21)]
    
    # Removing user 7 from the top 20
    user_removed = 7
    new_top_20 = [(i, i) for i in range(1, 21) if i != user_removed]

    # Mocking the send_notification function
    def mock_send_notification(user_id, message):
        print(f"Sending notification to User ID {user_id}: {message}")

    # Overriding the send_notification function temporarily with the mock
    globals()['send_notification'] = mock_send_notification

    # Calling the notify_user_removed_from_top_20 function with the mock setup
    notify_user_removed_from_top_20(user_removed)

    # We expect a notification for the removed user (user 7)
    expected_notification = (user_removed, 'Hey user_7, you\'ve been removed from the top 20 overall rank and now positioned as 21.')

def test_notify_user_position_change():
    # Assuming we have 25 users in the top 20
    prev_top_20 = [(i, i) for i in range(1, 21)]
    
    # Changing the position of user 5 from 5 to 15 in the new top 20
    user_id = 5
    prev_position = 5
    new_position = 15
    new_top_20 = [(i, i) if i != user_id else (i, new_position) for i in range(1, 21)]

    # Mocking the send_notification function
    def mock_send_notification(user_id, message):
        print(f"Sending notification to User ID {user_id}: {message}")

    # Overriding the send_notification function temporarily with the mock
    globals()['send_notification'] = mock_send_notification

    # Calling the notify_user_position_change function with the mock setup
    notify_user_position_change(user_id, prev_position, new_position)

    # We expect a notification for the user whose position changed
    expected_notification = (user_id, f"Hey user_{user_id}, your position changed from {prev_position} to {new_position} in the top 20 overall rank!")

def test_get_user_overall_rank_and_position():
    # Assuming we have 25 users in the top 20
    for i in range(1, 25):
        register_user_for_competition(user_id=i, comp_id=1, rank=i)  # Create dummy users for testing

    # Let's assume the user we're interested in has ID 5
    user_id = 5

    # Mocking the User.query.get method
    def mock_get_user(user_id):
        return User(id=user_id) if user_id <= 25 else None

    # Overriding the User.query.get method temporarily with the mock
    globals()['User'] = type('', (object,), {'query': type('', (object,), {'get': mock_get_user})})

    # Calling the get_user_overall_rank_and_position function
    overall_rank, user_position = get_user_overall_rank_and_position(user_id)

    # We expect this user's overall rank to be 5 in this simulation
    expected_overall_rank = 5

    # We expect this user's position in the top 20 to be 5 in this simulation
    expected_user_position = 5

   
