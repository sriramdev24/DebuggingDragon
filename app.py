import os
import uuid
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from config import Config
import db
import matcher

app = Flask(__name__)
app.config.from_object(Config)


SKILL_CATEGORIES = [
    "Programming",
    "Software Engineering",
    "Design",
    "Creative Tech",
    "Media",
    "Languages",
    "Academics",
    "Communication",
    "Music & Audio",
    "Business"
]

PROFICIENCY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ALL_SLOTS = [
    "Morning (9 AM - 12 PM)",
    "Afternoon (1 PM - 4 PM)",
    "Evening (5 PM - 8 PM)",
    "Night (8 PM - 10 PM)"
]

TRENDING_TAGS = [
    {"tag": "#FigmaTokens", "count": "18 swaps", "category": "Design"},
    {"tag": "#PythonAutomation", "count": "24 swaps", "category": "Programming"},
    {"tag": "#MotionCuts", "count": "12 swaps", "category": "Media"},
    {"tag": "#ConversationalSpanish", "count": "15 swaps", "category": "Languages"},
    {"tag": "#LeetCodeHard", "count": "21 swaps", "category": "Programming"},
    {"tag": "#AbletonBeats", "count": "9 swaps", "category": "Music"}
]

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or not db.get_user_by_id(session["user_id"]):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
                return jsonify({"success": False, "error": "Login required.", "redirect": url_for("login")}), 401
            flash("Please log in to access this feature.", "info")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.context_processor
def inject_global_data():
    current_uid = session.get("user_id")
    current_user = db.get_user_by_id(current_uid) if current_uid else None
    all_users = db.get_all_users()
    db_status = db.get_db_status()
    
    
    user_exchanges = db.get_user_exchanges(current_uid) if current_uid else []
    pending_count = sum(1 for e in user_exchanges if e.get("status") == "pending" and e.get("recipient_id") == current_uid)
    active_count = sum(1 for e in user_exchanges if e.get("status") in ["active", "scheduled"])

 
    conversations = db.get_user_conversations(current_uid) if current_uid else []
    unread_messages = sum(c.get("unread", 0) for c in conversations)

    return {
        "current_user": current_user,
        "all_users": all_users,
        "db_status": db_status,
        "pending_count": pending_count,
        "active_count": active_count,
        "unread_messages": unread_messages,
        "categories": SKILL_CATEGORIES,
        "levels": PROFICIENCY_LEVELS,
        "all_days": ALL_DAYS,
        "all_slots": ALL_SLOTS,
        "trending_tags": TRENDING_TAGS
    }



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

        user = db.get_user_by_email(email)
        if not user:
             
            clean_handle = email.lstrip("@").lower()
            user = db.get_user_by_id(email) or db.get_user_by_id(f"user_{clean_handle}")
            if not user:
                db_inst = db.get_db()
                user = db_inst.users.find_one({"handle": f"@{clean_handle}"}) or \
                       db_inst.users.find_one({"handle": clean_handle}) or \
                       db_inst.users.find_one({"email": {"$regex": f"^{email}", "$options": "i"}}) or \
                       db_inst.users.find_one({"name": {"$regex": f"^{email}", "$options": "i"}})

        valid = False
        if user:
            # Check password hash if present, or allow demo password 'password123'
            pwd_hash = user.get("password_hash")
            if pwd_hash:
                valid = check_password_hash(pwd_hash, password) or password == "password123"
            else:
                valid = (password == "password123" or len(password) >= 4)

        if valid:
            session["user_id"] = user["_id"]
            next_url = request.args.get("next") or url_for("index")
            msg = f"Welcome back, {user['name']}!"
            if is_ajax:
                return jsonify({"success": True, "message": msg, "redirect": next_url})
            flash(msg, "success")
            return redirect(next_url)
        else:
            err = "Invalid email or password. Default demo password is 'password123'."
            if is_ajax:
                return jsonify({"success": False, "error": err}), 400
            flash(err, "error")
            return render_template("login.html", demo_users=db.get_all_users()[:6])

    demo_users = db.get_all_users()[:6]
    return render_template("login.html", demo_users=demo_users)

