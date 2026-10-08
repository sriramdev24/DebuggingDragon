"""
Seed data for SkillSwap DNA Social Network.
Provides realistic campus profiles with complementary skills, social feeds,
stories, direct messaging threads, and multi-person circular exchange loops.
"""

INITIAL_USERS = [
    {
        "_id": "user_alex",
        "name": "Alex Chen",
        "handle": "@alex_chen",
        "email": "alex.chen@campus.edu",
        "department": "Computer Science",
        "year": "Junior (3rd Year)",
        "bio": "Building AI tools and backend systems. Passionate about machine learning but leveling up my design and visual thinking skills for hackathons.",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_1",
                "name": "Python & Data Science",
                "category": "Programming",
                "level": "Advanced",
                "experience": "3 years (Built ML pipelines, Pandas, PyTorch)",
                "endorsements": 8
            },
            {
                "id": "so_2",
                "name": "API & Backend Architecture",
                "category": "Software Engineering",
                "level": "Intermediate",
                "experience": "2 years with Flask & FastAPI",
                "endorsements": 5
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_1",
                "name": "UI/UX Design & Figma",
                "category": "Design",
                "target_level": "Intermediate",
                "goal": "Design clean web dashboards and intuitive mobile interfaces without struggling."
            },
            {
                "id": "sw_2",
                "name": "Product Prototyping",
                "category": "Design",
                "target_level": "Beginner",
                "goal": "Learn how to build clickable high-fidelity prototypes."
            }
        ],
        "availability": {
            "days": ["Monday", "Wednesday", "Saturday"],
            "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
            "format": "Hybrid (Campus Library or Discord)",
            "hours_per_week": 4
        },
        "karma_points": 140,
        "completed_swaps": 6,
        "rating": 4.9,
        "followers": ["user_maya", "user_liam", "user_elena"],
        "following": ["user_maya", "user_zara"]
    },
    {
        "_id": "user_maya",
        "name": "Maya Lin",
        "handle": "@mayadesigns",
        "email": "maya.lin@campus.edu",
        "department": "Digital Media & Design",
        "year": "Sophomore (2nd Year)",
        "bio": "Visual designer, Figma nerd and typography enthusiast. I create micro-interactions and design systems, eager to learn Python for design automation.",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_3",
                "name": "UI/UX Design & Figma",
                "category": "Design",
                "level": "Advanced",
                "experience": "3 years (Design systems, Wireframing, Auto-layout)",
                "endorsements": 12
            },
            {
                "id": "so_4",
                "name": "Brand Identity & Vector Art",
                "category": "Design",
                "level": "Intermediate",
                "experience": "Freelance logo & brand kit designer",
                "endorsements": 7
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_3",
                "name": "Python & Data Science",
                "category": "Programming",
                "target_level": "Beginner",
                "goal": "Automate data scraping for generative design research and scripts."
            },
            {
                "id": "sw_4",
                "name": "Creative Coding (p5.js)",
                "category": "Creative Tech",
                "target_level": "Intermediate",
                "goal": "Bring interactive generative art to web browsers."
            }
        ],
        "availability": {
            "days": ["Monday", "Wednesday", "Thursday"],
            "slots": ["Evening (6 PM - 8 PM)", "Morning (10 AM - 12 PM)"],
            "format": "Hybrid (Design Lab or Zoom)",
            "hours_per_week": 5
        },
        "karma_points": 195,
        "completed_swaps": 9,
        "rating": 5.0,
        "followers": ["user_alex", "user_zara", "user_mateo"],
        "following": ["user_alex", "user_liam"]
    },
    {
        "_id": "user_liam",
        "name": "Liam Patel",
        "handle": "@liamdev",
        "email": "liam.patel@campus.edu",
        "department": "Software Engineering",
        "year": "Senior (4th Year)",
        "bio": "Fullstack web developer specializing in React and Node.js. Need help editing high-impact video reels and tech demos for my startup pitch.",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_5",
                "name": "Fullstack Web Dev (React & Node)",
                "category": "Programming",
                "level": "Advanced",
                "experience": "4 years building full stack web apps",
                "endorsements": 15
            },
            {
                "id": "so_6",
                "name": "Git & CI/CD DevOps",
                "category": "Software Engineering",
                "level": "Intermediate",
                "experience": "Docker, GitHub Actions, Vercel",
                "endorsements": 6
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_5",
                "name": "Video Editing & Motion Graphics",
                "category": "Media",
                "target_level": "Beginner",
                "goal": "Create engaging 60-second product demo videos in Premiere / After Effects."
            }
        ],
        "availability": {
            "days": ["Tuesday", "Thursday", "Sunday"],
            "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
            "format": "In-Person (Student Union Hub)",
            "hours_per_week": 3
        },
        "karma_points": 120,
        "completed_swaps": 5,
        "rating": 4.8,
        "followers": ["user_zara", "user_mateo"],
        "following": ["user_zara", "user_mateo"]
    },
    {
        "_id": "user_zara",
        "name": "Zara Khan",
        "handle": "@zara_cuts",
        "email": "zara.khan@campus.edu",
        "department": "Film & Digital Arts",
        "year": "Junior (3rd Year)",
        "bio": "Motion graphics artist and Premiere Pro wizard. Looking for conversational Spanish lessons before my semester study abroad in Madrid!",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_7",
                "name": "Video Editing & Motion Graphics",
                "category": "Media",
                "level": "Advanced",
                "experience": "After Effects, Premiere Pro, color grading, pacing",
                "endorsements": 11
            },
            {
                "id": "so_8",
                "name": "Sound Design & Foley",
                "category": "Media",
                "level": "Intermediate",
                "experience": "Audio sync, Audition, podcast editing",
                "endorsements": 4
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_6",
                "name": "Spanish Language & Conversation",
                "category": "Languages",
                "target_level": "Intermediate",
                "goal": "Everyday fluent spoken Spanish for semester abroad in Spain."
            }
        ],
        "availability": {
            "days": ["Tuesday", "Thursday", "Saturday"],
            "slots": ["Evening (6 PM - 8 PM)", "Morning (10 AM - 12 PM)"],
            "format": "Hybrid",
            "hours_per_week": 4
        },
        "karma_points": 160,
        "completed_swaps": 7,
        "rating": 4.9,
        "followers": ["user_mateo", "user_liam"],
        "following": ["user_mateo", "user_liam"]
    },
    {
        "_id": "user_mateo",
        "name": "Mateo Hernandez",
        "handle": "@mateo_habla",
        "email": "mateo.h@campus.edu",
        "department": "International Relations & Linguistics",
        "year": "Junior (3rd Year)",
        "bio": "Native Spanish speaker and literature buff. Want to learn modern web development so I can publish an interactive online poetry archive.",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_9",
                "name": "Spanish Language & Conversation",
                "category": "Languages",
                "level": "Advanced",
                "experience": "Native speaker, experienced language partner & tutor",
                "endorsements": 14
            },
            {
                "id": "so_10",
                "name": "Academic Writing & Essay Polish",
                "category": "Academics",
                "level": "Advanced",
                "experience": "Writing center peer mentor",
                "endorsements": 9
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_7",
                "name": "Fullstack Web Dev (React & Node)",
                "category": "Programming",
                "target_level": "Beginner",
                "goal": "Understand React components, state, and host my web portfolio."
            }
        ],
        "availability": {
            "days": ["Tuesday", "Thursday", "Sunday"],
            "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
            "format": "In-Person (Campus Cafe)",
            "hours_per_week": 4
        },
        "karma_points": 175,
        "completed_swaps": 8,
        "rating": 5.0,
        "followers": ["user_zara", "user_liam"],
        "following": ["user_zara", "user_liam"]
    },
    {
        "_id": "user_elena",
        "name": "Elena Rostova",
        "handle": "@elena_codes",
        "email": "elena.r@campus.edu",
        "department": "Computer Science & Math",
        "year": "Sophomore (2nd Year)",
        "bio": "Competitive programmer. LeetCode 2100+. Looking for public speaking coaching to overcome stage fright during hackathon pitches.",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_11",
                "name": "Data Structures & Algorithms",
                "category": "Programming",
                "level": "Advanced",
                "experience": "Competitive programming (LeetCode 2100+)",
                "endorsements": 16
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_8",
                "name": "Public Speaking & Pitching",
                "category": "Communication",
                "target_level": "Beginner",
                "goal": "Speak confidently without anxiety during hackathon demos and interviews."
            }
        ],
        "availability": {
            "days": ["Monday", "Friday", "Sunday"],
            "slots": ["Afternoon (2 PM - 4 PM)", "Evening (6 PM - 8 PM)"],
            "format": "Online / Discord",
            "hours_per_week": 3
        },
        "karma_points": 110,
        "completed_swaps": 4,
        "rating": 4.7,
        "followers": ["user_alex"],
        "following": ["user_kai"]
    },
    {
        "_id": "user_marcus",
        "name": "Marcus Vance",
        "handle": "@marcus_speaks",
        "email": "marcus.v@campus.edu",
        "department": "Business & Communications",
        "year": "Senior (4th Year)",
        "bio": "Varsity debate captain and TEDx youth speaker. Coaching presentation presence. Learning electronic music production in Ableton Live.",
        "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_13",
                "name": "Public Speaking & Pitching",
                "category": "Communication",
                "level": "Advanced",
                "experience": "Varsity debate captain, delivered TEDx youth talk",
                "endorsements": 18
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_9",
                "name": "Music Production & Ableton",
                "category": "Music & Audio",
                "target_level": "Beginner",
                "goal": "Produce electronic music tracks, beats, and master EQ/compression."
            }
        ],
        "availability": {
            "days": ["Friday", "Saturday", "Sunday"],
            "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
            "format": "Hybrid",
            "hours_per_week": 4
        },
        "karma_points": 210,
        "completed_swaps": 11,
        "rating": 4.95,
        "followers": ["user_kai"],
        "following": ["user_elena"]
    },
    {
        "_id": "user_kai",
        "name": "Kai Takahashi",
        "handle": "@kai_beats",
        "email": "kai.t@campus.edu",
        "department": "Music Technology & Audio",
        "year": "Junior (3rd Year)",
        "bio": "Electronic music producer and audio technician. Prepping for technical coding interviews for audio DSP internships.",
        "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80",
        "cover_photo": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1000&auto=format&fit=crop&q=80",
        "skills_offered": [
            {
                "id": "so_15",
                "name": "Music Production & Ableton",
                "category": "Music & Audio",
                "level": "Advanced",
                "experience": "4 years mixing, synthesis, sound design, MIDI",
                "endorsements": 13
            }
        ],
        "skills_wanted": [
            {
                "id": "sw_10",
                "name": "Data Structures & Algorithms",
                "category": "Programming",
                "target_level": "Intermediate",
                "goal": "Master trees, binary search, and dynamic programming for audio coding exams."
            }
        ],
        "availability": {
            "days": ["Monday", "Friday", "Sunday"],
            "slots": ["Evening (6 PM - 8 PM)", "Afternoon (2 PM - 4 PM)"],
            "format": "In-Person (Studio B)",
            "hours_per_week": 3
        },
        "karma_points": 135,
        "completed_swaps": 5,
        "rating": 4.9,
        "followers": ["user_marcus"],
        "following": ["user_marcus"]
    }
]

