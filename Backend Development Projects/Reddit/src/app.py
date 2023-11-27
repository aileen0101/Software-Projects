import json

from flask import Flask #object of Flask type
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {"id": 0, "upvotes": 1, "title": "My cat is the cutest", 
    "link": "https://i.imgur.com/jseZqNK.jpg", "username": "alicia98"},
    1: {"id": 1, "upvotes": 3, "title": "Cat loaf", 
    "link": "https://i.imgur.com/TJ46wX4.jpg", "username": "alicia98"}
}

post_current_id = 2

posts_with_comments = {
    0: {"id": 0, "upvotes": 1, "title": "My cat is the cutest", 
    "link": "https://i.imgur.com/jseZqNK.jpg", "username": "alicia98", 
    "comments": {0: {"id": 0, "upvotes": 8, "text": "Wow, my first Reddit gold!", "username": "alicia98"}}}
,
    1: {"id": 1, "upvotes": 3, "title": "Cat loaf", 
    "link": "https://i.imgur.com/TJ46wX4.jpg", "username": "alicia98",
    "comments":{}},
}

posts_with_comments_id = 2
comment_id = 1

# your routes here
@app.route("/api/posts/", methods = ["GET"])


def getPosts():
    """Returns all posts in our posts dictionary."""
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route ("/api/posts/", methods = ["POST"])

def createPost():
    """Creates a posts in our posts dictionary. Returns the new post."""
    global post_current_id
    global posts_with_comments_id
    body = json.loads(request.data)
    link = body.get("link")
    title = body.get("title")
    username = body.get("username")
    if (link == None or body == None or title == None or username == None):
        return json.dumps({"error": "Missing field in your request"}), 400
    new_post = {"id": post_current_id, "upvotes": 1, "title": title, "link": link, "username": username}
    posts[post_current_id]=new_post
    post_current_id += 1
    new_post_for_comments = {"id": post_current_id, "upvotes": 1, "title": title, "link": link, "username": username, "comments": {}}
    posts_with_comments[posts_with_comments_id] = new_post_for_comments
    posts_with_comments_id +=1
    return json.dumps(new_post), 201

@app.route ("/api/posts/<int:id>/", methods = ["GET"])
def getOnePost(id):
    """Returns a post at [id] from our dictionary."""
    post= posts.get(id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

@app.route ("/api/posts/<int:id>/", methods=["DELETE"])
def deletePost(id):
    """Deletes a post at [id] from our dictionary."""
    post = posts.get(id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    del posts[id]
    return json.dumps(post), 200
    

@app.route ("/api/posts/<int:id>/comments/", methods=["GET"])
def getComments(id):
    """Returns all comments of a post at [id] from our dictionary posts_with_comments."""
    post = posts_with_comments.get(id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    comments = post.get("comments")
    res = {"comments": list(comments.values())}
    return json.dumps(res), 200

@app.route ("/api/posts/<int:id>/comments/", methods=["POST"])

def postComment(id):
    """Creates a comment for a post at [id] and returns the new comment."""
    global comment_id
    #get post
    post = posts_with_comments.get(id)
    data = json.loads(request.data)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    text = data.get("text")
    username = data.get("username")
    if (text == None or username == None):
        return json.dumps({"error": "Missing field in your request"}), 400
    new_comment = {"id": comment_id, "upvotes": 1, "text": text, "username": username}
    post["comments"][comment_id]= new_comment #adding new comment 
    comment_id+=1
    return json.dumps(new_comment), 201

@app.route ("/api/posts/<int:pid>/comments/<int:cid>/", methods=["POST"])
def editComment(pid, cid):
    """Edits a comment for a post at [id] and returns the new comment."""
    post = posts_with_comments.get(pid)
    data = json.loads(request.data)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    text = data.get("text")
    if text == None:
         return json.dumps({"error": "Missing field in your request"}), 400
#access comment of specific cid: access text field in comment
    comments = post.get("comments")
    comment = comments.get(cid)
#modify text field with request data
    comment["text"]=text
#return new comment 
    return json.dumps(comment), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)