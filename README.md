# 🧬 SkillSwap DNA — Campus Social Skill Barter Network

> **A Full-Fledged Social Media Application for Skill Exchanges & Peer Learning**  
> Connect with campus peers, share learning milestones, post 24-hour skill radar stories, direct-message matched partners, and trade practical skills without spending money.

---

## 🌟 The Problem & The Solution

* **The Challenge:** Many students want to learn practical skills but cannot afford expensive bootcamps or find suitable mentors. At the same time, peers have valuable skills they would gladly teach if someone could teach them what they need in return.
* **SkillSwap DNA Social Platform:** Instead of a boring directory of tutors, SkillSwap DNA builds a vibrant **social media platform**:
  * **Campus Social Feed:** Share skill showcases, learning milestones, and barter shoutouts with likes, comments, and tags.
  * **24h Skill Radar Stories:** Post ephemeral availability updates (e.g., *"Free 6–8 PM in library to mentor Python!"*).
  * **Direct Peer Messaging (DMs):** Coordinate swap times, Discord links, and study rooms with matched partners.
  * **Social Peer Profiles:** Follow peers, view follower counts, and review peer endorsements.
  * **Direct 2-Person Swaps:** Student A knows Python and wants UI Design. Student B knows UI Design and wants Python &rarr; **Direct Reciprocal Match!**
  * **The Unconventional Breakthrough (Circular Group Pods):** When a direct 1-to-1 match does not exist, our engine discovers closed 3-way circular knowledge loops:
    $$\text{Liam (React)} \longrightarrow \text{Mateo (Spanish)} \longrightarrow \text{Zara (Video)} \longrightarrow \text{Liam}$$
    Everyone gives 1 skill and gets 1 skill without any tuition fees or money.

---

## 🚀 Key Features

1. **Skill Profiles with Levels:**
   - Categorized skills with 3 proficiency tiers: `Beginner`, `Intermediate`, and `Advanced`.
   - Experience notes, endorsements, and domain categorization (Programming, Design, Languages, Media, Music & Audio, Academics, Communication, Business).
2. **Skills Offered & Skills Wanted:**
   - Registered skills to teach vs. target learning goals.
   - DNA skill tags and portfolio/experience context.
3. **Reciprocal Compatibility Matching Engine:**
   - Weighted DNA compatibility scoring ($50\% \text{ Reciprocal Fit} + 25\% \text{ Level Synergy} + 25\% \text{ Schedule Overlap}$).
   - Schedule intersection matching across days and morning/afternoon/evening time slots.
4. **Group Formation (Circular Exchange Pods):**
   - Directed knowledge graph cycle detection (DFS with backtracking).
   - Automatically detects 3-person and 4-person knowledge transfer pods when bilateral matching isn't possible.
   - Collective rating and shared availability calculation.
5. **Exchange Requests, Availability & Session Completion:**
   - Propose, accept, or decline swap requests.
   - Progress meter for multi-session milestones.
   - Session completion tracking that awards **+20 Karma Points** to each participant upon verified completion.
   - Peer ratings (1–5 stars) and mutual feedback endorsements.
6. **Campus Knowledge Network Graph:**
   - Interactive Vis.js network visualization.
   - Nodes for students and indexed skills.
   - Directional knowledge transfer arrows (green = teaches, purple = wants, gold = active barter).
   - Domain filtering, keyword search, physics controls, and slide-out node inspector drawer.
7. **Instant Student Identity Switcher:**
   - Quickly switch between pre-seeded campus students (e.g. *Alex Chen*, *Maya Lin*, *Liam Patel*, *Zara Khan*, *Mateo Hernandez*, *Elena Rostova*, etc.) to test reciprocal matches and circular pod interactions from any perspective.

---

## 🛠️ Technology Stack

- **Backend:** Python 3 (Flask)
- **Database:** MongoDB Cloud (Atlas) via `pymongo` and `dnspython` (with automated fallback to `mongomock` with realistic pre-seeded campus profiles if no Atlas URI is provided)
- **Frontend / UI:** Jinja2 Templates, Tailwind CSS (modern dark drizzle-ui glassmorphism), Lucide Icons
- **Network Graph:** Vis.js Network Engine (force-directed graph physics)

---

## ⚡ Quick Start

### 1. Requirements
Ensure you have Python installed. The required dependencies are:
```bash
py -m pip install -r requirements.txt
```

### 2. Configure Database (Optional for Cloud Atlas)
Open `.env` (or copy `.env.example` to `.env`):
```env
# Optional: To connect to MongoDB Atlas Cloud, paste your URI:
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xyz.mongodb.net/skillswap_dna?retryWrites=true&w=majority
DB_NAME=skillswap_dna
SECRET_KEY=skillswap-dna-secret-superkey-2026
PORT=5000
```
> *Note: If `MONGO_URI` is left blank, SkillSwap DNA runs seamlessly using its in-memory pre-seeded mock database.*

### 3. Run the Application
```bash
py app.py
```
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📁 Project Structure

```
g:/skilldna/
├── app.py                     # Main Flask application, routes, mutations & APIs
├── config.py                  # Environment & App configuration loader
├── db.py                      # MongoDB Cloud Atlas client & fallback mock handler
├── matcher.py                 # Core matching algorithms (2-person & circular DFS)
├── seed_data.py               # Pre-seeded campus students, skills, and swaps
├── requirements.txt           # Python dependencies
├── .env.example               # Atlas configuration template
├── .env                       # Local environment variables
├── static/
│   ├── css/
│   │   └── custom.css         # Drizzle design system, glassmorphism, animations
│   └── js/
│       └── network_graph.js   # Vis.js interactive graph, search & inspector drawer
└── templates/
    ├── base.html              # Sticky navbar, user switcher, MongoDB status badge
    ├── index.html             # Dashboard, campus pulse metrics, top matches preview
    ├── matches.html           # Dual-Engine: 2-way matches & circular group pods
    ├── network.html           # Campus Knowledge Graph interactive view
    ├── directory.html         # Peer directory with filters for level & category
    ├── exchanges.html         # Sessions tracker, schedule updates, ratings & reviews
    └── profile.html           # Skill DNA editor for offered/wanted skills & schedule
```
