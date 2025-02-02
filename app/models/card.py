from app import db
from flask import abort, make_response 


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    message = db.Column(db.String)
    likes = db.Column(db.Integer, default=0) 
    #delete_status = db.Column(db.String, nullable = True)
    board = db.relationship("Board", back_populates ="cards")
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)

    @classmethod
    def from_json(cls, req_body):
        return cls(
            message = req_body["message"],
            likes = req_body["likes"],
            #delete_status = req_body["delete_status"]
        )

    def to_dict_cards(self):
        return { "card":{
                "id":self.card_id,
                "message": self.message,
                "likes": self.likes
                #"delete_status": self.delete_status,
                }}
