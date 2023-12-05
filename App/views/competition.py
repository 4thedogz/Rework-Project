from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    # create_user,
    # jwt_authenticate, 
    # get_all_users,
    # get_all_users_json,
    jwt_required,
    create_competition,
    get_all_competitions_json,
    get_competition_by_id,
    add_results,
    get_user_rankings,
    add_user_to_comp,
    create_user, register_user_for_competition, update_user_competition_rank, manage_top_20_and_notify, update_top20_overall, notify_rank_changes, get_top_20_users_api
)


comp_views = Blueprint('comp_views', __name__, template_folder='../templates')


##return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitons():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200) 

##add new competition to the db
@comp_views.route('/competitions', methods=['POST'])
@jwt_required()
def add_new_comp():
    data = request.json
    response = create_competition(data['name'], data['location'])
    if response:
        return (jsonify({'message': f"competition created"}), 201)
    return (jsonify({'error': f"error creating competition"}),500)


@comp_views.route('/competitions/user', methods=['POST'])
@jwt_required()
def add_comp_user():
    data = request.json

    user_id = data.get('user_id')
    comp_id = data.get('comp_id')
    rank = data.get('rank')

    if user_id is None or comp_id is None or rank is None:
        return jsonify({'error': 'Missing required parameters'}), 400

    result = add_user_to_comp(user_id, comp_id, rank)

    if result:
        return jsonify({'message': 'User added to competition successfully'}), 201
    else:
        return jsonify({'error': 'Error adding user to competition. User may already be added to this competition.'}), 500

@comp_views.route('/competitions/<int:id>', methods=['GET'])
def get_competition(id):
    print(id)
    competition = get_competition_by_id(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404 
    return (jsonify(competition.toDict()),200)


@comp_views.route('/rankings/<int:id>', methods =['GET'])
def get_rankings(id):
    ranks = get_user_rankings(id)
    return (jsonify(ranks),200)
