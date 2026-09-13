import random
import gradio as gr


# -----------------------------
# Game logic
# -----------------------------
def create_game(difficulty):
    ranges = {
        "Easy (1–50)": (1, 50),
        "Normal (1–100)": (1, 100),
        "Hard (1–500)": (1, 500),
    }

    minimum, maximum = ranges[difficulty]

    return {
        "secret_number": random.randint(minimum, maximum),
        "attempts": 0,
        "minimum": minimum,
        "maximum": maximum,
        "game_over": False,
    }


def start_game(difficulty):
    game = create_game(difficulty)

    message = f"""
    <div class="status-card ready">
        <div class="status-icon">🎯</div>
        <div>
            <h3>New game started!</h3>
            <p>I selected a number between
            <strong>{game["minimum"]}</strong> and
            <strong>{game["maximum"]}</strong>.</p>
        </div>
    </div>
    """

    return (
        game,
        message,
        "Attempts: 0",
        None,
        gr.update(interactive=True),
    )


def check_guess(guess, game):
    if not game:
        return (
            game,
            """
            <div class="status-card warning">
                <div class="status-icon">⚠️</div>
                <div>
                    <h3>Start a new game</h3>
                    <p>Please click the New Game button first.</p>
                </div>
            </div>
            """,
            "Attempts: 0",
            None,
            gr.update(),
        )

    if game["game_over"]:
        return (
            game,
            """
            <div class="status-card warning">
                <div class="status-icon">🔄</div>
                <div>
                    <h3>This round is finished</h3>
                    <p>Click New Game to play again.</p>
                </div>
            </div>
            """,
            f'Attempts: {game["attempts"]}',
            None,
            gr.update(interactive=False),
        )

    if guess is None:
        return (
            game,
            """
            <div class="status-card warning">
                <div class="status-icon">⚠️</div>
                <div>
                    <h3>Enter a number</h3>
                    <p>Please type your guess before submitting.</p>
                </div>
            </div>
            """,
            f'Attempts: {game["attempts"]}',
            None,
            gr.update(),
        )

    # Prevent decimal values
    if float(guess) != int(guess):
        return (
            game,
            """
            <div class="status-card warning">
                <div class="status-icon">⚠️</div>
                <div>
                    <h3>Whole numbers only</h3>
                    <p>Please enter a valid whole number.</p>
                </div>
            </div>
            """,
            f'Attempts: {game["attempts"]}',
            None,
            gr.update(),
        )

    guess = int(guess)

    if guess < game["minimum"] or guess > game["maximum"]:
        return (
            game,
            f"""
            <div class="status-card warning">
                <div class="status-icon">⚠️</div>
                <div>
                    <h3>Number outside the range</h3>
                    <p>Enter a number from
                    <strong>{game["minimum"]}</strong> to
                    <strong>{game["maximum"]}</strong>.</p>
                </div>
            </div>
            """,
            f'Attempts: {game["attempts"]}',
            None,
            gr.update(),
        )

    game["attempts"] += 1
    secret_number = game["secret_number"]
    difference = abs(secret_number - guess)

    if guess == secret_number:
        game["game_over"] = True

        message = f"""
        <div class="status-card success">
            <div class="status-icon">🏆</div>
            <div>
                <h3>Congratulations!</h3>
                <p>You found <strong>{secret_number}</strong> in
                <strong>{game["attempts"]} attempts</strong>.</p>
            </div>
        </div>
        """

        return (
            game,
            message,
            f'Attempts: {game["attempts"]}',
            None,
            gr.update(interactive=False),
        )

    direction = "higher" if guess < secret_number else "lower"
    arrow = "⬆️" if guess < secret_number else "⬇️"

    if difference <= 3:
        temperature = "🔥 Extremely close!"
    elif difference <= 10:
        temperature = "🌡️ Very close!"
    elif difference <= 20:
        temperature = "🙂 Getting closer!"
    else:
        temperature = "❄️ Still far away!"

    message = f"""
    <div class="status-card incorrect">
        <div class="status-icon">{arrow}</div>
        <div>
            <h3>Try a {direction} number</h3>
            <p>{temperature}</p>
        </div>
    </div>
    """

    return (
        game,
        message,
        f'Attempts: {game["attempts"]}',
        None,
        gr.update(),
    )


