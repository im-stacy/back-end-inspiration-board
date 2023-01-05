from os import abort
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# helper function
def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model



################################################################
###################### BOARD ROUTES ############################

#create a post route
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_dict_boards(), 201)

# create a get one board route 
@boards_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return jsonify(board.to_dict_boards(), 200)

# create get all route
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards_response = []
    boards = Board.query.all()
    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })

    return jsonify(boards_response)


# create a post route to assign card to board

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def assign_card_to_board(board_id):

    board = validate_model(Board, board_id) 
    request_body = request.get_json()

    board.cards = [] 

    for card_id in request_body['card_ids']:
        card = validate_model(Card, card_id)
        board.cards.append(card)
        db.session.commit() 
    
    return make_response(jsonify({"id":board.board_id,"card_ids":request_body["card_ids"]})),200 

# create a get route to see all card of a board

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def gets_cards_of_one_board(board_id):

    board = validate_model(Board, board_id)
    cards_of_board =[]  
    
    for card in board.cards:
        cards_of_board.append(
            {
                "id": card.card_id,
                "board_id": card.board_id,
                "title": card.title,
                "description": card.description,
                "is_complete": bool(card.completed_at)
            }
            ) 
    return make_response(jsonify({"id":board.board_id,"title":board.title,"cards":cards_of_board})),200 

################################################################
####################### CARD ROUTES ############################

# create a post route for card
@cards_bp.route("", methods = ["POST"])
def create_card():
    request_body = request.get_json()

    try:
        new_card = Card.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict_cards(), 201)



# create a get all cards route 

@cards_bp.route("", methods = ["GET"])
def get_all_cards():
    cards_response = []
    cards = Card.query.all()
    for card in cards:
        cards_response.append({
            "id": card.card_id,
            "title": card.title,
            "owner": card.owner
        })

    return jsonify(cards_response)



# create a route to delete a single  card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card,card_id)

    db.session.delete(card)
    db.session.commit()
    deleted_card_dict = {"details":f"Card {card.card_id} \"{card.title}\" successfully deleted"}

    return make_response(jsonify(deleted_card_dict), 200)







# create a route to delete all boards and cards 


