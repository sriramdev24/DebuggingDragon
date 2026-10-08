import logging
import copy
from pymongo import MongoClient
import mongomock
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from seed_data import INITIAL_USERS, INITIAL_EXCHANGES, INITIAL_POSTS, INITIAL_STORIES, INITIAL_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skilldna_db")

_db_instance = None
_is_cloud = False
_connection_status_msg = ""

def get_db():
    global _db_instance, _is_cloud, _connection_status_msg
    if _db_instance is not None:
        return _db_instance

    mongo_uri = Config.MONGO_URI.strip() if Config.MONGO_URI else ""
    if mongo_uri:
        try:
            logger.info("Attempting connection to MongoDB Atlas...")
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=4000)
            client.admin.command('ping')
            _db_instance = client[Config.DB_NAME]
            _is_cloud = True
            _connection_status_msg = "Connected to MongoDB Cloud (Atlas)"
            logger.info("Successfully connected to MongoDB Cloud.")
            _ensure_seeded(_db_instance)
            return _db_instance
        except Exception as e:
            logger.warning(f"Could not connect to MongoDB Atlas ({e}). Falling back to in-memory MongoDB mock.")
            _connection_status_msg = f"Atlas unavailable. Using in-memory MongoMock."
    else:
        _connection_status_msg = "Using in-memory MongoMock (Atlas URI can be configured in .env)"

    mock_client = mongomock.MongoClient()
    _db_instance = mock_client[Config.DB_NAME]
    _is_cloud = False
    _ensure_seeded(_db_instance)
    return _db_instance

def get_db_status():
    get_db()
    return {
        "is_cloud": _is_cloud,
        "message": _connection_status_msg
    }

def _ensure_seeded(db):
    try:
        if db.users.count_documents({}) == 0:
            logger.info("Seeding initial campus users...")
            default_pwd_hash = generate_password_hash("password123")
            seeded_users = []
            for u in INITIAL_USERS:
                uc = copy.deepcopy(u)
                uc["email"] = uc["email"].lower()
                if "password_hash" not in uc:
                    uc["password_hash"] = default_pwd_hash
                seeded_users.append(uc)
            db.users.insert_many(seeded_users)
        
        if db.exchanges.count_documents({}) == 0:
            logger.info("Seeding initial exchanges...")
            db.exchanges.insert_many([copy.deepcopy(e) for e in INITIAL_EXCHANGES])

        if db.posts.count_documents({}) == 0:
            logger.info("Seeding initial social posts...")
            db.posts.insert_many([copy.deepcopy(p) for p in INITIAL_POSTS])

        if db.stories.count_documents({}) == 0:
            logger.info("Seeding initial campus stories...")
            db.stories.insert_many([copy.deepcopy(s) for s in INITIAL_STORIES])

        if db.messages.count_documents({}) == 0:
            logger.info("Seeding initial peer messages...")
            db.messages.insert_many([copy.deepcopy(m) for m in INITIAL_MESSAGES])
    except Exception as e:
        logger.error(f"Error during db seeding: {e}")

# --- User Helpers ---

def get_all_users():
    db = get_db()
    return list(db.users.find({}))

def get_user_by_id(user_id):
    db = get_db()
    return db.users.find_one({"_id": user_id})

def get_user_by_email(email):
    if not email:
        return None
    db = get_db()
    return db.users.find_one({"email": email.strip().lower()})

def save_user(user_data):
    db = get_db()
    return db.users.insert_one(user_data)

def create_user(user_data):
    db = get_db()
    if "email" in user_data:
        user_data["email"] = user_data["email"].strip().lower()
    db.users.insert_one(user_data)
    return user_data

def update_user(user_id, update_fields):
    db = get_db()
    return db.users.update_one({"_id": user_id}, {"$set": update_fields})

def toggle_follow(user_id, target_id):
    if user_id == target_id:
        return False
    db = get_db()
    curr_user = db.users.find_one({"_id": user_id})
    target_user = db.users.find_one({"_id": target_id})
    if not curr_user or not target_user:
        return False

    following = curr_user.get("following", [])
    followers = target_user.get("followers", [])

    if target_id in following:
        following.remove(target_id)
        if user_id in followers:
            followers.remove(user_id)
        is_following = False
    else:
        following.append(target_id)
        if user_id not in followers:
            followers.append(user_id)
        is_following = True

    db.users.update_one({"_id": user_id}, {"$set": {"following": following}})
    db.users.update_one({"_id": target_id}, {"$set": {"followers": followers}})
    return is_following

