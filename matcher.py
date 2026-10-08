"""
SkillSwap DNA Matching Engine
Computes:
1. Direct 2-person reciprocal matches with DNA compatibility scores.
2. Multi-person circular exchange pods (Triads & 4-way cycles) when direct swap is unavailable.
3. Campus Knowledge Graph data for interactive visual network.
"""

import re
from typing import List, Dict, Any

LEVEL_WEIGHTS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())

def skill_matches(offered_name: str, wanted_name: str) -> bool:
   
    s1 = normalize_text(offered_name)
    s2 = normalize_text(wanted_name)
    
    if s1 in s2 or s2 in s1:
        return True
    
    tokens1 = set(s1.split())
    tokens2 = set(s2.split())
    # remove noise words
    noise = {"and", "&", "the", "in", "with", "for", "to", "of", "basics", "advanced", "level"}
    t1 = tokens1 - noise
    t2 = tokens2 - noise
    
    if not t1 or not t2:
        return False
        
    overlap = t1.intersection(t2)
    return len(overlap) >= 1

def compute_availability_overlap(avail_a: dict, avail_b: dict) -> tuple:
    """Finds overlapping days and time slots between two users."""
    days_a = set(avail_a.get("days", []))
    days_b = set(avail_b.get("days", []))
    shared_days = list(days_a.intersection(days_b))
    
    slots_a = set(avail_a.get("slots", []))
    slots_b = set(avail_b.get("slots", []))
    shared_slots = list(slots_a.intersection(slots_b))
    
    return shared_days, shared_slots

def compute_compatibility_score(a_teaches_b, b_teaches_a, shared_days, shared_slots) -> int:
    """
    Computes DNA Compatibility percentage (50% to 99%).
    Takes into account skill proficiency levels and schedule synergy.
    """
    score = 60 # Base reciprocal match score
    
    # Check level matching
    t1_level = LEVEL_WEIGHTS.get(a_teaches_b.get("level", "").lower(), 2)
    g1_level = LEVEL_WEIGHTS.get(a_teaches_b.get("target_level", "").lower(), 1)
    if t1_level >= g1_level:
        score += 10
    else:
        score += 5

    t2_level = LEVEL_WEIGHTS.get(b_teaches_a.get("level", "").lower(), 2)
    g2_level = LEVEL_WEIGHTS.get(b_teaches_a.get("target_level", "").lower(), 1)
    if t2_level >= g2_level:
        score += 10
    else:
        score += 5
        
    # Schedule overlap
    if shared_days:
        score += min(len(shared_days) * 4, 12)
    if shared_slots:
        score += min(len(shared_slots) * 5, 10)
        
    return min(score, 99)

def find_direct_matches(user: dict, all_users: List[dict]) -> List[Dict[str, Any]]:
    """
    Finds 2-person reciprocal matches:
    User A has skill User B wants, and User B has skill User A wants.
    """
    matches = []
    u_id = user.get("_id")
    u_offers = user.get("skills_offered", [])
    u_wants = user.get("skills_wanted", [])
    u_avail = user.get("availability", {})

    for partner in all_users:
        p_id = partner.get("_id")
        if p_id == u_id:
            continue
            
        p_offers = partner.get("skills_offered", [])
        p_wants = partner.get("skills_wanted", [])
        p_avail = partner.get("availability", {})

        # Find if user can teach partner
        matched_a_to_b = None
        for off in u_offers:
            for wnt in p_wants:
                if skill_matches(off.get("name", ""), wnt.get("name", "")):
                    matched_a_to_b = {
                        "offered_skill": off,
                        "wanted_skill": wnt,
                        "level": off.get("level"),
                        "target_level": wnt.get("target_level")
                    }
                    break
            if matched_a_to_b:
                break

        # Find if partner can teach user
        matched_b_to_a = None
        for off in p_offers:
            for wnt in u_wants:
                if skill_matches(off.get("name", ""), wnt.get("name", "")):
                    matched_b_to_a = {
                        "offered_skill": off,
                        "wanted_skill": wnt,
                        "level": off.get("level"),
                        "target_level": wnt.get("target_level")
                    }
                    break
            if matched_b_to_a:
                break

        # Reciprocal match found!
        if matched_a_to_b and matched_b_to_a:
            shared_days, shared_slots = compute_availability_overlap(u_avail, p_avail)
            compat_score = compute_compatibility_score(
                matched_a_to_b, matched_b_to_a, shared_days, shared_slots
            )

            reasons = ["Direct 2-way reciprocal skill synergy"]
            if shared_days:
                reasons.append(f"Available together on {', '.join(shared_days)}")
            if shared_slots:
                reasons.append(f"Matching times: {', '.join(shared_slots)}")
            if matched_a_to_b["level"] == "Advanced":
                reasons.append(f"You offer Advanced mentoring in {matched_a_to_b['offered_skill']['name']}")
            if matched_b_to_a["level"] == "Advanced":
                reasons.append(f"{partner.get('name')} offers Advanced expertise in {matched_b_to_a['offered_skill']['name']}")

            matches.append({
                "partner": partner,
                "compatibility_score": compat_score,
                "you_teach": matched_a_to_b["offered_skill"],
                "they_teach": matched_b_to_a["offered_skill"],
                "shared_days": shared_days,
                "shared_slots": shared_slots,
                "reasons": reasons
            })

    # Sort descending by compatibility score
    matches.sort(key=lambda m: m["compatibility_score"], reverse=True)
    return matches

