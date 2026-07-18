"""
Expected Goals (xG) Analytics & Penalty Mini-Game
-------------------------
To run this app, type this in your terminal:
python -m streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import xgboost as xgb
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="xG AI & Game", layout="wide", page_icon="⚽")

# ==========================================
# 1. THE HTML5 MINI-GAME CODE (JAVASCRIPT)
# ==========================================
# We inject this directly into the browser for real-time 60fps flick mechanics!
flick_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; background-color: #0e1117; color: white; font-family: sans-serif; }
        canvas { background: #2b8c5a; border: 4px solid #fff; border-radius: 10px; cursor: crosshair; touch-action: none; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        #scoreboard { display: flex; justify-content: space-between; width: 600px; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
        #instructions { margin-top: 10px; font-size: 16px; color: #aaa; }
    </style>
</head>
<body>
    <div id="scoreboard">
        <div>Score: <span id="score">0</span></div>
        <div id="message">Flick the ball to shoot!</div>
        <div>Saves: <span id="saves">0</span></div>
    </div>
    <canvas id="gameCanvas" width="600" height="400"></canvas>
    <div id="instructions">Click and drag (flick) your mouse towards the goal to shoot.</div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const msg = document.getElementById('message');
        
        let score = 0; let saves = 0;
        let isDragging = false; let startX, startY;
        
        // Game Objects
        const goal = { x: 150, y: 50, w: 300, h: 100 };
        const keeper = { x: 275, y: 120, w: 50, h: 30, speed: 0, targetX: 275 };
        let ball = { x: 300, y: 320, r: 15, vx: 0, vy: 0, moving: false, scale: 1 };
        
        // Input tracking
        canvas.addEventListener('mousedown', (e) => {
            if(ball.moving) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            // Check if clicking near ball
            if (Math.hypot(mouseX - ball.x, mouseY - ball.y) < 50) {
                isDragging = true; startX = mouseX; startY = mouseY;
            }
        });

        canvas.addEventListener('mouseup', (e) => {
            if(!isDragging) return;
            isDragging = false;
            const rect = canvas.getBoundingClientRect();
            const endX = e.clientX - rect.left;
            const endY = e.clientY - rect.top;
            
            // Calculate flick vector
            const dx = endX - startX; const dy = endY - startY;
            if (dy < -20) { // Must flick forwards (up)
                ball.vx = dx * 0.15;
                ball.vy = dy * 0.15;
                ball.moving = true;
                
                // AI Keeper Logic: Predicts where ball is going and moves there
                // Adds a little random error so he doesn't save everything
                let predictedX = ball.x + (ball.vx * (Math.abs((ball.y - goal.y) / ball.vy)));
                let error = (Math.random() - 0.5) * 100; // Keeper makes mistakes
                keeper.targetX = Math.max(goal.x, Math.min(goal.x + goal.w - keeper.w, predictedX + error - (keeper.w/2)));
            }
        });

        function reset() {
            ball = { x: 300, y: 320, r: 15, vx: 0, vy: 0, moving: false, scale: 1 };
            keeper.x = 275; keeper.targetX = 275;
            msg.innerText = "Flick to shoot!";
            msg.style.color = "white";
        }

        function update() {
            // Draw Pitch
            ctx.fillStyle = '#2b8c5a'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw Goal Lines
            ctx.strokeStyle = 'white'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(0, 50); ctx.lineTo(600, 50); ctx.stroke(); // Backline
            ctx.beginPath(); ctx.moveTo(100, 50); ctx.lineTo(100, 200); ctx.lineTo(500, 200); ctx.lineTo(500, 50); ctx.stroke(); // Penalty Box
            
            // Draw Goal Net
            ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(goal.x, goal.y, goal.w, goal.h);
            ctx.strokeStyle = 'white'; ctx.strokeRect(goal.x, goal.y, goal.w, goal.h);

            // Update Ball Physics
            if (ball.moving) {
                ball.x += ball.vx; ball.y += ball.vy;
                ball.scale -= 0.015; // Simulates ball going away (depth)
                
                // Keeper Movement (Lerp)
                keeper.x += (keeper.targetX - keeper.x) * 0.08;

                // Collision Detection (Ball reaches goal line)
                if (ball.scale <= 0.4 || ball.y <= goal.y + goal.h) {
                    ball.moving = false;
                    
                    // Did Keeper save it?
                    if (ball.x > keeper.x - 20 && ball.x < keeper.x + keeper.w + 20 && ball.y <= keeper.y + 20) {
                        msg.innerText = "SAVED BY THE KEEPER!"; msg.style.color = "red";
                        saves++; document.getElementById('saves').innerText = saves;
                    } 
                    // Did it hit the net?
                    else if (ball.x > goal.x && ball.x < goal.x + goal.w && ball.y <= goal.y + goal.h) {
                        msg.innerText = "GOAL!!!"; msg.style.color = "#00ff00";
                        score++; document.getElementById('score').innerText = score;
                    } 
                    // Missed completely
                    else {
                        msg.innerText = "MISSED THE TARGET!"; msg.style.color = "orange";
                    }
                    setTimeout(reset, 1500); // Reset after 1.5 seconds
                }
            }

            // Draw Keeper (Orange block)
            ctx.fillStyle = 'orange'; ctx.fillRect(keeper.x, keeper.y, keeper.w, keeper.h);

            // Draw Ball
            ctx.beginPath();
            ctx.arc(ball.x, ball.y, Math.max(ball.r * ball.scale, 2), 0, Math.PI * 2);
            ctx.fillStyle = 'white'; ctx.fill(); ctx.strokeStyle = 'black'; ctx.stroke();

            requestAnimationFrame(update);
        }
        update(); // Start loop
    </script>
</body>
</html>
"""

