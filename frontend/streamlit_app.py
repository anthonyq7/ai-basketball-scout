import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import re
load_dotenv()

st.set_page_config(
    page_title="AI Basketball Scout",
    page_icon="��",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #2b2b2b;
        color: white;
    }
    
    /* Center the header */
    .main .block-container h1 {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Style the selectbox container - centered and reduced width */
    .stSelectbox {
        background-color: #2b2b2b;
        color: white;
        border-radius: 10px;
        padding: 10px;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Style the selectbox dropdown */
    .stSelectbox > div > div {
        background-color: #2b2b2b;
        border: 2px solid #666;
        border-radius: 10px;
        color: white;
    }
    
    /* Style the selectbox options */
    .stSelectbox > div > div > div {
        background-color: #2b2b2b;
        color: white;
    }
    
    /* Style the selectbox when focused */
    .stSelectbox > div > div:focus-within {
        border-color: #1f77b4;
        box-shadow: 0 0 0 2px rgba(31, 119, 180, 0.2);
    }
    
    /* Style the selectbox input field background */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        background-color: #2b2b2b !important;
    }
    
    /* Style the selectbox text input */
    .stSelectbox input {
        background-color: #2b2b2b !important;
        color: white !important;
    }
    
    /* Style the selectbox dropdown options */
    .stSelectbox [role="listbox"] {
        background-color: #2b2b2b !important;
    }
    
    .stSelectbox [role="option"] {
        background-color: #2b2b2b !important;
        color: white !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #404040 !important;
    }
    
    /* Remove the fixed button width and let it be responsive */
    .stButton > button {
        background-color: #ff7f0e;
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin: 20px auto;
    }
    
    .stButton > button:hover {
        background-color: #e65c00;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .player-card {
        background-color: #404040;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        display: flex;
        align-items: center;
    }
    
    .player-info {
        margin-left: 15px;
    }
    
    .scout-report {
        background-color: #404040;
        padding: 20px 80px;
        border-radius: 10px;
        margin: 20px 60px;
        white-space: pre-line;  
        border: 1px solid #666;
        width: calc(100vw - 120px);
        position: relative;
        left: 50%;
        margin-left: calc(-50vw + 60px);
        text-align: left;
        box-sizing: border-box;
        line-height: 1.6;
    }
    
    .scout-report h2 {
        color: #ff7f0e;
        font-size: 24px;
        font-weight: bold;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #ff7f0e;
    }
    
    .scout-report h2:first-child {
        margin-top: 0;
    }
    
    .scout-report p {
        margin: 15px 0;
        text-align: justify;
    }
    
    /* Style for plain text section headers */
    .scout-report {
        color: white;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Style section headers with the section-header class */
    .scout-report .section-header {
        color: #ff7f0e !important;
        font-size: 24px !important;
        font-weight: bold !important;
        margin: 30px 0 15px 0 !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid #ff7f0e !important;
    }
    
    .scout-report-title {
        text-align: center;
        margin: 20px 0 10px 0;
        font-size: 24px;
        font-weight: bold;
        width: 100%;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 14px;
        margin-top: 40px;
    }
    
    /* Hide selectbox when no players */
    .no-players .stSelectbox {
        display: none;
    }
    
    /* Player selection container styling - side by side layout */
    .player-selection-container {
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Align headshot with search bar - accommodate larger image */
    .stImage {
        text-align: center !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 100% !important;
        min-height: 80px !important;  
    }
    
    .stImage > div {
        text-align: center !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .stImage img {
        margin: 0 auto !important;
        display: block !important;
        max-width: 100% !important;  
        height: auto !important;
    }
    
    /* Override any Streamlit column padding */
    .stColumn > div {
        padding: 0 !important;
    }
    
    /* Center any image containers */
    div[data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL")

def get_player_names():
    try:
        response = requests.get(f"{BACKEND_URL}/players/names")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching players: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

def get_player_headshot(player_name, birth_year):
    try:
        response = requests.get(f"{BACKEND_URL}/player-headshot/{player_name}/{birth_year}")
        if response.status_code == 200:
            return response.json().get("headshot_url")
        return None
    except:
        return None

def generate_scout_report(player_name, birth_year):
    try:
        response = requests.get(f"{BACKEND_URL}/generate_report/{player_name}/{birth_year}")
        if response.status_code == 200:
            return response.text
        else:
            return f"Error generating report: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"

def display_player_image(headshot_url):
    if headshot_url:
        try:
            response = requests.get(headshot_url)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                target_width = 180  
                target_height = int((760 * target_width) / 1040)  # Maintain aspect ratio for 1040x760
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

                st.image(image, width=target_width, use_container_width=False)
            else:
                st.write("🏀")  
        except:
            st.write("🏀")  
    else:
        st.write("🏀")  

def create_combined_player_graph(player_name, birth_year):
    """Create one combined matplotlib graph for player stats across years"""
    try:
        response = requests.get(f"{BACKEND_URL}/player/{player_name}", params={"birth_year": birth_year})
        if response.status_code != 200:
            return None

        player_data = response.json()
        if not player_data:
            return None

        years, ppg, apg, rpg, spg, bpg = [], [], [], [], [], []
        for season in player_data:
            if season.get('year') and season.get('points_per_game') is not None:
                years.append(int(season['year']))
                ppg.append(season.get('points_per_game', 0))
                apg.append(season.get('assists_per_game', 0))
                rpg.append(season.get('total_rebounds_per_game', 0))
                spg.append(season.get('steals_per_game', 0))
                bpg.append(season.get('blocks_per_game', 0))

        if not years:
            return None

        years, ppg, apg, rpg, spg, bpg = zip(*sorted(zip(years, ppg, apg, rpg, spg, bpg)))
        plt.style.use('dark_background')

        fig, ax = plt.subplots(figsize=(36, 22))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Plot all five statistics on the same axes with larger elements
        line1 = ax.plot(years, ppg, marker='o', linewidth=7, markersize=24, 
                       color='#ff7f0e', markerfacecolor='#ff7f0e', markeredgecolor='white', 
                       markeredgewidth=4, label='Points Per Game (PPG)')
        
        line2 = ax.plot(years, apg, marker='s', linewidth=7, markersize=24, 
                       color='#1f77b4', markerfacecolor='#1f77b4', markeredgecolor='white', 
                       markeredgewidth=4, label='Assists Per Game (APG)')
        
        line3 = ax.plot(years, rpg, marker='^', linewidth=7, markersize=24, 
                       color='#2ca02c', markerfacecolor='#2ca02c', markeredgecolor='white', 
                       markeredgewidth=4, label='Rebounds Per Game (RPG)')
        
        line4 = ax.plot(years, spg, marker='D', linewidth=7, markersize=24, 
                       color='#d62728', markerfacecolor='#d62728', markeredgecolor='white', 
                       markeredgewidth=4, label='Steals Per Game (SPG)')
        
        line5 = ax.plot(years, bpg, marker='*', linewidth=7, markersize=28, 
                       color='#9467bd', markerfacecolor='#9467bd', markeredgecolor='white', 
                       markeredgewidth=4, label='Blocks Per Game (BPG)')
        
        ax.set_title(f'{player_name} - Performance Trends (2020-2025)', 
                    fontsize=44, fontweight='bold', color='white', pad=60)
        ax.set_xlabel('Season', color='white', fontsize=36, fontweight='bold')
        ax.set_ylabel('Per Game Statistics', color='white', fontsize=36, fontweight='bold')
        
        ax.grid(True, alpha=0.3, color='#888', linewidth=1.5)
        ax.tick_params(colors='white', labelsize=26, width=4, length=16)
        
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(4)
        
        for i, (x, y) in enumerate(zip(years, ppg)):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,35), ha='center', fontsize=20, color='white', 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.6", facecolor='#ff7f0e', alpha=0.95))
        
        for i, (x, y) in enumerate(zip(years, apg)):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,35), ha='center', fontsize=20, color='white', 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.6", facecolor='#1f77b4', alpha=0.95))
        
        for i, (x, y) in enumerate(zip(years, rpg)):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,35), ha='center', fontsize=20, color='white', 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.6", facecolor='#2ca02c', alpha=0.95))
        
        for i, (x, y) in enumerate(zip(years, spg)):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,35), ha='center', fontsize=20, color='white', 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.6", facecolor='#d62728', alpha=0.95))
        
        for i, (x, y) in enumerate(zip(years, bpg)):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,35), ha='center', fontsize=20, color='white', 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.6", facecolor='#9467bd', alpha=0.95))
        
        legend = ax.legend(loc='upper left', fontsize=28, frameon=True, 
                          framealpha=0.95, facecolor='#404040', edgecolor='white', 
                          bbox_to_anchor=(0.02, 0.98), markerscale=1.5)
        legend.get_frame().set_linewidth(4)
        
        # Set y-axis to start from 0 for better comparison
        ax.set_ylim(bottom=0)
        
        max_value = max(max(ppg), max(apg), max(rpg), max(spg), max(bpg))
        ax.set_ylim(top=max_value * 1.40)  # Add 40% padding above the highest point
        
        plt.tight_layout(pad=6.0)
        
        return fig
        
    except Exception as e:
        print(f"Error creating combined graph: {e}")
        return None

