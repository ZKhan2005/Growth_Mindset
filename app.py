import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

# Initialize session state
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = pd.DataFrame(columns=['Date', 'Progress', 'Mood', 'Energy'])
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = set()
if 'daily_quote' not in st.session_state:
    st.session_state.daily_quote = ""
if 'avatar' not in st.session_state:
    st.session_state.avatar = "👩"

# Quotes and challenges
quotes = [
    "Your mind is a powerful thing. When you fill it with positive thoughts, your life will start to change. 🌟",
    "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. 💖",
    "Believe you can and you're halfway there. 🚀",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. 💪",
    "The future belongs to those who believe in the beauty of their dreams. 🌈"
]

challenges = [
    "Learn a new word in a foreign language and use it in a sentence",
    "Do 20 jumping jacks right now!",
    "Write a short story using exactly 50 words",
    "Compliment three people today",
    "Try a new healthy recipe for dinner",
    "Meditate for 5 minutes",
    "Draw a self-portrait without looking at the paper",
    "Learn and practice a new yoga pose"
]

achievements = {
    "Early Bird": "Complete a challenge before 9 AM",
    "Night Owl": "Complete a challenge after 10 PM",
    "Streak Master": "Maintain a 7-day streak",
    "Century Club": "Earn 100 points",
    "Mood Maestro": "Track your mood for 14 consecutive days",
    "Challenge Champion": "Complete 50 challenges"
}

# Functions
def update_points_and_level(points):
    st.session_state.points += points
    st.session_state.level = (st.session_state.points // 100) + 1

def check_achievements():
    if st.session_state.streak >= 7:
        st.session_state.achievements.add("Streak Master")
    if st.session_state.points >= 100:
        st.session_state.achievements.add("Century Club")
    if len(st.session_state.completed_challenges) >= 50:
        st.session_state.achievements.add("Challenge Champion")

# Main app
st.title("🚀 Growth Mindset Challenge")

# Sidebar
with st.sidebar:
    st.markdown(f"### {st.session_state.avatar} Your Stats")
    st.markdown(f"**Level:** {st.session_state.level}")
    st.markdown(f"**Points:** {st.session_state.points}")
    st.markdown(f"**Streak:** {st.session_state.streak} days 🔥")
    
    st.markdown("### Choose Your Avatar")
    avatars = ["👩", "🧑", "👨", "🧙", "🦸", "🦹", "🧚", "🧛", "🧜", "🧝", "🧞", "🧟"]
    cols = st.columns(4)
    for i, avatar in enumerate(avatars):
        if cols[i % 4].button(avatar, key=f"avatar_{i}"):
            st.session_state.avatar = avatar
            st.success(f"Avatar changed to {avatar}")

# Daily quote
if st.session_state.daily_quote == "":
    st.session_state.daily_quote = random.choice(quotes)
st.markdown(f'<p class="quote">{st.session_state.daily_quote}</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Daily Challenge", "📊 Progress Tracker", "🏆 Achievements"])

with tab1:
    st.header("🎯 Daily Challenge")
    challenge = random.choice(challenges)
    st.markdown(f'<p class="big-font">{challenge}</p>', unsafe_allow_html=True)
    if st.button("Complete Challenge"):
        update_points_and_level(10)
        st.session_state.streak += 1
        st.session_state.completed_challenges.append(challenge)
        st.balloons()
        st.success(f"🎉 Challenge completed! You earned 10 points!")
        check_achievements()

with tab2:
    st.header("📊 Progress Tracker")
    progress = st.slider("Rate your progress (0-100)", 0, 100, 50)
    mood = st.select_slider("How's your mood?", options=["😢", "😐", "😊", "😄", "🤩"])
    energy = st.select_slider("Energy level?", options=["🔋", "🔋🔋", "🔋🔋🔋", "🔋🔋🔋🔋", "🔋🔋🔋🔋🔋"])
    
    if st.button("Log Progress"):
        new_data = pd.DataFrame({'Date': [datetime.now()], 'Progress': [progress], 'Mood': [mood], 'Energy': [energy]})
        st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_data], ignore_index=True)
        update_points_and_level(5)
        st.success("Progress logged! You earned 5 points!")
        check_achievements()
    
    if not st.session_state.progress_data.empty:
        fig = px.line(st.session_state.progress_data, x='Date', y='Progress', title='Your Growth Journey')
        st.plotly_chart(fig)

with tab3:
    st.header("🏆 Achievements")
    for achievement, description in achievements.items():
        if achievement in st.session_state.achievements:
            st.markdown(f'<div class="achievement">{achievement}: {description}</div>', unsafe_allow_html=True)
    
    if not st.session_state.achievements:
        st.info("Complete challenges and maintain streaks to unlock achievements!")

# Footer
st.markdown("---")
st.markdown("Remember, every small step counts towards your growth! 🌱")