# ==========================================
# 2. CACHED DATA & MODEL (FROM DASHBOARD)
# ==========================================
@st.cache_data
def get_shot_data():
    np.random.seed(42)
    n_shots = 2500 
    x_coords = np.clip(np.random.normal(85, 10, n_shots), 0, 100)
    y_coords = np.clip(np.random.normal(50, 15, n_shots), 0, 100)
    situations = np.random.choice(['OpenPlay', 'SetPiece', 'Corner', 'FreeKick'], n_shots, p=[0.7, 0.1, 0.15, 0.05])
    body_parts = np.random.choice(['RightFoot', 'LeftFoot', 'Head'], n_shots, p=[0.55, 0.30, 0.15])
    assist_types = np.random.choice(['Pass', 'Cross', 'ThroughBall', 'None'], n_shots, p=[0.5, 0.2, 0.1, 0.2])
    dist_to_goal = np.sqrt((100 - x_coords)**2 + (50 - y_coords)**2)
    pressure = np.clip(np.random.normal(80 - (dist_to_goal * 0.5), 20, n_shots), 0, 100)
    goal_prob = np.exp(-dist_to_goal / 15) * 0.5 
    goal_prob = np.where(body_parts == 'Head', goal_prob * 0.7, goal_prob)
    goal_prob = np.where(assist_types == 'ThroughBall', goal_prob * 1.4, goal_prob)
    goal_prob = np.where(assist_types == 'Cross', goal_prob * 0.8, goal_prob)
    goal_prob = goal_prob * (1 - (pressure / 200))
    is_goal = np.random.binomial(1, np.clip(goal_prob, 0, 1))
    return pd.DataFrame({'X': x_coords, 'Y': y_coords, 'situation': situations, 'body_part': body_parts, 'assist_type': assist_types, 'defender_pressure': pressure, 'is_goal': is_goal})

@st.cache_data
def engineer_features(df):
    df['distance'] = np.sqrt((100 - df['X'])**2 + (50 - df['Y'])**2)
    post1_y, post2_y = 46, 54
    a_sq = (100 - df['X'])**2 + (post1_y - df['Y'])**2
    b_sq = (100 - df['X'])**2 + (post2_y - df['Y'])**2
    c_sq = (post2_y - post1_y)**2
    df['angle_rad'] = np.arccos(np.clip((a_sq + b_sq - c_sq) / (2 * np.sqrt(a_sq) * np.sqrt(b_sq) + 1e-9), -1.0, 1.0))
    df['angle_deg'] = np.degrees(df['angle_rad'])
    return pd.get_dummies(df, columns=['situation', 'body_part', 'assist_type'], drop_first=True)