# -----------------------------
# Interface design
# -----------------------------
custom_css = """
.gradio-container {
    max-width: 760px !important;
    margin: auto !important;
    font-family: Inter, Arial, sans-serif !important;
}

.game-container {
    border-radius: 28px !important;
    padding: 12px !important;
}

.hero {
    text-align: center;
    padding: 30px 20px 18px;
}

.hero-icon {
    width: 78px;
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    border-radius: 24px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.30);
    font-size: 40px;
}

.hero h1 {
    margin: 18px 0 6px;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    margin: 0;
    color: #64748b;
    font-size: 16px;
}

.status-card {
    min-height: 100px;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    margin: 12px 0;
    border-radius: 18px;
    border: 1px solid transparent;
}

.status-card h3 {
    margin: 0 0 5px;
    font-size: 19px;
}

.status-card p {
    margin: 0;
    line-height: 1.6;
}

.status-icon {
    font-size: 34px;
}

.ready {
    background: #eff6ff;
    border-color: #bfdbfe;
    color: #1e3a8a;
}

.incorrect {
    background: #fff7ed;
    border-color: #fed7aa;
    color: #9a3412;
}

.warning {
    background: #fffbeb;
    border-color: #fde68a;
    color: #92400e;
}

.success {
    background: #ecfdf5;
    border-color: #a7f3d0;
    color: #065f46;
}

#guess-input input {
    font-size: 24px !important;
    font-weight: 700 !important;
    text-align: center !important;
}

#guess-button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
}

#new-game-button {
    border: 1px solid #cbd5e1 !important;
}

.attempt-counter {
    text-align: center;
    padding: 10px;
    margin-top: 5px;
    border-radius: 12px;
    background: rgba(148, 163, 184, 0.12);
    font-weight: 700;
}
"""


# -----------------------------
# Build the application
# -----------------------------
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="blue",
        radius_size="lg",
    ),
    css=custom_css,
    title="Number Guessing Game",
) as app:

    game_state = gr.State()

    gr.HTML("""
    <div class="hero">
        <div class="hero-icon">🎯</div>
        <h1>Guess the Number</h1>
        <p>Can you discover the secret number?</p>
    </div>
    """)

    with gr.Group(elem_classes="game-container"):
        difficulty = gr.Dropdown(
            choices=[
                "Easy (1–50)",
                "Normal (1–100)",
                "Hard (1–500)",
            ],
            value="Normal (1–100)",
            label="Difficulty level",
        )

        status = gr.HTML("""
        <div class="status-card ready">
            <div class="status-icon">👋</div>
            <div>
                <h3>Ready to play?</h3>
                <p>Select a difficulty and click New Game.</p>
            </div>
        </div>
        """)

        guess_input = gr.Number(
            label="Your guess",
            placeholder="Enter a whole number",
            precision=0,
            elem_id="guess-input",
        )

        attempt_counter = gr.HTML(
            '<div class="attempt-counter">Attempts: 0</div>'
        )

        with gr.Row():
            new_game_button = gr.Button(
                "🔄 New Game",
                elem_id="new-game-button",
            )

            guess_button = gr.Button(
                "Submit Guess 🚀",
                variant="primary",
                elem_id="guess-button",
            )

    gr.Markdown(
        "<div style='text-align:center;color:#94a3b8'>"
        "Tip: Use the higher/lower hints to narrow down the answer."
        "</div>"
    )

    new_game_button.click(
        fn=start_game,
        inputs=difficulty,
        outputs=[
            game_state,
            status,
            attempt_counter,
            guess_input,
            guess_input,
        ],
    )

    guess_button.click(
        fn=check_guess,
        inputs=[guess_input, game_state],
        outputs=[
            game_state,
            status,
            attempt_counter,
            guess_input,
            guess_input,
        ],
    )

    guess_input.submit(
        fn=check_guess,
        inputs=[guess_input, game_state],
        outputs=[
            game_state,
            status,
            attempt_counter,
            guess_input,
            guess_input,
        ],
    )

    app.load(
        fn=start_game,
        inputs=difficulty,
        outputs=[
            game_state,
            status,
            attempt_counter,
            guess_input,
            guess_input,
        ],
    )


# Launch inside Google Colab
app.launch(share=True, debug=True)
