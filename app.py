# 🚀 AI Puzzle Generator – Tron Neon Edition with Online Learning AI (MongoDB)
# ✔ Maze, Sudoku, Riddle
# ✔ Dynamic Difficulty AI (SGDClassifier)
# ✔ MongoDB Logging
# ✔ Tron UI
# ✔ Perfectly Aligned Arrow Keys

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
from datetime import datetime
from sklearn.linear_model import SGDClassifier
from pymongo import MongoClient

# Puzzle modules
from puzzles.maze_generator import generate_maze
from puzzles.sudoku_generator import generate_sudoku
from puzzles.sudoku_interactive import create_interactive_grid, validate_sudoku
from puzzles.riddles_generator import generate_riddle

# ------------------------------------------------------------
# MongoDB Connection
# ------------------------------------------------------------
client = MongoClient("mongodb://localhost:27017")
db = client["puzzle_ai"]
logs = db["player_logs"]
model_store = db["difficulty_model"]

# ------------------------------------------------------------
# Load or Initialize AI Model
# ------------------------------------------------------------
classes = np.array(["Easy", "Medium", "Hard"])
model = SGDClassifier(loss="log_loss")

stored = model_store.find_one({"_id": "current_model"})
if stored:
    model = pickle.loads(stored["model_bytes"])
else:
    model.partial_fit([[0, 0, 0, 0]], ["Easy"], classes=classes)

# ------------------------------------------------------------
# Tron Neon Theme
# ------------------------------------------------------------
st.set_page_config(page_title="AI Puzzle Generator", layout="wide", page_icon="💠")