INITIAL_POSTS = [
    {
        "_id": "post_1",
        "author_id": "user_alex",
        "content": "Just completed Session #2 with @mayadesigns! 🚀 We built a Python script that automatically exports Figma design tokens into clean CSS variables. Here is the prototype preview. Zero dollars spent, pure peer barter!",
        "skill_tag": "Python & Data Science",
        "post_type": "showcase",
        "image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80",
        "likes": ["user_maya", "user_liam", "user_zara", "user_elena"],
        "comments": [
            {
                "id": "c_1",
                "user_id": "user_maya",
                "text": "Such a fun session! Next Wednesday we're diving into auto-layout flex grids and component variants 🔥",
                "created_at": "2 hours ago"
            },
            {
                "id": "c_2",
                "user_id": "user_liam",
                "text": "Need this script for my React app! Would love to trade for some Docker/CI tips.",
                "created_at": "1 hour ago"
            }
        ],
        "created_at": "3 hours ago"
    },
    {
        "_id": "post_2",
        "author_id": "user_maya",
        "content": "🎨 Quick UI Tip: Never use pure black (#000000) for body text on dark mode! Use #0f172a or #1e293b with slight opacity for softer eye strain. Free tomorrow at Design Lab 204 if anyone wants a live Figma walkthrough in exchange for Python data scraping!",
        "skill_tag": "UI/UX Design & Figma",
        "post_type": "swap_request",
        "image": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop&q=80",
        "likes": ["user_alex", "user_mateo", "user_marcus"],
        "comments": [
            {
                "id": "c_3",
                "user_id": "user_alex",
                "text": "Already taking notes! Let's cover Beautiful Soup and JSON scraping on Friday.",
                "created_at": "45 mins ago"
            }
        ],
        "created_at": "5 hours ago"
    },
    {
        "_id": "post_3",
        "author_id": "user_liam",
        "content": "Huge shoutout to the Circular Pod matching engine! 🔄 Because of SkillSwap DNA, @liamdev ➔ @mateo_habla ➔ @zara_cuts ➔ @liamdev formed a 3-way knowledge loop. Mateo taught Spanish, Zara taught Premiere Pro motion cuts, and I'm teaching React. Circular exchanges are changing how our campus learns!",
        "skill_tag": "Fullstack Web Dev (React & Node)",
        "post_type": "milestone",
        "image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&auto=format&fit=crop&q=80",
        "likes": ["user_zara", "user_mateo", "user_alex", "user_elena", "user_kai"],
        "comments": [
            {
                "id": "c_4",
                "user_id": "user_zara",
                "text": "Best learning format ever. Mateo is a fantastic Spanish tutor!",
                "created_at": "3 hours ago"
            },
            {
                "id": "c_5",
                "user_id": "user_mateo",
                "text": "¡Totalmente! Building my React poetry portfolio step by step.",
                "created_at": "2 hours ago"
            }
        ],
        "created_at": "8 hours ago"
    },
    {
        "_id": "post_4",
        "author_id": "user_elena",
        "content": "Solved LeetCode 2100+ dynamic programming problem with bitmasking today! 💡 Still get anxious speaking in front of people though. Who wants to do mock hackathon demo pitches in exchange for binary tree & graph tutoring?",
        "skill_tag": "Data Structures & Algorithms",
        "post_type": "swap_request",
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop&q=80",
        "likes": ["user_marcus", "user_kai", "user_alex"],
        "comments": [
            {
                "id": "c_6",
                "user_id": "user_marcus",
                "text": "I'm your person, Elena! Varsity debate captain here. Let's do a session this Sunday.",
                "created_at": "1 hour ago"
            }
        ],
        "created_at": "12 hours ago"
    }
]