# --- Exchange Helpers ---

def get_all_exchanges():
    db = get_db()
    return list(db.exchanges.find({}).sort("created_at", -1))

def get_user_exchanges(user_id):
    db = get_db()
    return list(db.exchanges.find({"participants": user_id}).sort("created_at", -1))

def get_exchange_by_id(exchange_id):
    db = get_db()
    return db.exchanges.find_one({"_id": exchange_id})

def save_exchange(exchange_data):
    db = get_db()
    return db.exchanges.insert_one(exchange_data)

def update_exchange(exchange_id, update_fields):
    db = get_db()
    return db.exchanges.update_one({"_id": exchange_id}, {"$set": update_fields})

# --- Social Post Helpers ---

def get_all_posts():
    db = get_db()
    posts = list(db.posts.find({}).sort("created_at", -1))
    # populate author info
    users_map = {u["_id"]: u for u in db.users.find({})}
    for p in posts:
        p["author"] = users_map.get(p.get("author_id"), {
            "name": "Campus Peer",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
            "department": "Student",
            "handle": "@student"
        })
    return posts

def get_user_posts(user_id):
    db = get_db()
    posts = list(db.posts.find({"author_id": user_id}).sort("created_at", -1))
    user = get_user_by_id(user_id)
    for p in posts:
        p["author"] = user
    return posts

def save_post(post_data):
    db = get_db()
    return db.posts.insert_one(post_data)

def toggle_like_post(post_id, user_id):
    db = get_db()
    post = db.posts.find_one({"_id": post_id})
    if not post:
        return 0, False
    likes = post.get("likes", [])
    if user_id in likes:
        likes.remove(user_id)
        liked = False
    else:
        likes.append(user_id)
        liked = True
    db.posts.update_one({"_id": post_id}, {"$set": {"likes": likes}})
    return len(likes), liked

def add_comment_to_post(post_id, comment_data):
    db = get_db()
    return db.posts.update_one({"_id": post_id}, {"$push": {"comments": comment_data}})

# --- Stories Helpers ---

def get_all_stories():
    db = get_db()
    stories = list(db.stories.find({}))
    users_map = {u["_id"]: u for u in db.users.find({})}
    for s in stories:
        s["user"] = users_map.get(s.get("user_id"), {
            "name": "Peer",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        })
    return stories

def save_story(story_data):
    db = get_db()
    return db.stories.insert_one(story_data)

# --- Direct Messaging Helpers ---

def get_user_conversations(user_id):
    db = get_db()
    # Find all messages where user is sender or receiver
    msgs = list(db.messages.find({
        "$or": [{"sender_id": user_id}, {"receiver_id": user_id}]
    }))
    
    users_map = {u["_id"]: u for u in db.users.find({})}
    conversations = {}

    for m in msgs:
        partner_id = m["receiver_id"] if m["sender_id"] == user_id else m["sender_id"]
        if partner_id not in conversations:
            conversations[partner_id] = {
                "partner": users_map.get(partner_id),
                "last_message": m.get("text"),
                "timestamp": m.get("created_at"),
                "unread": 1 if m.get("receiver_id") == user_id and not m.get("read", False) else 0
            }
        else:
            conversations[partner_id]["last_message"] = m.get("text")
            conversations[partner_id]["timestamp"] = m.get("created_at")

    # If no conversations yet, suggest top 2 users
    if not conversations:
        for u in db.users.find({"_id": {"$ne": user_id}}).limit(2):
            conversations[u["_id"]] = {
                "partner": u,
                "last_message": "Say hi to start trading skills!",
                "timestamp": "Just now",
                "unread": 0
            }

    return list(conversations.values())

def get_conversation_messages(user_id, partner_id):
    db = get_db()
    msgs = list(db.messages.find({
        "$or": [
            {"sender_id": user_id, "receiver_id": partner_id},
            {"sender_id": partner_id, "receiver_id": user_id}
        ]
    }))
    # mark messages as read
    db.messages.update_many(
        {"sender_id": partner_id, "receiver_id": user_id},
        {"$set": {"read": True}}
    )
    return msgs

def save_message(msg_data):
    db = get_db()
    return db.messages.insert_one(msg_data)