@app.route("/demo-login/<user_id>", methods=["POST", "GET"])
def demo_login(user_id):
    target = db.get_user_by_id(user_id)
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json
    if target:
        session["user_id"] = user_id
        msg = f"Logged in as demo user {target['name']}!"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "redirect": url_for("index")})
        flash(msg, "info")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        department = request.form.get("department", "Computer Science").strip()
        year = request.form.get("year", "Sophomore (2nd Year)").strip()
        bio = request.form.get("bio", "Student eager to exchange knowledge on campus.").strip()
        
        # Initial Offered Skill
        offer_name = request.form.get("offer_name", "").strip()
        offer_category = request.form.get("offer_category", "Programming")
        offer_level = request.form.get("offer_level", "Intermediate")
        
        # Initial Wanted Skill
        want_name = request.form.get("want_name", "").strip()
        want_category = request.form.get("want_category", "Design")
        want_level = request.form.get("want_level", "Beginner")

        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

        if not name or not email or not password:
            err = "Name, email, and password are required."
            if is_ajax:
                return jsonify({"success": False, "error": err}), 400
            flash(err, "error")
            return render_template("register.html")

        if db.get_user_by_email(email):
            err = "An account with this email is already registered."
            if is_ajax:
                return jsonify({"success": False, "error": err}), 400
            flash(err, "error")
            return render_template("register.html")

        user_id = f"user_{uuid.uuid4().hex[:8]}"
        clean_name = name.strip()
        avatar_choice = request.form.get("avatar") or f"https://api.dicebear.com/7.x/open-peeps/svg?seed={clean_name.replace(' ', '_')}&backgroundColor=b6e3f4"
        new_user = {
            "_id": user_id,
            "name": clean_name,
            "handle": f"@{clean_name.lower().replace(' ', '_')}",
            "email": email,
            "password_hash": generate_password_hash(password),
            "department": department,
            "year": year,
            "bio": bio,
            "avatar": avatar_choice,
            "cover_photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1000&auto=format&fit=crop&q=80",
            "skills_offered": [
                {
                    "id": f"so_{uuid.uuid4().hex[:6]}",
                    "name": offer_name or "General Problem Solving",
                    "category": offer_category,
                    "level": offer_level,
                    "experience": "Campus student project experience",
                    "endorsements": 0
                }
            ],
            "skills_wanted": [
                {
                    "id": f"sw_{uuid.uuid4().hex[:6]}",
                    "name": want_name or "UI/UX Design",
                    "category": want_category,
                    "target_level": want_level,
                    "goal": "Learn practical hands-on foundations"
                }
            ],
            "availability": {
                "days": ["Monday", "Wednesday", "Friday"],
                "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
                "format": "Hybrid (Campus or Online)",
                "hours_per_week": 4
            },
            "karma_points": 100,
            "completed_swaps": 0,
            "rating": 5.0,
            "followers": [],
            "following": []
        }

        db.create_user(new_user)
        session["user_id"] = user_id
        msg = f"Account created! Welcome to SkillSwap DNA, {name}!"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "redirect": url_for("index")})
        flash(msg, "success")
        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json
    if is_ajax:
        return jsonify({"success": True, "message": "You have been signed out.", "redirect": url_for("login")})
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))

# ----------------- Social Feed & Main Pages -----------------

