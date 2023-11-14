import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)

@app.route("/")
@app.route("/api/users/", methods = ["GET"]) 
def get_users():
    """Endpoint for getting all users"""
    return json.dumps({"users": DB.get_all_users()}), 200


# your routes here
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating user 
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    if name == None or username == None:
        return json.dumps({"error": "Missing field when creating user"}), 400
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "Something wrong happened when creating user"})
    return json.dumps(user), 201

@app.route("/api/user/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting user by its user_id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    return json.dumps(user), 200

@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """Endpoint for deleting task"""
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/send/", methods= ["POST"])
def send_money():
    """
    Endpoint for sending money from a 
    sender to a receiver, updating sender
    and receiver's balances respectively 
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    if sender_id == None or receiver_id == None or amount == None:
        return json.dumps({"error": "Missing field in send money request"}), 400
    current_sender= DB.get_user_by_id(sender_id)
    if current_sender is None:
        return json.dumps({"error": "User not found"}), 404
    current_user_amount = current_sender.get("balance")
    if (amount > current_user_amount):
        return json.dumps({"error": "Amount withdrawn exceeds user balance"}), 400
    new_user_amount = current_user_amount - amount
    DB.update_user(sender_id, new_user_amount)
    receiver_user = DB.get_user_by_id(receiver_id)
    if receiver_user is None:
        return json.dumps({"error": "User not found"}), 404
    new_receiver_amount = receiver_user.get("balance")
    DB.update_user(receiver_id, new_receiver_amount)    
    res = {"sender_id": sender_id, "receiver_id": receiver_id, "amount": amount}
    return json.dumps(res), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