INITIAL_STORIES = [
    {
        "_id": "story_alex",
        "user_id": "user_alex",
        "text": "Free 6-8 PM today for Python or Backend tips in library!",
        "skill_tag": "Python",
        "gradient": "from-indigo-600 to-pink-500"
    },
    {
        "_id": "story_maya",
        "user_id": "user_maya",
        "text": "Reviewing Figma portfolio designs at Design Hub 🎨",
        "skill_tag": "UI/UX",
        "gradient": "from-pink-500 to-amber-500"
    },
    {
        "_id": "story_zara",
        "user_id": "user_zara",
        "text": "Rendering After Effects reels. Need 30min Spanish chat! 🇪🇸",
        "skill_tag": "Spanish",
        "gradient": "from-emerald-500 to-teal-600"
    },
    {
        "_id": "story_kai",
        "user_id": "user_kai",
        "text": "Studio B open for Ableton synthesizers & drum mixing 🎛️",
        "skill_tag": "Ableton",
        "gradient": "from-purple-600 to-indigo-600"
    },
    {
        "_id": "story_mateo",
        "user_id": "user_mateo",
        "text": "Just launched my first React counter component! 🎉",
        "skill_tag": "React",
        "gradient": "from-sky-500 to-blue-600"
    }
]

INITIAL_MESSAGES = [
    {
        "_id": "msg_1",
        "sender_id": "user_maya",
        "receiver_id": "user_alex",
        "text": "Hey Alex! Loved our session on dictionaries and JSON serialization.",
        "created_at": "Yesterday at 4:15 PM"
    },
    {
        "_id": "msg_2",
        "sender_id": "user_alex",
        "receiver_id": "user_maya",
        "text": "Thanks Maya! Your auto-layout tips completely fixed my responsive cards. Are we still on for Wednesday 6:30 PM?",
        "created_at": "Yesterday at 4:18 PM"
    },
    {
        "_id": "msg_3",
        "sender_id": "user_maya",
        "receiver_id": "user_alex",
        "text": "Yes! Design Lab 204. I'll bring the interactive prototype files.",
        "created_at": "Yesterday at 4:20 PM"
    },
    {
        "_id": "msg_4",
        "sender_id": "user_liam",
        "receiver_id": "user_alex",
        "text": "Hey Alex, saw your post on Figma token scripts. Would love to swap for React fullstack tips!",
        "created_at": "Today at 9:30 AM"
    }
]