@app.route("/")
def index():
    current_uid = session.get("user_id")
    current_user = db.get_user_by_id(current_uid) if current_uid else None
    all_users = db.get_all_users()
    all_exchanges = db.get_all_exchanges()

    posts = db.get_all_posts()
    stories = db.get_all_stories()

    direct_matches = []
    group_pods = []
    if current_user:
        direct_matches = matcher.find_direct_matches(current_user, all_users)
        group_pods = matcher.find_group_pods(current_user, all_users)
    else:
        # Campus preview matches for guests from seed demo user
        demo_user = db.get_user_by_id("user_alex") or (all_users[0] if all_users else None)
        if demo_user:
            direct_matches = matcher.find_direct_matches(demo_user, all_users)
            group_pods = matcher.find_group_pods(demo_user, all_users)

    my_exchanges = [e for e in all_exchanges if current_uid in e.get("participants", [])] if current_uid else []
    
    # Campus stats
    stats = {
        "total_swappers": len(all_users),
        "total_skills": sum(len(u.get("skills_offered", [])) for u in all_users),
        "active_exchanges": sum(1 for e in all_exchanges if e.get("status") in ["active", "scheduled"]),
        "completed_sessions": sum(e.get("completed_sessions", 0) for e in all_exchanges)
    }

    return render_template(
        "index.html",
        posts=posts,
        stories=stories,
        direct_matches=direct_matches[:4],
        group_pods=group_pods[:2],
        my_exchanges=my_exchanges[:3],
        stats=stats
    )

# ----------------- Social Post Interactions -----------------

@app.route("/posts/create", methods=["POST"])
@login_required
def create_post():
    current_uid = session.get("user_id")
    content = request.form.get("content", "").strip()
    skill_tag = request.form.get("skill_tag", "Skill Barter").strip()
    post_type = request.form.get("post_type", "showcase")
    image_url = request.form.get("image_url", "").strip()

    if not content:
        flash("Post content cannot be empty.", "warning")
        return redirect(url_for("index"))

    new_post = {
        "_id": f"post_{uuid.uuid4().hex[:8]}",
        "author_id": current_uid,
        "content": content,
        "skill_tag": skill_tag,
        "post_type": post_type,
        "image": image_url if image_url else None,
        "likes": [],
        "comments": [],
        "created_at": "Just now"
    }
    db.save_post(new_post)
    flash("Post shared with campus network!", "success")
    return redirect(url_for("index"))

@app.route("/posts/like/<post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    current_uid = session.get("user_id")
    count, liked = db.toggle_like_post(post_id, current_uid)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"likes_count": count, "liked": liked})
    return redirect(request.referrer or url_for("index"))

@app.route("/posts/comment/<post_id>", methods=["POST"])
@login_required
def comment_post(post_id):
    current_uid = session.get("user_id")
    user = db.get_user_by_id(current_uid)
    text = request.form.get("text", "").strip()

    if not text:
        flash("Comment cannot be empty.", "warning")
        return redirect(request.referrer or url_for("index"))

    comment_doc = {
        "id": f"c_{uuid.uuid4().hex[:6]}",
        "user_id": current_uid,
        "user_name": user.get("name", "Student"),
        "user_avatar": user.get("avatar", ""),
        "text": text,
        "created_at": "Just now"
    }
    db.add_comment_to_post(post_id, comment_doc)
    flash("Comment posted!", "success")
    return redirect(request.referrer or url_for("index"))

@app.route("/stories/create", methods=["POST"])
@login_required
def create_story():
    current_uid = session.get("user_id")
    text = request.form.get("text", "").strip()
    skill_tag = request.form.get("skill_tag", "Skill Radar").strip()
    gradient = request.form.get("gradient", "from-indigo-600 to-pink-500")

    if not text:
        flash("Story text cannot be empty.", "warning")
        return redirect(url_for("index"))

    new_story = {
        "_id": f"story_{uuid.uuid4().hex[:6]}",
        "user_id": current_uid,
        "text": text,
        "skill_tag": skill_tag,
        "gradient": gradient
    }
    db.save_story(new_story)
    flash("Skill Story posted to campus radar!", "success")
    return redirect(url_for("index"))

# ----------------- Direct Peer Messaging (DMs) -----------------