@st.cache_resource
def train_xgboost_model(df):
    features = [col for col in df.columns if col not in ['is_goal']]
    X, y = df[features], df['is_goal']
    model = xgb.XGBClassifier(n_estimators=50, learning_rate=0.1, max_depth=4, objective='binary:logistic', random_state=42)
    model.fit(X, y)
    df['xG'] = model.predict_proba(X)[:, 1]
    return model, df, features

raw_df = get_shot_data()
processed_df = engineer_features(raw_df)
model, final_df, model_features = train_xgboost_model(processed_df)

# ==========================================
# 3. TABS SETUP (DASHBOARD vs GAME)
# ==========================================
st.title("⚽ Analytics & Match Day")
tab_dashboard, tab_game = st.tabs(["📊 Analytics Dashboard", "🎮 Penalty Flick Game"])

# ==========================================
# 4. TAB 1: THE PRO DASHBOARD
# ==========================================
with tab_dashboard:
    st.sidebar.header("👤 Scenario Profiles")
    profile = st.sidebar.selectbox("Select a scenario:", ["Custom Play", "Erling Haaland (Tap-in)", "Lionel Messi (Free Kick)", "Sunday League Amateur"])

    def_x, def_y, def_pres, def_ast, def_bod, def_sit, def_ty, def_tz = 85.0, 50.0, 20, "Pass", "RightFoot", "OpenPlay", 50.0, 1.0
    if profile == "Erling Haaland (Tap-in)": def_x, def_y, def_pres, def_ast, def_bod, def_sit, def_ty, def_tz = 94.0, 50.0, 60, "ThroughBall", "LeftFoot", "OpenPlay", 47.0, 0.5
    elif profile == "Lionel Messi (Free Kick)": def_x, def_y, def_pres, def_ast, def_bod, def_sit, def_ty, def_tz = 75.0, 65.0, 0, "None", "LeftFoot", "FreeKick", 53.5, 2.2
    elif profile == "Sunday League Amateur": def_x, def_y, def_pres, def_ast, def_bod, def_sit, def_ty, def_tz = 60.0, 30.0, 10, "Cross", "RightFoot", "OpenPlay", 40.0, 5.0

    with st.sidebar.expander("📍 Player Position", expanded=True):
        sim_x = st.slider("Distance from Goal Line (X)", 50.0, 100.0, def_x)
        sim_y = st.slider("Pitch Width (Y)", 0.0, 100.0, def_y)

    with st.sidebar.expander("⚽ The Play Setup", expanded=True):
        sim_pressure = st.slider("Defender Pressure", 0, 100, def_pres)
        sim_assist = st.selectbox("Assist Type", ["Pass", "ThroughBall", "Cross", "None"], index=["Pass", "ThroughBall", "Cross", "None"].index(def_ast))
        sim_body = st.selectbox("Body Part", ["RightFoot", "LeftFoot", "Head"], index=["RightFoot", "LeftFoot", "Head"].index(def_bod))
        sim_situation = st.selectbox("Situation", ["OpenPlay", "SetPiece", "Corner", "FreeKick"], index=["OpenPlay", "SetPiece", "Corner", "FreeKick"].index(def_sit))

    with st.sidebar.expander("🥅 The Shot (Placement)", expanded=True):
        target_y = st.slider("Placement (Left/Right)", 40.0, 60.0, def_ty)
        target_z = st.slider("Placement (Height in meters)", 0.0, 5.0, def_tz)

    # Math & Prediction
    sim_distance = np.sqrt((100 - sim_x)**2 + (50 - sim_y)**2)
    a_sq = (100 - sim_x)**2 + (46 - sim_y)**2; b_sq = (100 - sim_x)**2 + (54 - sim_y)**2; c_sq = (54 - 46)**2
    cos_th = np.clip((a_sq + b_sq - c_sq) / (2 * np.sqrt(a_sq) * np.sqrt(b_sq) + 1e-9), -1.0, 1.0)
    sim_angle = np.degrees(np.arccos(cos_th))

    sim_data = pd.DataFrame(0, index=[0], columns=model_features)
    sim_data['X'], sim_data['Y'], sim_data['defender_pressure'] = sim_x, sim_y, sim_pressure
    sim_data['distance'], sim_data['angle_rad'], sim_data['angle_deg'] = sim_distance, np.arccos(cos_th), sim_angle
    if f"body_part_{sim_body}" in sim_data.columns: sim_data[f"body_part_{sim_body}"] = 1
    if f"assist_type_{sim_assist}" in sim_data.columns: sim_data[f"assist_type_{sim_assist}"] = 1
    if f"situation_{sim_situation}" in sim_data.columns: sim_data[f"situation_{sim_situation}"] = 1

    predicted_xg = model.predict_proba(sim_data)[:, 1][0]
    on_target = (46.0 <= target_y <= 54.0) and (target_z <= 2.44)

    if not on_target:
        psxg, save_prob = 0.0, 0.0
    else:
        shot_difficulty = (abs(target_y - 50.0) / 4.0 * 0.6) + (target_z / 2.44 * 0.4)
        psxg = np.clip(predicted_xg * (0.3 + (shot_difficulty * 1.5)), 0.01, 0.99)
        save_prob = 1.0 - psxg

    if sim_assist == 'Cross': pass_x, pass_y = 85, 10 if sim_y < 50 else 90
    elif sim_assist == 'ThroughBall': pass_x, pass_y = sim_x - 15, 50
    elif sim_assist == 'Pass': pass_x, pass_y = sim_x - 10, sim_y + 10
    else: pass_x, pass_y = sim_x, sim_y
    gk_x, gk_y = 100 - min((100 - sim_x) * 0.15, 4), 50 + (sim_y - 50) * 0.3
    ball_x_path, ball_y_path = [], []
    if sim_assist != 'None':
        ball_x_path.extend(np.linspace(pass_x, sim_x, 15)); ball_y_path.extend(np.linspace(pass_y, sim_y, 15))
    ball_x_path.extend(np.linspace(sim_x, 100, 15)); ball_y_path.extend(np.linspace(sim_y, target_y, 15))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pre-Shot xG", f"{predicted_xg:.2f}")
    col2.metric("Post-Shot xG (PSxG)", f"{psxg:.2f}")
    col3.metric("GK Save Prob", f"{save_prob * 100:.1f}%" if on_target else "N/A")
    col4.metric("Shot Distance", f"{sim_distance:.1f}m")

    if not on_target: st.error("🤦‍♂️ **Terrible miss.** You completely missed the target.")
    elif save_prob > 0.8: st.warning("🧤 **Easy save.** You hit it right at the keeper.")
    elif psxg > 0.6: st.success("🔥 **Unstoppable!** An absolute rocket into the danger zone.")
    elif sim_pressure > 70 and predicted_xg < 0.1: st.error("❌ **Selfish decision.** You should have passed the ball.")
    else: st.info("⚽ **Decent effort.** A solid attempt, 50/50 for the keeper.")

    st.divider()
    col_map, col_net = st.columns([1.5, 1])

    with col_map:
        fig = go.Figure()
        shapes = [
            dict(type="rect", x0=50, y0=0, x1=100, y1=100, line=dict(color="#4f5b66"), fillcolor="#0e1117", layer="below"),
            dict(type="rect", x0=82, y0=21, x1=100, y1=79, line=dict(color="#4f5b66"), layer="below"),
            dict(type="rect", x0=94, y0=36.8, x1=100, y1=63.2, line=dict(color="#4f5b66"), layer="below"),
            dict(type="rect", x0=100, y0=46, x1=102, y1=54, line=dict(color="#4f5b66"), layer="below"),
        ]
        fig.update_layout(shapes=shapes, template="plotly_dark", height=500, xaxis=dict(range=[50, 105], showgrid=False, zeroline=False), yaxis=dict(range=[-5, 105], showgrid=False, zeroline=False), margin=dict(l=0, r=0, t=0, b=0))

        goals_df = final_df[final_df['is_goal'] == 1]
        fig.add_trace(go.Histogram2dContour(x=goals_df['X'], y=goals_df['Y'], colorscale='Hot', opacity=0.3, showscale=False, ncontours=15, line=dict(width=0), hoverinfo='skip', name="Danger Zone"))
        fig.add_trace(go.Scatter(x=[gk_x], y=[gk_y], mode="markers+text", marker=dict(color="orange", size=14), text=["GK"], textposition="top right", name="Goalkeeper"))
        fig.add_trace(go.Scatter(x=[sim_x], y=[sim_y], mode="markers+text", marker=dict(color="rgba(0, 255, 0, 0.3)", size=16, symbol="x"), text=["Shot Origin"], textposition="bottom center", name="Shooter"))
        
        if sim_assist != 'None':
            fig.add_trace(go.Scatter(x=[pass_x], y=[pass_y], mode="markers+text", marker=dict(color="cyan", size=10), text=["Pass Origin"], textposition="bottom center", name="Passer"))
        else:
            fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", showlegend=False))

        fig.add_trace(go.Scatter(x=[ball_x_path[0]], y=[ball_y_path[0]], mode="markers", marker=dict(color="white", size=12, line=dict(color="black", width=2)), name="Ball"))

        frames = [go.Frame(data=[go.Scatter(x=[ball_x_path[k]], y=[ball_y_path[k]])], traces=[4]) for k in range(len(ball_x_path))]
        fig.frames = frames
        fig.update_layout(updatemenus=[dict(type="buttons", showactive=False, x=0.05, y=1.1, xanchor="left", yanchor="top", buttons=[dict(label="▶️ PLAY ANIMATION", method="animate", args=[None, dict(frame=dict(duration=40, redraw=False), transition=dict(duration=0), fromcurrent=True, mode="immediate")])])])
        st.plotly_chart(fig, use_container_width=True)

    with col_net:
        fig2 = go.Figure()
        fig2.add_shape(type="rect", x0=40, y0=-2, x1=60, y1=0, fillcolor="#2b8c5a", line=dict(width=0), layer="below")
        fig2.add_shape(type="rect", x0=46, y0=0, x1=54, y1=2.44, line=dict(color="white", width=6), fillcolor="rgba(0,0,0,0.3)")
        for i in np.linspace(46.2, 53.8, 15): fig2.add_shape(type="line", x0=i, y0=0, x1=i, y1=2.44, line=dict(color="rgba(255,255,255,0.15)", width=1))
        for i in np.linspace(0.2, 2.44, 6): fig2.add_shape(type="line", x0=46, y0=i, x1=54, y1=i, line=dict(color="rgba(255,255,255,0.15)", width=1))
        
        fig2.add_trace(go.Scatter(
            x=[target_y], y=[target_z], mode="markers",
            marker=dict(size=22, symbol="circle" if on_target else "x", color=[psxg] if on_target else ["red"], colorscale="RdYlBu_r" if on_target else None, cmin=0 if on_target else None, cmax=1 if on_target else None, line=dict(color="white", width=2)),
            text=[f"PSxG: {psxg:.2f}<br>Save Prob: {save_prob*100:.1f}%"] if on_target else ["MISS!"], hoverinfo="text", name="Shot"
        ))
        fig2.update_layout(template="plotly_dark", height=450, xaxis=dict(range=[42, 58], showgrid=False, zeroline=False, visible=False), yaxis=dict(range=[-1, 4], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1), margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 5. TAB 2: THE PLAYABLE MINI-GAME
# ==========================================
with tab_game:
    st.subheader("🎮 Can you beat the AI Keeper?")
    st.markdown("Use your mouse to **click and quickly drag (flick)** the ball toward the net. The AI Keeper will try to predict where you are aiming based on your swipe velocity!")
    
    # Render the custom HTML5/JS game directly into Streamlit
    components.html(flick_game_html, height=550)