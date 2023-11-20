from datetime import datetime
import json

import db
from flask import Flask
from flask import request


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
    res = { 
        "id": user_id,
        "name": name,
        "username": username,
        "balance": balance,
        "transactions": []
    }
    return json.dumps(res), 201

@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting user by its user_id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    user_transactions = DB.get_interactions_of_user(user_id)
    res = { 
        "id": user.get("id"),
        "name": user.get("name"),
        "username": user.get("username"),
        "balance": user.get("balance"),
        "transactions": user_transactions
    }
    return json.dumps(res), 200

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """Endpoint for deleting task"""
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    user_transactions = DB.get_interactions_of_user(user_id)
    res = { 
        "id": user.get("id"),
        "name": user.get("name"),
        "username": user.get("username"),
        "balance": user.get("balance"),
        "transactions": user_transactions
    }
    DB.delete_user_by_id(user_id)
    return json.dumps(res), 200

@app.route("/api/transactions/", methods= ["POST"])
def create_transaction():
    """
    Endpoint for creating a transaction
    between a sender and receiver, either
    requesting or sending money 
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    message = body.get("message")
    accepted = body.get("accepted")
    if sender_id == None or receiver_id == None or amount == None or message == None:
        return json.dumps({"error": "Missing field in transaction request"}), 400
    sender = DB.get_user_by_id(sender_id)
    if sender == None: 
        return json.dumps({"error": "User not found"}), 404
    receiver = DB.get_user_by_id(receiver_id)
    if receiver == None: 
        return json.dumps({"error": "User not found"}), 404
    if accepted:   
        s_balance = sender.get("balance")
        r_balance= receiver.get("balance")
        if s_balance >= amount: 
            DB.update_user(sender_id, s_balance - amount)
            DB.update_user(receiver_id, r_balance + amount)
            id =DB.insert_interaction(datetime.now(), sender_id, receiver_id, amount, message, 1)
            res = DB.get_interaction_by_id(id)
            return json.dumps(res), 201
        else: 
            return json.dumps({"error": "Transaction amount greater than sender balance"}), 403
    else:
        id = DB.insert_interaction(datetime.now(), sender_id, receiver_id, amount, message, None)
        res = DB.get_interaction_by_id(id)
        return json.dumps(res), 201

@app.route("/api/transactions/<int:id>/", methods= ["POST"])
def accept_or_deny(id):
    """
    Endpoint for accepting or denying a request
    between a sender and receiver
    """
    body = json.loads(request.data)
    accepted = body.get("accepted")
    curr_transaction = DB.get_interaction_by_id(id)
    if (curr_transaction==None):
        return json.dumps({"error": "Transaction not found"}), 404
    curr_accepted = curr_transaction.get("accepted")
    sender_id = curr_transaction.get("sender_id")
    receiver_id = curr_transaction.get("receiver_id")
    if curr_accepted == True or curr_accepted == False:
        return json.dumps({"error": "Cannot modify this transaction's accepted field because it already contains a value"}), 403
   
    sender = DB.get_user_by_id(sender_id)
    if sender == None: 
        return json.dumps({"error": "User not found"}), 404
    receiver = DB.get_user_by_id(receiver_id)
    if receiver == None: 
        return json.dumps({"error": "User not found"}), 404
    
    if accepted: 
            amount = curr_transaction.get("amount")
            s_balance = sender.get("balance")
            r_balance = receiver.get("balance")
            if s_balance >= amount: 
                DB.update_user(sender_id, s_balance - amount)
                DB.update_user(receiver_id, r_balance + amount)
                DB.update_interaction(datetime.now(),id ,1)
            else: 
                return json.dumps({"error": "Transaction amount greater than sender balance"}), 403
    else:
            DB.update_interaction(datetime.now(),id, 0)

    res= DB.get_interaction_by_id(id)
    return json.dumps(res), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