def build_transfer_graph(users: List[dict]):
    """
    Builds a directed adjacency graph where edge (u -> v) means:
    u can TEACH a skill that v WANTS to learn.
    """
    adj = {u["_id"]: [] for u in users}
    edge_details = {}

    for u in users:
        u_id = u["_id"]
        for v in users:
            v_id = v["_id"]
            if u_id == v_id:
                continue

            for off in u.get("skills_offered", []):
                for wnt in v.get("skills_wanted", []):
                    if skill_matches(off.get("name", ""), wnt.get("name", "")):
                        adj[u_id].append(v_id)
                        edge_details[(u_id, v_id)] = {
                            "teacher": u["name"],
                            "student": v["name"],
                            "skill_name": off.get("name"),
                            "level": off.get("level"),
                            "category": off.get("category", "General")
                        }
                        break
                if (u_id, v_id) in edge_details:
                    break

    return adj, edge_details

def find_group_pods(user: dict, all_users: List[dict], max_cycle_len: int = 4) -> List[Dict[str, Any]]:
    """
    Finds circular multi-person skill exchange pods (triads/quads)
    when a direct 2-person swap is not available or to explore creative loops.
    Example 3-way Loop:
    Liam (React) -> Mateo (Spanish) -> Zara (Video Editing) -> Liam!
    """
    user_map = {u["_id"]: u for u in all_users}
    adj, edge_details = build_transfer_graph(all_users)
    root_id = user.get("_id")
    
    if root_id not in adj:
        return []

    # Direct 2-person partners set (so we prioritize group pods of size >= 3)
    direct_partners = set()
    for neighbor in adj.get(root_id, []):
        if root_id in adj.get(neighbor, []):
            direct_partners.add(neighbor)

    found_cycles = []

    def dfs(curr_id, path, visited):
        if len(path) > max_cycle_len:
            return

        for next_id in adj.get(curr_id, []):
            if next_id == root_id and len(path) >= 3:
                # Cycle closed!
                found_cycles.append(list(path))
            elif next_id not in visited and len(path) < max_cycle_len:
                visited.add(next_id)
                dfs(next_id, path + [next_id], visited)
                visited.remove(next_id)

    dfs(root_id, [root_id], {root_id})

    # Deduplicate and format pods
    formatted_pods = []
    seen_sig = set()

    for cycle in found_cycles:
        # Signature to avoid identical cycles
        sig = tuple(cycle)
        if sig in seen_sig:
            continue
        seen_sig.add(sig)

        members = [user_map[uid] for uid in cycle]
        steps = []
        n = len(cycle)
        
        # Calculate shared days across the pod
        common_days = set(members[0].get("availability", {}).get("days", []))
        for m in members[1:]:
            common_days = common_days.intersection(set(m.get("availability", {}).get("days", [])))

        total_karma = sum(m.get("karma_points", 100) for m in members)
        avg_rating = round(sum(m.get("rating", 4.5) for m in members) / n, 2)

        for i in range(n):
            sender_id = cycle[i]
            receiver_id = cycle[(i + 1) % n]
            edge_info = edge_details.get((sender_id, receiver_id), {
                "skill_name": "Specialized Skill",
                "level": "Intermediate"
            })
            steps.append({
                "step_num": i + 1,
                "teacher": user_map[sender_id],
                "student": user_map[receiver_id],
                "skill_name": edge_info.get("skill_name"),
                "level": edge_info.get("level")
            })

        # Base pod score
        pod_score = 88 if len(cycle) == 3 else 82
        if common_days:
            pod_score += 6
        if avg_rating >= 4.8:
            pod_score += 4

        formatted_pods.append({
            "pod_id": f"pod_{'_'.join([uid.replace('user_', '') for uid in cycle])}",
            "size": n,
            "type_name": f"{n}-Way Synergy Pod" if n > 3 else "Triangular Skill Pod",
            "members": members,
            "steps": steps,
            "common_days": list(common_days),
            "avg_rating": avg_rating,
            "pod_score": min(pod_score, 98),
            "description": " -> ".join([m["name"] for m in members] + [members[0]["name"]])
        })

    # Sort descending by pod score
    formatted_pods.sort(key=lambda p: p["pod_score"], reverse=True)
    return formatted_pods

