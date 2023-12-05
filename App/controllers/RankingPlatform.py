from App.models import User, Competition, UserCompetition
from App.controllers import add_results
from App.database import db


   
def register_user_for_competition(user_id, comp_id, rank=0):
   rank = 0
   result = add_results(user_id,comp_id,rank)
   return result

def update_user_competition_rank(user_id, comp_id, rank):
    """
    Update a user's rank in a specific competition.
    Args:
    - user_id: ID of the user.
    - comp_id: ID of the competition.
    - rank: New rank to be updated for the user in the competition.
    """
    user_comp = UserCompetition.query.filter_by(user_id=user_id, comp_id=comp_id).first()
    if user_comp:
        user_comp.rank = rank
        db.session.commit()
       # manage_top_20_and_notify(comp_id)
        
def manage_top_20_and_notify(comp_id):
    """
    Manage top 20 placement in a competition and notify relevant users.
    """
    top_20_users = get_top_20_users_in_competition(comp_id)
    #update_overall_rankings(top_20_users)
    notify_top_20_users(top_20_users)

def get_top_20_users_in_competition(comp_id):
    """
    Get the top 20 users in a specific competition.
    """
    # Fetching top 20 users in a competition, ordered by rank (descending)
    top_20_users = UserCompetition.query.filter_by(comp_id=comp_id).order_by(UserCompetition.rank.desc()).limit(20).all()

    return top_20_users

def notify_top_20_users(top_20_users):
    """
    Notify top 20 users about their placement in the competition.
    """
    for user in top_20_users:
        # Send notification to each user about their placement in the competition
        send_notification(user.id, f"You've been placed in the top 20 of the competition!")

def update_top20_overall(comp_id):
    """
    Manage top 20 placement in a competition and notify relevant users.
    """
    top_20_users = get_top_20_users_in_competition(comp_id)
    update_overall_rankings(top_20_users)
    
def update_overall_rankings(top_20_users):
    """
    Update overall rankings for top 20 users based on their position in the competition.
    """
    for position, user in enumerate(top_20_users, start=1):
        points = 21 - position  # Assign points based on competition position
        update_user_overall_rank(user.id, points)

def update_user_overall_rank(user_id, points):
    """
    Update the overall rank of a user by adding competition rank points.
    """
    user = User.query.get(user_id)
    if user:
        user.overall_rank += points
        db.session.commit()

def get_top_20_users_overall_rank():
    """
    Get the top 20 users in the overall platform ranking.
    
    """
    # Query to fetch top 20 users based on overall rank
    top_20_users = User.query.order_by(User.overall_rank.desc()).limit(20).all()
    # Create a list of tuples with user_id and their position
    top_20_positions = [(user.id, index + 1) for index, user in enumerate(top_20_users)]
    return top_20_positions

def notify_rank_changes(prev_top_20, new_top_20):
    """
    Compare previous and new positions in the top 20 overall rank and notify users if their position changed.
    """
    prev_top_20_dict = dict(prev_top_20)
    new_top_20_dict = dict(new_top_20)

    # Check for users that were in the previous top 20 but not in the new top 20
    for user_id, prev_position in prev_top_20:
        new_position = new_top_20_dict.get(user_id)
        
        if new_position and new_position != prev_position:
            notify_user_position_change(user_id, prev_position, new_position)
            
    # Check for users that were in the previous top 20 but not in the new top 20
    for user_id, prev_position in prev_top_20:
        if user_id not in new_top_20_dict:
            notify_user_removed_from_top_20(user_id)

def notify_user_removed_from_top_20(user_id):
    """
    Notify the user about their removal from the top 20 overall rank.
    """
    user = User.query.get(user_id)
    if user:
        notification_message = f"Hey {user.username}, you've been removed from the top 20 overall rank and now positioned as 21."
        send_notification(user_id, notification_message)

def notify_user_position_change(user_id, prev_position, new_position):
    """
    Notify the user about their position change in the top 20 overall rank.
    """
    user = User.query.get(user_id)
    if user:
        notification_message = f"Hey {user.username}, your position changed from {prev_position} to {new_position} in the top 20 overall rank!"
       
        send_notification(user_id, notification_message)
        send_notification_touser(user_id, notification_message)
        
def send_notification(user_id, message):
   
   
    print(f"Sending notification to User ID {user_id}: {message}")
    

def get_user_overall_rank_and_position(user_id):
    user = User.query.get(user_id)
    if user:
        overall_rank = user.overall_rank
        top_20_users = User.query.order_by(User.overall_rank.desc()).limit(20).all()
        user_position = next((pos + 1 for pos, u in enumerate(top_20_users) if u.id == user_id), None)
        return overall_rank, user_position
    else:
        return None, None

def arrange_top_20_overall():
    """
    Arrange top 20 users from 1 to 20 based on overall ranking.
    """
    top_20_users = User.query.order_by(User.overall_rank.desc()).limit(20).all()
    for index, user in enumerate(top_20_users, start=1):
        user.overall_rank = index
    db.session.commit()


def print_top_20_users():
    """
    Print the top 20 users in order of their overall ranking.
    """
    top_20_users = User.query.order_by(User.overall_rank.desc()).limit(20).all()
    for rank, user in enumerate(top_20_users, start=1):
        print(f"{rank}. {user.username} - Overall Rank: {user.overall_rank}")

def get_top_20_users_api():
    """
    Get the top 20 users in order of their overall ranking.
    Returns:
    - List containing tuples of user details (username, overall rank).
    """
    top_20_users = User.query.order_by(User.overall_rank.desc()).limit(20).all()
    user_details = [(user.username, user.overall_rank) for user in top_20_users]
    return user_details

def send_notification_touser(user_id, message):
    user = User.query.get(user_id)
    if user:
        # Append the new message to the existing messages
        if user.message:
            user.message += f"\n{message}"
        else:
            user.message = message
        
        db.session.commit()

def get_user_overall_rank(user_id):
    user = User.query.get(user_id)
    if user:
        return user.overall_rank
    return None