INITIAL_EXCHANGES = [
    {
        "_id": "exch_1",
        "type": "direct",
        "participants": ["user_alex", "user_maya"],
        "initiator_id": "user_alex",
        "recipient_id": "user_maya",
        "initiator_offers": "Python & Data Science",
        "recipient_offers": "UI/UX Design & Figma",
        "status": "active",
        "scheduled_time": "Every Wednesday 6:30 PM",
        "location": "Design Lab 204 & Discord",
        "created_at": "2026-09-28T14:00:00",
        "total_sessions": 3,
        "completed_sessions": 2,
        "notes": "Session 1: Figma auto-layout mastered. Session 2: Python script for Figma color token automation.",
        "reviews": [
            {
                "from_user": "user_maya",
                "to_user": "user_alex",
                "rating": 5,
                "comment": "Alex is super patient! He broke down Python dictionaries so clearly.",
                "date": "2026-10-02"
            }
        ]
    },
    {
        "_id": "exch_2",
        "type": "pod",
        "pod_name": "Web & Media Triad",
        "participants": ["user_liam", "user_zara", "user_mateo"],
        "initiator_id": "user_liam",
        "loop_description": "Liam (React) -> Mateo (Spanish) -> Zara (Motion Graphics) -> Liam",
        "status": "scheduled",
        "scheduled_time": "Tuesdays & Thursdays 7:00 PM",
        "location": "Campus Innovation Center - Pod 3",
        "created_at": "2026-10-01T16:30:00",
        "total_sessions": 3,
        "completed_sessions": 1,
        "notes": "First kick-off session completed! Mateo taught conversational Spanish basics to Zara.",
        "reviews": []
    }
]