def get_knowledge_network_data(all_users: List[dict], active_exchanges: List[dict] = None) -> dict:
    """
    Transforms campus users, their offered/wanted skills, and active exchanges
    into nodes & edges ready for Vis.js Network visualization.
    """
    if active_exchanges is None:
        active_exchanges = []

    nodes = []
    edges = []
    
    category_colors = {
        "Programming": "#38bdf8",       # Sky
        "Software Engineering": "#60a5fa", # Blue
        "Design": "#f472b6",            # Pink
        "Creative Tech": "#c084fc",     # Purple
        "Media": "#fb923c",             # Orange
        "Languages": "#34d399",         # Emerald
        "Academics": "#a78bfa",         # Violet
        "Communication": "#facc15",     # Amber
        "Music & Audio": "#e879f9",     # Fuchsia
        "Business": "#2dd4bf"           # Teal
    }

    # 1. Add User Nodes
    for u in all_users:
        u_id = u["_id"]
        nodes.append({
            "id": u_id,
            "label": u["name"],
            "group": "user",
            "department": u.get("department", "Student"),
            "avatar": u.get("avatar", ""),
            "shape": "circularImage",
            "image": u.get("avatar", ""),
            "title": f"<b>{u['name']}</b><br>{u.get('department')}<br>Points: {u.get('karma_points', 0)} pts<br>Rating: ⭐ {u.get('rating', 5.0)}",
            "value": 25 + len(u.get("skills_offered", [])) * 5,
            "borderWidth": 3,
            "color": {
                "border": "#0f172a",
                "background": "#ffffff",
                "highlight": {
                    "border": "#0f172a",
                    "background": "#fef08a"
                }
            },
            "font": {
                "color": "#0f172a",
                "size": 13,
                "face": "Plus Jakarta Sans, sans-serif"
            }
        })

    # 2. Add Skill Nodes & Connect to Users
    skill_seen = set()
    for u in all_users:
        u_id = u["_id"]

        # Skills Offered (u --teaches--> skill)
        for off in u.get("skills_offered", []):
            s_name = off.get("name", "")
            cat = off.get("category", "General")
            s_id = f"skill_{normalize_text(s_name).replace(' ', '_')}"

            if s_id not in skill_seen:
                skill_seen.add(s_id)
                nodes.append({
                    "id": s_id,
                    "label": s_name,
                    "group": "skill",
                    "category": cat,
                    "shape": "dot",
                    "size": 16,
                    "title": f"<b>Skill: {s_name}</b><br>Category: {cat}",
                    "color": {
                        "background": category_colors.get(cat, "#38bdf8"),
                        "border": "#ffffff"
                    },
                    "font": {
                        "color": "#0f172a",
                        "size": 12,
                        "face": "Plus Jakarta Sans, sans-serif"
                    }
                })

            edges.append({
                "from": u_id,
                "to": s_id,
                "arrows": "to",
                "label": f"Teaches ({off.get('level', 'Exp')})",
                "color": {"color": "#10b981", "opacity": 0.7},
                "dashes": False,
                "width": 2,
                "font": {"size": 9, "color": "#10b981", "align": "middle"}
            })

        # Skills Wanted (u --wants--> skill)
        for wnt in u.get("skills_wanted", []):
            s_name = wnt.get("name", "")
            cat = wnt.get("category", "General")
            s_id = f"skill_{normalize_text(s_name).replace(' ', '_')}"

            if s_id not in skill_seen:
                skill_seen.add(s_id)
                nodes.append({
                    "id": s_id,
                    "label": s_name,
                    "group": "skill",
                    "category": cat,
                    "shape": "dot",
                    "size": 14,
                    "title": f"<b>Skill: {s_name}</b><br>Category: {cat}",
                    "color": {
                        "background": category_colors.get(cat, "#a855f7"),
                        "border": "#ffffff"
                    },
                    "font": {
                        "color": "#e2e8f0",
                        "size": 12
                    }
                })

            edges.append({
                "from": u_id,
                "to": s_id,
                "arrows": "to",
                "label": "Wants",
                "color": {"color": "#a855f7", "opacity": 0.6},
                "dashes": True,
                "width": 1.5,
                "font": {"size": 9, "color": "#c084fc", "align": "middle"}
            })

    # 3. Active Exchange Edges (Glowing gold double edges between users)
    for ex in active_exchanges:
        parts = ex.get("participants", [])
        if len(parts) == 2:
            edges.append({
                "from": parts[0],
                "to": parts[1],
                "arrows": "to, from",
                "label": "Active Swap",
                "color": {"color": "#f59e0b", "opacity": 0.95},
                "width": 3.5,
                "dashes": [6, 4],
                "font": {"size": 11, "color": "#fbbf24", "bold": True}
            })
        elif len(parts) >= 3:
            # Multi-person loop active swap
            n = len(parts)
            for i in range(n):
                edges.append({
                    "from": parts[i],
                    "to": parts[(i + 1) % n],
                    "arrows": "to",
                    "label": "Pod Member",
                    "color": {"color": "#ec4899", "opacity": 0.9},
                    "width": 3,
                    "dashes": [4, 4],
                    "font": {"size": 10, "color": "#f472b6"}
                })

    return {
        "nodes": nodes,
        "edges": edges,
        "categories": list(category_colors.keys())
    }
