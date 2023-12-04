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