st.markdown("""
<style>
body { background-color:#0b0f19; color:#00eaff; }
.stApp { background:#0b0f19; }
h1,h2,h3 { color:#00eaff; text-shadow:0 0 10px #00eaff; }
.stButton>button {
    background:transparent; color:#00eaff;
    border:2px solid #00eaff; border-radius:10px;
    box-shadow:0 0 10px #00eaff;
}
.stButton>button:hover {
    background:#00eaff22;
    box-shadow:0 0 20px #00eaff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>💠 AI Puzzle Generator </h1>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Initialize Session State
# ------------------------------------------------------------
def init_state():
    defaults = {
        "player": (1, 1),
        "current_maze": None,
        "sudoku_grid": None,
        "sudoku_solution": None,
        "current_riddle": None,
        "mistakes": 0,
        "attempts": 0,
        "start_time": None,
        "time_taken": 0,
        "puzzle_completed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
puzzle_type = st.sidebar.selectbox("Puzzle Type", ["Maze", "Sudoku", "Riddle"])
predicted_difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

if st.sidebar.button("Start Timer"):
    st.session_state.start_time = time.time()

if st.sidebar.button("Stop Timer") and st.session_state.start_time:
    st.session_state.time_taken = round(time.time() - st.session_state.start_time, 2)
    st.sidebar.success(f"Time: {st.session_state.time_taken}s")

# ------------------------------------------------------------
# Feature Extraction
# ------------------------------------------------------------
def extract_features():
    return [
        ["Maze", "Sudoku", "Riddle"].index(puzzle_type),
        st.session_state.time_taken,
        st.session_state.mistakes,
        st.session_state.attempts,
    ]

# ------------------------------------------------------------
# AI Model Update
# ------------------------------------------------------------
def update_ai(success):
    logs.insert_one({
        "puzzle_type": puzzle_type,
        "time_taken": st.session_state.time_taken,
        "mistakes": st.session_state.mistakes,
        "attempts": st.session_state.attempts,
        "success": int(success),
        "timestamp": datetime.utcnow(),
    })

    X = [extract_features()]
    y = [predicted_difficulty]
    model.partial_fit(X, y)

    blob = pickle.dumps(model)
    model_store.update_one({"_id": "current_model"}, {"$set": {"model_bytes": blob}}, upsert=True)

# ------------------------------------------------------------
# Predict Difficulty
# ------------------------------------------------------------
def ai_predict_next():
    return model.predict([extract_features()])[0]

# ------------------------------------------------------------
# Maze Movement
# ------------------------------------------------------------
def move_player(direction):
    maze = st.session_state.current_maze
    r, c = st.session_state.player
    moves = {"up":(-1,0), "down":(1,0), "left":(0,-1), "right":(0,1)}
    dr, dc = moves[direction]
    nr, nc = r + dr, c + dc

    if maze[nr][nc] == 0:
        st.session_state.player = (nr, nc)
    else:
        st.session_state.mistakes += 1

    if (nr, nc) == (maze.shape[0]-2, maze.shape[1]-2):
        st.success("💠 Maze Completed!")
        st.session_state.puzzle_completed = True
# ------------------------------------------------------------
# Generate Puzzle
# ------------------------------------------------------------
def generate_puzzle():
    st.session_state.mistakes = 0
    st.session_state.attempts = 0
    st.session_state.time_taken = 0
    st.session_state.puzzle_completed = False

    if puzzle_type == "Maze":
        st.session_state.current_maze = generate_maze(21, 21)
        st.session_state.player = (1, 1)

    elif puzzle_type == "Sudoku":
        puzzle = generate_sudoku(predicted_difficulty)
        st.session_state.sudoku_solution = puzzle.copy()
        st.session_state.sudoku_grid = create_interactive_grid(puzzle)

    else:  # Riddle
        st.session_state.current_riddle = generate_riddle()

# ------------------------------------------------------------
# Generate Button
# ------------------------------------------------------------
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
if st.button(f"Generate {puzzle_type} 💠"):
    generate_puzzle()
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# MAZE RENDER + PERFECT ARROW KEYS
# ------------------------------------------------------------
if puzzle_type == "Maze" and st.session_state.current_maze is not None:

    maze = st.session_state.current_maze.copy()
    r, c = st.session_state.player
    maze[r][c] = 2  # player position highlight

    left, right = st.columns([3,1])

    # Maze display
    with left:
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.imshow(maze, cmap="winter")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        st.pyplot(fig, use_container_width=True)

    # Arrow key controls
    with right:
        st.markdown("<h3 style='text-align:center;'>Controls</h3>", unsafe_allow_html=True)

        # UP
        up1, up2, up3 = st.columns([1,1,1])
        with up2:
            if st.button("⬆️"):
                move_player("up")

        # LEFT — EMPTY — RIGHT
        left1, mid, right1 = st.columns([1,1,1])
        with left1:
            if st.button("⬅️"):
                move_player("left")
        with mid:
            st.write("")  # perfect centering
        with right1:
            if st.button("➡️"):
                move_player("right")

        # DOWN
        down1, down2, down3 = st.columns([1,1,1])
        with down2:
            if st.button("⬇️"):
                move_player("down")

    # AI update when maze solved
    if st.session_state.puzzle_completed:
        update_ai(True)
        st.info(f"Next Difficulty (AI): {ai_predict_next()}")
# ------------------------------------------------------------
# SUDOKU RENDER
# ------------------------------------------------------------
if puzzle_type == "Sudoku" and st.session_state.sudoku_grid is not None:

    st.subheader("💠 Sudoku ")

    # Editable Sudoku grid
    edited = st.data_editor(
        st.session_state.sudoku_grid,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button("Check Sudoku ✔️"):
        correct_mask, incorrect_mask, solved = validate_sudoku(
            edited,
            st.session_state.sudoku_solution
        )

        st.session_state.attempts += 1
        wrong = sum(
            1 for i in range(9) for j in range(9)
            if incorrect_mask[i][j]
        )
        st.session_state.mistakes += wrong

        if solved:
            st.success("💠 Sudoku Solved!")
            st.session_state.puzzle_completed = True

            update_ai(True)
            st.info(f"Next Difficulty (AI): {ai_predict_next()}")

        else:
            st.error("Incorrect Cells")

            styled = edited.style.apply(
                lambda x: [
                    "background-color:#ff004450" if incorrect_mask[i][j] else ""
                    for i in range(9) for j in range(9)
                ],
                axis=None,
            )
            st.write(styled)

# ------------------------------------------------------------
# RIDDLE RENDER
# ------------------------------------------------------------
if puzzle_type == "Riddle" and st.session_state.current_riddle is not None:

    r = st.session_state.current_riddle

    st.subheader("💠 Riddle Challenge")
    st.info(r["question"])

    answer = st.text_input("Your Answer:")

    if st.button("Check Answer"):
        st.session_state.attempts += 1

        if answer.strip().lower() == r["answer"]:
            st.success("Correct!")

            st.session_state.puzzle_completed = True
            update_ai(True)

            st.info(f"Next Difficulty (AI): {ai_predict_next()}")

        else:
            st.error("Incorrect")
            st.session_state.mistakes += 1

    if st.button("New Riddle 🔄"):
        st.session_state.current_riddle = generate_riddle()
