import click, pytest, sys
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (register_user_for_competition,add_results, get_user_rankings, get_competition_users, findCompUser, get_user_competitions, add_user_to_comp, create_competition, get_all_competitions, get_all_competitions_json, create_user, get_all_users_json, get_all_users )
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_user('notbob', 'bobpass')
    create_user('sparky', 'bobpass')
    create_user('pierce', 'bobpass')
    create_user('vedesh', 'bobpass')
    create_user('parbs', 'bobpass')
    create_user('brian', 'bobpass')
    create_user('andy', 'bobpass')
    create_user('keegan', 'bobpass')
    create_user('jeff', 'bobpass')
    create_user('whocares', 'bobpass')
    create_user('anotherone', 'bobpass')
    create_user('drake', 'bobpass')
    create_user('uzi', 'bobpass')
    create_user('carti', 'bobpass')
    create_user('offset', 'bobpass')
    create_user('quavo', 'bobpass')
    create_user('blueface', 'bobpass')
    create_user('random', 'bobpass')
    create_user('salik', 'bobpass')
    create_user('outsider', 'bobpass')

    create_competition('theboys','sando')

    register_user_for_competition(1,1,1)
    register_user_for_competition(2,1,1)
    register_user_for_competition(3,1,1)
    register_user_for_competition(4,1,1)
    register_user_for_competition(5,1,1)
    register_user_for_competition(6,1,1)
    register_user_for_competition(7,1,1)
    register_user_for_competition(8,1,1)
    register_user_for_competition(9,1,1)
    register_user_for_competition(10,1,1)
    register_user_for_competition(11,1,1)
    register_user_for_competition(12,1,1)
    register_user_for_competition(13,1,1)
    register_user_for_competition(14,1,1)
    register_user_for_competition(15,1,1)
    register_user_for_competition(16,1,1)
    register_user_for_competition(17,1,1)
    register_user_for_competition(18,1,1)
    register_user_for_competition(19,1,1)
    register_user_for_competition(20,1,1)
    register_user_for_competition(21,1,1)

    update_user_competition_rank(1,1,40)
    update_user_competition_rank(2,1,43)
    update_user_competition_rank(3,1,44)
    update_user_competition_rank(4,1,45)
    update_user_competition_rank(5,1,20)
    update_user_competition_rank(6,1,54)
    update_user_competition_rank(7,1,30)
    update_user_competition_rank(8,1,29)
    update_user_competition_rank(9,1,44)
    update_user_competition_rank(10,1,49)
    update_user_competition_rank(11,1,51)
    update_user_competition_rank(12,1,62)
    update_user_competition_rank(13,1,31)
    update_user_competition_rank(14,1,19)
    update_user_competition_rank(15,1,14)
    update_user_competition_rank(16,1,39)
    update_user_competition_rank(17,1,45)
    update_user_competition_rank(18,1,50)
    update_user_competition_rank(19,1,21)
    update_user_competition_rank(20,1,22)
    update_user_competition_rank(21,1,23)

    manage_top_20_and_notify(1)
    top_20_positions = get_top_20_users_overall_rank()
    update_top20_overall(1)
    top_20_positions2 = get_top_20_users_overall_rank()
    notify_rank_changes(top_20_positions,top_20_positions2)
    arrange_top_20_overall()
    print_top_20_users()
    
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))





@test.command("competition", help = 'Testing Competition commands')
@click.argument("type", default="all")
def competition_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CompUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CompIntegrationTests"]))
    else:
        print("deafult input, no test ran")




app.cli.add_command(test)


'''
Competition commands
'''

comps = AppGroup('comp', help = 'commands for competition')   

@comps.command("add", help = 'add new competition')
@click.argument("name", default = "Coding Comp")
@click.argument("location", default = "Port of Spain")
def add_comp(name, location):
    response = create_competition(name, location)
    if response:
        print("Competition Created Successfully")
    else:
        print("error adding comp")





@comps.command("get", help = "list all competitions")
def get_comps():
    print(get_all_competitions())

@comps.command("get_json", help = "list all competitions")
def get_comps():
    print(get_all_competitions_json())


@comps.command("add_user")
@click.argument("user_id")
@click.argument("comp_id")
@click.argument("rank")
def add_to_comp(user_id, comp_id, rank):
    add_user_to_comp(user_id, comp_id, rank)
    print("Done!")


@comps.command("getUserComps")
@click.argument("user_id")
def getUserCompetitions(user_id):
    competitions = get_user_competitions(user_id)
    print("these are the competitions")
    # print(competitions)

@comps.command("findcompuser")
@click.argument("user_id")
@click.argument("comp_id")
def find_comp_user(user_id, comp_id):
    findCompUser(user_id, comp_id)

@comps.command("getCompUsers")
@click.argument("comp_id")
def get_comp_users(comp_id):
    get_competition_users(comp_id)




app.cli.add_command(comps)

rank_cli = AppGroup('rank', help='RankingPlatform commands')

@rank_cli.command("register_user_for_competition", help="Register user for a competition")
@click.argument("user_id")
@click.argument("comp_id")
@click.argument("rank", default=0)
def register_user_for_competition_command(user_id, comp_id, rank=0):
    register_user_for_competition(user_id, comp_id, )
    print(f"User {user_id} registered for competition {comp_id} with rank 0")

# Add other commands for your RankingPlatform methods similarly...
@rank_cli.command("update_user_competition_rank", help="Update user's rank in a competition")
@click.argument("user_id")
@click.argument("comp_id")
@click.argument("rank")
def update_user_competition_rank_command(user_id, comp_id, rank):
    update_user_competition_rank(user_id, comp_id, rank)
    print(f"Updated user {user_id} rank for competition {comp_id} with {rank} points")

@rank_cli.command("manage_top_20_and_notify", help="Manage top 20 placement in a competition")
@click.argument("comp_id")
def manage_top_20_and_notify_command(comp_id):
    manage_top_20_and_notify(comp_id)
    print(f"Managed top 20 and notified users for competition {comp_id}")

@rank_cli.command("update_top20_overall", help="Update top 20 overall rank")
@click.argument("comp_id")
def update_top20_overall_command(comp_id):
    update_top20_overall(comp_id)
    print(f"Updated top 20 overall rank for competition {comp_id}")

@rank_cli.command("update_and_notify_top_20", help="Update top 20 and notify rank changes")
@click.argument("comp_id")
def update_and_notify_top_20_command(comp_id):
    top_20_positions = get_top_20_users_overall_rank()
    update_top20_overall(comp_id)
    updated_top_20_positions = get_top_20_users_overall_rank()
    notify_rank_changes(top_20_positions, updated_top_20_positions)
    arrange_top_20_overall()
    print("Updated top 20 and notified rank changes")
    
@rank_cli.command("get_user_overall_rank_and_position", help="Gets the user overall rank and position")
@click.argument("user_id")
def get_user_overall_rank_and_position_command(user_id):
    """Get user's overall rank and position"""
    overall_rank, user_position = get_user_overall_rank_and_position(user_id)
    
    if overall_rank is None:
        print(f"User {user_id} does not exist.")
    else:
        print(f"User {user_id} has an overall rank of {overall_rank} and is positioned at {overall_rank}.")

app.cli.add_command(rank_cli)