@app.route("/messages")
@app.route("/messages/<peer_id>")
@login_required
def messages(peer_id=None):
    current_uid = session.get("user_id")
    all_users = db.get_all_users()
    conversations = db.get_user_conversations(current_uid)

    if not peer_id and conversations:
        peer_id = conversations[0]["partner"]["_id"]
    elif not peer_id:
        # Default to another user
        other_user = next((u for u in all_users if u["_id"] != current_uid), None)
        peer_id = other_user["_id"] if other_user else None

    active_peer = db.get_user_by_id(peer_id) if peer_id else None
    chat_messages = db.get_conversation_messages(current_uid, peer_id) if (current_uid and peer_id) else []

    # Reciprocal match status between active chat peers
    peer_match_info = None
    if current_uid and active_peer:
        direct_matches = matcher.find_direct_matches(db.get_user_by_id(current_uid), [active_peer])
        if direct_matches:
            peer_match_info = direct_matches[0]

    return render_template(
        "messages.html",
        conversations=conversations,
        active_peer=active_peer,
        chat_messages=chat_messages,
        peer_match_info=peer_match_info
    )

@app.route("/messages/send", methods=["POST"])
@login_required
def send_message():
    current_uid = session.get("user_id")
    receiver_id = request.form.get("receiver_id")
    text = request.form.get("text", "").strip()
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

    if not text or not receiver_id:
        if is_ajax:
            return jsonify({"success": False, "error": "Message cannot be empty."}), 400
        return redirect(url_for("messages"))

    msg_doc = {
        "_id": f"msg_{uuid.uuid4().hex[:8]}",
        "sender_id": current_uid,
        "receiver_id": receiver_id,
        "text": text,
        "created_at": datetime.datetime.now().strftime("%I:%M %p"),
        "read": False
    }
    db.save_message(msg_doc)

    if is_ajax:
        return jsonify({
            "success": True,
            "message": msg_doc
        })

    return redirect(url_for("messages", peer_id=receiver_id))

# ----------------- Public Social User Profile -----------------

@app.route("/user/<user_id>")
def user_profile(user_id):
    current_uid = session.get("user_id")
    target_user = db.get_user_by_id(user_id)
    if not target_user:
        flash("User not found.", "error")
        return redirect(url_for("index"))

    user_posts = db.get_user_posts(user_id)
    all_exchanges = db.get_user_exchanges(user_id)
    is_following = user_id in db.get_user_by_id(current_uid).get("following", [])

    return render_template(
        "user_profile.html",
        user=target_user,
        user_posts=user_posts,
        exchanges=all_exchanges,
        is_following=is_following
    )

@app.route("/user/<user_id>/follow", methods=["POST"])
@login_required
def follow_user(user_id):
    current_uid = session.get("user_id")
    is_following = db.toggle_follow(current_uid, user_id)
    target_user = db.get_user_by_id(user_id)
    msg = f"You are now following {target_user.get('name')}!" if is_following else f"Unfollowed {target_user.get('name')}."
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({
            "success": True,
            "is_following": is_following,
            "message": msg
        })

    flash(msg, "success" if is_following else "info")
    return redirect(request.referrer or url_for("user_profile", user_id=user_id))

# ----------------- Matcher & Network & Directory -----------------

@app.route("/matches")
def matches():
    current_uid = session.get("user_id")
    current_user = db.get_user_by_id(current_uid) if current_uid else None
    all_users = db.get_all_users()

    if not current_user:
        flash("Please log in or select a demo student persona to view your DNA matches.", "info")
        return redirect(url_for("login", next=url_for("matches")))

    direct_matches = matcher.find_direct_matches(current_user, all_users)
    group_pods = matcher.find_group_pods(current_user, all_users)

    return render_template(
        "matches.html",
        direct_matches=direct_matches,
        group_pods=group_pods,
        all_users=all_users
    )

@app.route("/network")
def network():
    return render_template("network.html")