def main():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🏀 AI Basketball Scout 🏀</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    players = get_player_names()
    
    if not players:
        st.error("No players found. Please ensure the FastAPI backend is running.")
        return
    
    player_options = [("No player selected", None)]
    for player in players:
        if isinstance(player, dict) and "player_name" in player and "birth_year" in player:
            display_name = f"{player['player_name']}"
            player_options.append((display_name, player))
    
    if player_options:
        st.markdown('<div class="player-selection-container">', unsafe_allow_html=True)
        search_col, headshot_col = st.columns([3, 2])  # Changed from [2, 1] to [3, 2]
        
        with search_col:
            selected_display, selected_player = st.selectbox(
                "Select a player to scout:",
                options=player_options,
                format_func=lambda x: x[0],
                key="player_select"
            )
        
        with headshot_col:
            if selected_player:
                headshot_url = get_player_headshot(selected_player["player_name"], selected_player["birth_year"])
                display_player_image(headshot_url)
            else:
                st.write("") 
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_player:
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Generate Scout Report", type="primary", use_container_width=True):
                    with st.spinner("Generating scout report..."):
                        fig = create_combined_player_graph(
                            selected_player["player_name"], selected_player["birth_year"]
                        )
                        if fig:
                            st.markdown('<h3 style="text-align: center; margin: 30px 0;">Player Performance Statistics</h3>', unsafe_allow_html=True)
                            st.pyplot(fig, use_container_width=True, clear_figure=False)
                            plt.close(fig)
                            st.markdown("<br><br>", unsafe_allow_html=True)
                        
                     
                        report = generate_scout_report(
                            selected_player["player_name"], 
                            selected_player["birth_year"]
                        )
                        
    
                        section_headers = ["Overview", "Strengths", "Weaknesses", "Playstyle and Tendencies", "Scheme Fit"]
                        report = re.sub(r'(?im)^\s*##\s*Overview\s*\n', '<div class="section-header">Overview</div>\n\n', report)
                        report = re.sub(r'(?im)^\s*Overview\s*\n', '<div class="section-header">Overview</div>\n\n', report)
                        
                        for header in section_headers:
                            # Find and replace each section header with consistent formatting and CSS class
                            pattern = rf'(?im)\n\s*{re.escape(header)}\s*\n'
                            replacement = f'\n\n<div class="section-header">{header}</div>\n\n'
                            report = re.sub(pattern, replacement, report)
                        
                        report = re.sub(r'\n{3,}', '\n\n', report)  # Remove excessive line breaks
                        report = re.sub(r' +', ' ', report)  # Remove extra spaces
                        report = report.strip()  # Remove leading/trailing whitespace
                        
                        st.markdown('<div class="scout-report-title">Scout Report</div>', unsafe_allow_html=True)
                        if report:
                            st.markdown(f'<div class="scout-report">{report}</div>', unsafe_allow_html=True)
                        else:
                            st.error("Failed to generate scout report")
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.info("Please select a player to generate a scout report.")
    else:
        st.warning("No players available for selection.")
    

    st.markdown("---")
    st.markdown(
        '<div class="footer">All data provided by Basketball Reference across the 2020 to 2025 NBA Seasons</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
