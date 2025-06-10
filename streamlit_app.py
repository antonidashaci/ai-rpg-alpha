import streamlit as st
import requests
import json
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="AI-RPG-Alpha",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for RPG styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #d4af37;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .scenario-card {
        border: 2px solid #d4af37;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #2c1810, #3d2817);
    }
    .narrative-box {
        background: #1e1e1e;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 1.5rem;
        font-size: 1.1rem;
        line-height: 1.6;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    .choice-button {
        background: #2c1810;
        border: 2px solid #d4af37;
        color: #d4af37;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .choice-button:hover {
        background: #d4af37;
        color: #2c1810;
    }
    .stat-box {
        background: #2a2a2a;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'player_name': '',
        'selected_scenario': None,
        'current_narrative': '',
        'choices': [],
        'turn_number': 0,
        'player_stats': {
            'level': 1,
            'health': 100,
            'mana': 50,
            'stamina': 100,
            'action_points': 2
        }
    }

def make_api_call(endpoint: str, data: Dict) -> Dict:
    """Make API call to backend server"""
    try:
        response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def scenario_selection():
    """Scenario selection interface"""
    st.markdown('<h1 class="main-header">⚔️ AI-RPG-Alpha ⚔️</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #888;">Choose Your Adventure</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="scenario-card">
            <h3 style="color: #d4af37;">🏰 The Northern Realms</h3>
            <p style="color: #888;">Epic Fantasy</p>
            <p>Ancient dragons stir in forgotten mountain peaks. Magic flows through mystical ley lines, and kingdoms rise and fall by the strength of heroes.</p>
            <ul style="color: #666;">
                <li>⚔️ Epic Battles</li>
                <li>🏰 Political Intrigue</li>
                <li>🔮 Ancient Magic</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏰 Begin Epic Quest", key="northern", use_container_width=True):
            st.session_state.game_state['selected_scenario'] = 'northern_realms'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="scenario-card">
            <h3 style="color: #d4af37;">🌊 The Whispering Town</h3>
            <p style="color: #888;">Cosmic Horror</p>
            <div style="background: #4a148c; padding: 0.3rem; border-radius: 20px; text-align: center; margin-bottom: 1rem;">
                <strong>RECOMMENDED</strong>
            </div>
            <p>Reality grows thin in this forgotten New England town. Ancient whispers carry forbidden knowledge, and your sanity hangs by a thread.</p>
            <ul style="color: #666;">
                <li>🧠 Sanity System</li>
                <li>👁️ Cosmic Knowledge</li>
                <li>🌊 Reality Distortion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌊 Enter the Unknown", key="whispering", use_container_width=True):
            st.session_state.game_state['selected_scenario'] = 'whispering_town'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="scenario-card">
            <h3 style="color: #d4af37;">🌃 Neo-Tokyo 2087</h3>
            <p style="color: #888;">Cyberpunk Dystopia</p>
            <p>Neon lights pierce through acid rain as corporate overlords control humanity's digital souls. In this chrome-plated nightmare, information is power.</p>
            <ul style="color: #666;">
                <li>🤖 Cybernetics</li>
                <li>💾 Data Warfare</li>
                <li>🏙️ Urban Decay</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌃 Jack In", key="neo_tokyo", use_container_width=True):
            st.session_state.game_state['selected_scenario'] = 'neo_tokyo'
            st.rerun()

def player_setup():
    """Player name input"""
    st.markdown('<h2 style="text-align: center; color: #d4af37;">Enter Your Name</h2>', unsafe_allow_html=True)
    
    scenario_names = {
        'northern_realms': '🏰 The Northern Realms',
        'whispering_town': '🌊 The Whispering Town', 
        'neo_tokyo': '🌃 Neo-Tokyo 2087'
    }
    
    selected = st.session_state.game_state['selected_scenario']
    st.info(f"Selected Scenario: {scenario_names[selected]}")
    
    player_name = st.text_input("Character Name:", placeholder="Enter your hero's name...")
    
    if st.button("🎮 Begin Adventure", use_container_width=True) and player_name:
        st.session_state.game_state['player_name'] = player_name
        
        # Make first API call
        response = make_api_call('/turn', {
            'player_name': player_name,
            'choice': 'Begin my adventure',
            'scenario': selected
        })
        
        if response:
            st.session_state.game_state['current_narrative'] = response.get('narrative', '')
            st.session_state.game_state['choices'] = response.get('choices', [])
            st.session_state.game_state['turn_number'] = 1
            st.rerun()

def game_interface():
    """Main game interface"""
    # Sidebar with player info
    with st.sidebar:
        st.markdown("### 👤 Player Info")
        st.markdown(f"**Name:** {st.session_state.game_state['player_name']}")
        
        # Scenario info
        scenario_names = {
            'northern_realms': '🏰 The Northern Realms',
            'whispering_town': '🌊 The Whispering Town', 
            'neo_tokyo': '🌃 Neo-Tokyo 2087'
        }
        selected = st.session_state.game_state['selected_scenario']
        st.markdown(f"**Scenario:** {scenario_names[selected]}")
        
        st.markdown("### 📊 Stats")
        stats = st.session_state.game_state['player_stats']
        
        # Health bar
        health_percent = stats['health'] / 100
        st.markdown(f"**❤️ Health:** {stats['health']}/100")
        st.progress(health_percent)
        
        # Mana bar  
        mana_percent = stats['mana'] / 50
        st.markdown(f"**🔮 Mana:** {stats['mana']}/50")
        st.progress(mana_percent)
        
        # Combat resources
        st.markdown("### ⚔️ Combat Resources")
        st.markdown(f"**⚡ Stamina:** {stats['stamina']}/100")
        st.progress(stats['stamina'] / 100)
        
        st.markdown(f"**🎯 Action Points:** {stats['action_points']}/3")
        
        # Turn counter
        st.markdown("### 🎲 Game Info")
        st.markdown(f"**Turn:** {st.session_state.game_state['turn_number']}")
        
        # New game button
        if st.button("🔄 New Game"):
            st.session_state.game_state = {
                'player_name': '',
                'selected_scenario': None,
                'current_narrative': '',
                'choices': [],
                'turn_number': 0,
                'player_stats': {
                    'level': 1,
                    'health': 100,
                    'mana': 50,
                    'stamina': 100,
                    'action_points': 2
                }
            }
            st.rerun()
    
    # Main content area
    st.markdown('<h1 class="main-header">⚔️ AI-RPG-Alpha ⚔️</h1>', unsafe_allow_html=True)
    
    # Narrative display
    st.markdown("### 📖 Story")
    narrative = st.session_state.game_state['current_narrative']
    if narrative:
        st.markdown(f'<div class="narrative-box">{narrative}</div>', unsafe_allow_html=True)
    
    # Choices
    st.markdown("### 🎯 What do you choose?")
    choices = st.session_state.game_state['choices']
    
    if choices:
        for i, choice in enumerate(choices):
            if st.button(choice, key=f"choice_{i}", use_container_width=True):
                # Make API call for selected choice
                response = make_api_call('/turn', {
                    'player_name': st.session_state.game_state['player_name'],
                    'choice': choice,
                    'scenario': st.session_state.game_state['selected_scenario']
                })
                
                if response:
                    st.session_state.game_state['current_narrative'] = response.get('narrative', '')
                    st.session_state.game_state['choices'] = response.get('choices', [])
                    st.session_state.game_state['turn_number'] += 1
                    st.rerun()
    
    # Custom input
    st.markdown("### ✍️ Custom Action")
    custom_action = st.text_input("Describe your action:", placeholder="What do you want to do?")
    if st.button("Submit Custom Action") and custom_action:
        response = make_api_call('/turn', {
            'player_name': st.session_state.game_state['player_name'],
            'choice': custom_action,
            'scenario': st.session_state.game_state['selected_scenario']
        })
        
        if response:
            st.session_state.game_state['current_narrative'] = response.get('narrative', '')
            st.session_state.game_state['choices'] = response.get('choices', [])
            st.session_state.game_state['turn_number'] += 1
            st.rerun()

# Main app logic
def main():
    # Check game state and show appropriate interface
    if not st.session_state.game_state['selected_scenario']:
        scenario_selection()
    elif not st.session_state.game_state['player_name']:
        player_setup()
    else:
        game_interface()

if __name__ == "__main__":
    main() 