@app.route("/directory")
def directory():
    all_users = db.get_all_users()
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    level = request.args.get("level", "").strip()

    filtered_users = []
    for u in all_users:
        if query:
            name_match = query in u.get("name", "").lower()
            dept_match = query in u.get("department", "").lower()
            skill_match = any(query in s.get("name", "").lower() for s in u.get("skills_offered", []) + u.get("skills_wanted", []))
            if not (name_match or dept_match or skill_match):
                continue

        if category:
            cat_match = any(s.get("category") == category for s in u.get("skills_offered", []) + u.get("skills_wanted", []))
            if not cat_match:
                continue

        if level:
            lvl_match = any(s.get("level") == level for s in u.get("skills_offered", []))
            if not lvl_match:
                continue

        filtered_users.append(u)

    return render_template(
        "directory.html",
        users=filtered_users,
        query=query,
        selected_category=category,
        selected_level=level
    )

@app.route("/exchanges")
@login_required
def exchanges():
    current_uid = session.get("user_id")
    all_exchanges = db.get_user_exchanges(current_uid)
    all_users_map = {u["_id"]: u for u in db.get_all_users()}

    pending_incoming = []
    pending_outgoing = []
    active_exchanges = []
    completed_exchanges = []

    for ex in all_exchanges:
        status = ex.get("status")
        if status == "pending":
            if ex.get("recipient_id") == current_uid:
                pending_incoming.append(ex)
            else:
                pending_outgoing.append(ex)
        elif status in ["active", "scheduled"]:
            active_exchanges.append(ex)
        elif status == "completed":
            completed_exchanges.append(ex)

    return render_template(
        "exchanges.html",
        pending_incoming=pending_incoming,
        pending_outgoing=pending_outgoing,
        active_exchanges=active_exchanges,
        completed_exchanges=completed_exchanges,
        users_map=all_users_map
    )

@app.route("/profile")
@login_required
def profile():
    current_uid = session.get("user_id")
    user = db.get_user_by_id(current_uid)
    return render_template("profile.html", user=user)

# ----------------- Profile & Exchange Mutations -----------------

@app.route("/switch-user/<user_id>")
def switch_user(user_id):
    target = db.get_user_by_id(user_id)
    if target:
        session["user_id"] = user_id
        flash(f"Switched identity to {target['name']} ({target.get('department')})", "info")
    return redirect(request.referrer or url_for("index"))

@app.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    current_uid = session.get("user_id")
    bio = request.form.get("bio", "").strip()
    department = request.form.get("department", "").strip()
    year = request.form.get("year", "").strip()
    days = request.form.getlist("days")
    slots = request.form.getlist("slots")
    format_pref = request.form.get("format", "Hybrid")
    hours = int(request.form.get("hours_per_week", 4) or 4)

    update_doc = {
        "bio": bio,
        "department": department,
        "year": year,
        "availability": {
            "days": days,
            "slots": slots,
            "format": format_pref,
            "hours_per_week": hours
        }
    }
    db.update_user(current_uid, update_doc)
    msg = "Skill DNA Profile & Availability updated successfully!"
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": True, "message": msg})
    flash(msg, "success")
    return redirect(url_for("profile"))

@app.route("/profile/skill/add", methods=["POST"])
@login_required
def add_skill():
    current_uid = session.get("user_id")
    user = db.get_user_by_id(current_uid)
    skill_type = request.form.get("skill_type")
    skill_name = request.form.get("name", "").strip()
    category = request.form.get("category", "General")
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json
    
    if not skill_name:
        if is_ajax:
            return jsonify({"success": False, "error": "Skill name cannot be empty."}), 400
        flash("Skill name cannot be empty.", "error")
        return redirect(url_for("profile"))

    if skill_type == "offered":
        level = request.form.get("level", "Intermediate")
        experience = request.form.get("experience", "").strip()
        new_item = {
            "id": f"so_{uuid.uuid4().hex[:6]}",
            "name": skill_name,
            "category": category,
            "level": level,
            "experience": experience,
            "endorsements": 0
        }
        current_skills = user.get("skills_offered", [])
        current_skills.append(new_item)
        db.update_user(current_uid, {"skills_offered": current_skills})
        msg = f"Added offered skill: {skill_name} ({level})"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "skill": new_item, "skill_type": "offered"})
        flash(msg, "success")

    elif skill_type == "wanted":
        target_level = request.form.get("target_level", "Beginner")
        goal = request.form.get("goal", "").strip()
        new_item = {
            "id": f"sw_{uuid.uuid4().hex[:6]}",
            "name": skill_name,
            "category": category,
            "target_level": target_level,
            "goal": goal
        }
        current_skills = user.get("skills_wanted", [])
        current_skills.append(new_item)
        db.update_user(current_uid, {"skills_wanted": current_skills})
        msg = f"Added target learning goal: {skill_name}"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "skill": new_item, "skill_type": "wanted"})
        flash(msg, "success")

    return redirect(url_for("profile"))

@app.route("/profile/skill/delete/<skill_type>/<skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_type, skill_id):
    current_uid = session.get("user_id")
    user = db.get_user_by_id(current_uid)
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

    if skill_type == "offered":
        updated = [s for s in user.get("skills_offered", []) if s.get("id") != skill_id]
        db.update_user(current_uid, {"skills_offered": updated})
        msg = "Offered skill removed."
    elif skill_type == "wanted":
        updated = [s for s in user.get("skills_wanted", []) if s.get("id") != skill_id]
        db.update_user(current_uid, {"skills_wanted": updated})
        msg = "Learning goal removed."

    if is_ajax:
        return jsonify({"success": True, "message": msg, "skill_id": skill_id, "skill_type": skill_type})

    flash(msg, "info")
    return redirect(url_for("profile"))

@app.route("/exchanges/create", methods=["POST"])
@login_required
def create_exchange():
    current_uid = session.get("user_id")
    ex_type = request.form.get("type", "direct")
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

    if ex_type == "direct":
        partner_id = request.form.get("partner_id")
        initiator_offers = request.form.get("initiator_offers", "Skill Swap")
        recipient_offers = request.form.get("recipient_offers", "Skill Swap")
        scheduled_time = request.form.get("scheduled_time", "To be coordinated")
        location = request.form.get("location", "Campus Library / Discord")
        notes = request.form.get("notes", "Let's kick off our peer skill exchange!")

        new_exchange = {
            "_id": f"exch_{uuid.uuid4().hex[:8]}",
            "type": "direct",
            "participants": [current_uid, partner_id],
            "initiator_id": current_uid,
            "recipient_id": partner_id,
            "initiator_offers": initiator_offers,
            "recipient_offers": recipient_offers,
            "status": "pending",
            "scheduled_time": scheduled_time,
            "location": location,
            "created_at": datetime.datetime.now().isoformat(),
            "total_sessions": 3,
            "completed_sessions": 0,
            "notes": notes,
            "reviews": []
        }
        db.save_exchange(new_exchange)
        msg = "Skill Exchange Request sent to your peer!"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "exchange": new_exchange})
        flash(msg, "success")
        return redirect(url_for("exchanges"))

    elif ex_type == "pod":
        member_ids = request.form.getlist("members")
        if current_uid not in member_ids:
            member_ids.append(current_uid)
        
        pod_name = request.form.get("pod_name", "Campus Synergy Pod")
        loop_description = request.form.get("loop_description", "")
        scheduled_time = request.form.get("scheduled_time", "To be coordinated")
        location = request.form.get("location", "Campus MakerSpace / Hybrid")

        new_pod = {
            "_id": f"exch_{uuid.uuid4().hex[:8]}",
            "type": "pod",
            "pod_name": pod_name,
            "participants": member_ids,
            "initiator_id": current_uid,
            "loop_description": loop_description,
            "status": "scheduled",
            "scheduled_time": scheduled_time,
            "location": location,
            "created_at": datetime.datetime.now().isoformat(),
            "total_sessions": len(member_ids),
            "completed_sessions": 0,
            "notes": f"Exchange pod formed! All {len(member_ids)} members share complementary knowledge.",
            "reviews": []
        }
        db.save_exchange(new_pod)
        msg = f"Group Skill Pod '{pod_name}' created successfully!"
        if is_ajax:
            return jsonify({"success": True, "message": msg, "exchange": new_pod})
        flash(msg, "success")
        return redirect(url_for("exchanges"))

    return redirect(url_for("matches"))

@app.route("/exchanges/action/<exchange_id>", methods=["POST"])
@login_required
def exchange_action(exchange_id):
    current_uid = session.get("user_id")
    action = request.form.get("action")
    exchange = db.get_exchange_by_id(exchange_id)
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

    if not exchange:
        if is_ajax:
            return jsonify({"success": False, "error": "Exchange not found."}), 404
        flash("Exchange not found.", "error")
        return redirect(url_for("exchanges"))

    if action == "accept":
        db.update_exchange(exchange_id, {"status": "active"})
        msg = "Exchange request accepted! You can now coordinate sessions."
        if is_ajax:
            return jsonify({"success": True, "action": "accept", "message": msg, "status": "active"})
        flash(msg, "success")
    elif action == "reject":
        db.update_exchange(exchange_id, {"status": "rejected"})
        msg = "Exchange request declined."
        if is_ajax:
            return jsonify({"success": True, "action": "reject", "message": msg, "status": "rejected"})
        flash(msg, "info")
    elif action == "complete_session":
        completed = exchange.get("completed_sessions", 0) + 1
        total = exchange.get("total_sessions", 3)
        status = "completed" if completed >= total else exchange.get("status", "active")
        
        db.update_exchange(exchange_id, {
            "completed_sessions": completed,
            "status": status
        })

        for p_id in exchange.get("participants", []):
            p_user = db.get_user_by_id(p_id)
            if p_user:
                new_karma = p_user.get("karma_points", 100) + 20
                new_swaps = p_user.get("completed_swaps", 0) + (1 if status == "completed" else 0)
                db.update_user(p_id, {"karma_points": new_karma, "completed_swaps": new_swaps})

        msg = f"Session {completed}/{total} marked completed! +20 Points awarded to all participants."
        if is_ajax:
            return jsonify({
                "success": True,
                "action": "complete_session",
                "message": msg,
                "completed_sessions": completed,
                "total_sessions": total,
                "status": status
            })
        flash(msg, "success")
    elif action == "update_schedule":
        scheduled_time = request.form.get("scheduled_time")
        location = request.form.get("location")
        db.update_exchange(exchange_id, {
            "scheduled_time": scheduled_time,
            "location": location
        })
        msg = "Schedule details updated."
        if is_ajax:
            return jsonify({"success": True, "action": "update_schedule", "message": msg, "scheduled_time": scheduled_time, "location": location})
        flash(msg, "success")

    return redirect(url_for("exchanges"))

@app.route("/exchanges/review/<exchange_id>", methods=["POST"])
@login_required
def add_review(exchange_id):
    current_uid = session.get("user_id")
    rating = int(request.form.get("rating", 5))
    comment = request.form.get("comment", "").strip()
    to_user = request.form.get("to_user")
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json

    exchange = db.get_exchange_by_id(exchange_id)
    if not exchange:
        if is_ajax:
            return jsonify({"success": False, "error": "Exchange not found."}), 404
        flash("Exchange not found.", "error")
        return redirect(url_for("exchanges"))

    reviews = exchange.get("reviews", [])
    reviews.append({
        "from_user": current_uid,
        "to_user": to_user,
        "rating": rating,
        "comment": comment,
        "date": datetime.date.today().isoformat()
    })

    db.update_exchange(exchange_id, {"reviews": reviews})
    msg = "Review submitted! Thank you for strengthening the campus knowledge network."
    if is_ajax:
        return jsonify({"success": True, "message": msg})
    flash(msg, "success")
    return redirect(url_for("exchanges"))

# ----------------- JSON API Endpoints -----------------

@app.route("/api/network-data")
def api_network_data():
    all_users = db.get_all_users()
    all_exchanges = db.get_all_exchanges()
    network_data = matcher.get_knowledge_network_data(all_users, all_exchanges)
    return jsonify(network_data)

@app.route("/api/user/<user_id>")
def api_user_details(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
