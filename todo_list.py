import gradio as gr
from datetime import datetime


# -----------------------------
# Helper functions
# -----------------------------
def task_choices(tasks):
    """Create task labels for the checkbox list."""
    choices = []

    for index, task in enumerate(tasks):
        status_icon = "✅" if task["completed"] else "⬜"
        choices.append(
            (
                f'{status_icon} {task["description"]}',
                str(index)
            )
        )

    return choices


def generate_stats(tasks):
    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    pending = total - completed

    return f"""
    <div class="stats-container">
        <div class="stat-card">
            <span class="stat-number">{total}</span>
            <span class="stat-label">Total</span>
        </div>

        <div class="stat-card pending-stat">
            <span class="stat-number">{pending}</span>
            <span class="stat-label">Pending</span>
        </div>

        <div class="stat-card completed-stat">
            <span class="stat-number">{completed}</span>
            <span class="stat-label">Completed</span>
        </div>
    </div>
    """


def render_tasks(tasks):
    if not tasks:
        return gr.update(
            choices=[],
            value=[],
            label="Your Tasks"
        )

    return gr.update(
        choices=task_choices(tasks),
        value=[],
        label=f"Your Tasks ({len(tasks)})"
    )


def add_task(description, tasks):
    tasks = list(tasks or [])

    if not description or not description.strip():
        return (
            tasks,
            render_tasks(tasks),
            "",
            """
            <div class="message warning">
                ⚠️ Please enter a task description.
            </div>
            """,
            generate_stats(tasks)
        )

    description = description.strip()

    tasks.append({
        "description": description,
        "completed": False,
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })

    return (
        tasks,
        render_tasks(tasks),
        "",
        f"""
        <div class="message success">
            ✔️ <strong>{description}</strong> was added successfully.
        </div>
        """,
        generate_stats(tasks)
    )


def complete_tasks(selected_tasks, tasks):
    tasks = list(tasks or [])
    selected_tasks = selected_tasks or []

    if not selected_tasks:
        return (
            tasks,
            render_tasks(tasks),
            """
            <div class="message warning">
                ⚠️ Select at least one task first.
            </div>
            """,
            generate_stats(tasks)
        )

    for selected_index in selected_tasks:
        index = int(selected_index)

        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True

    return (
        tasks,
        render_tasks(tasks),
        """
        <div class="message success">
            ✅ Selected task(s) marked as completed.
        </div>
        """,
        generate_stats(tasks)
    )


def reopen_tasks(selected_tasks, tasks):
    tasks = list(tasks or [])
    selected_tasks = selected_tasks or []

    if not selected_tasks:
        return (
            tasks,
            render_tasks(tasks),
            """
            <div class="message warning">
                ⚠️ Select at least one task first.
            </div>
            """,
            generate_stats(tasks)
        )

    for selected_index in selected_tasks:
        index = int(selected_index)

        if 0 <= index < len(tasks):
            tasks[index]["completed"] = False

    return (
        tasks,
        render_tasks(tasks),
        """
        <div class="message info">
            🔄 Selected task(s) moved back to pending.
        </div>
        """,
        generate_stats(tasks)
    )


def delete_tasks(selected_tasks, tasks):
    tasks = list(tasks or [])
    selected_tasks = selected_tasks or []

    if not selected_tasks:
        return (
            tasks,
            render_tasks(tasks),
            """
            <div class="message warning">
                ⚠️ Select at least one task to delete.
            </div>
            """,
            generate_stats(tasks)
        )

    selected_indexes = sorted(
        [int(index) for index in selected_tasks],
        reverse=True
    )

    deleted_count = 0

    for index in selected_indexes:
        if 0 <= index < len(tasks):
            tasks.pop(index)
            deleted_count += 1

    return (
        tasks,
        render_tasks(tasks),
        f"""
        <div class="message deleted">
            🗑️ {deleted_count} task(s) deleted successfully.
        </div>
        """,
        generate_stats(tasks)
    )


def clear_completed(tasks):
    tasks = list(tasks or [])
    completed_count = sum(task["completed"] for task in tasks)

    if completed_count == 0:
        return (
            tasks,
            render_tasks(tasks),
            """
            <div class="message warning">
                ⚠️ There are no completed tasks to clear.
            </div>
            """,
            generate_stats(tasks)
        )

    tasks = [task for task in tasks if not task["completed"]]

    return (
        tasks,
        render_tasks(tasks),
        f"""
        <div class="message deleted">
            🧹 {completed_count} completed task(s) cleared.
        </div>
        """,
        generate_stats(tasks)
    )


def clear_all_tasks(tasks):
    tasks = []

    return (
        tasks,
        render_tasks(tasks),
        """
        <div class="message deleted">
            🗑️ All tasks have been removed.
        </div>
        """,
        generate_stats(tasks)
    )


# -----------------------------
# Custom interface style
# -----------------------------
custom_css = """
.gradio-container {
    max-width: 850px !important;
    margin: auto !important;
    font-family: Inter, Arial, sans-serif !important;
}

.hero {
    text-align: center;
    padding: 32px 20px 20px;
}

.hero-icon {
    width: 80px;
    height: 80px;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    box-shadow: 0 15px 35px rgba(79, 70, 229, 0.30);
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

.stats-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 12px 0 20px;
}

.stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 18px 10px;
    border-radius: 18px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
}

.pending-stat {
    background: #fff7ed;
    border-color: #fed7aa;
}

.completed-stat {
    background: #ecfdf5;
    border-color: #a7f3d0;
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
}

.stat-label {
    margin-top: 3px;
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
}

.message {
    margin: 10px 0;
    padding: 14px 18px;
    border-radius: 14px;
    border: 1px solid transparent;
}

.success {
    color: #065f46;
    background: #ecfdf5;
    border-color: #a7f3d0;
}

.warning {
    color: #92400e;
    background: #fffbeb;
    border-color: #fde68a;
}

.deleted {
    color: #991b1b;
    background: #fef2f2;
    border-color: #fecaca;
}

.info {
    color: #1e40af;
    background: #eff6ff;
    border-color: #bfdbfe;
}

#task-input textarea {
    font-size: 16px !important;
}

#add-button {
    color: white !important;
    border: none !important;
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
}

#delete-button {
    color: white !important;
    border: none !important;
    background: #ef4444 !important;
}

.footer {
    margin-top: 20px;
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
}

@media (max-width: 600px) {
    .hero h1 {
        font-size: 29px;
    }

    .stats-container {
        gap: 7px;
    }

    .stat-card {
        padding: 14px 5px;
    }

    .stat-number {
        font-size: 23px;
    }
}
"""


# -----------------------------
# Build the Gradio application
# -----------------------------
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="blue",
        radius_size="lg"
    ),
    css=custom_css,
    title="Modern To-Do List"
) as app:

    tasks_state = gr.State([])

    gr.HTML("""
    <div class="hero">
        <div class="hero-icon">📝</div>
        <h1>My To-Do List</h1>
        <p>Organize your tasks and make today productive.</p>
    </div>
    """)

    stats = gr.HTML(generate_stats([]))

    with gr.Group():
        with gr.Row():
            task_input = gr.Textbox(
                label="New Task",
                placeholder="What do you need to do?",
                lines=1,
                scale=4,
                elem_id="task-input"
            )

            add_button = gr.Button(
                "＋ Add Task",
                variant="primary",
                scale=1,
                elem_id="add-button"
            )

        message = gr.HTML("""
        <div class="message info">
            💡 Enter a task above and click Add Task.
        </div>
        """)

        task_list = gr.CheckboxGroup(
            choices=[],
            label="Your Tasks",
            info="Select one or more tasks to manage them."
        )

        with gr.Row():
            complete_button = gr.Button(
                "✅ Complete",
                variant="primary"
            )

            reopen_button = gr.Button(
                "🔄 Reopen"
            )

            delete_button = gr.Button(
                "🗑️ Delete",
                elem_id="delete-button"
            )

        with gr.Row():
            clear_completed_button = gr.Button(
                "🧹 Clear Completed"
            )

            clear_all_button = gr.Button(
                "⚠️ Clear All"
            )

    gr.HTML("""
    <div class="footer">
        Your tasks remain available while this Colab session is running.
    </div>
    """)

    # Add task
    add_button.click(
        fn=add_task,
        inputs=[task_input, tasks_state],
        outputs=[
            tasks_state,
            task_list,
            task_input,
            message,
            stats
        ]
    )

    # Pressing Enter also adds the task
    task_input.submit(
        fn=add_task,
        inputs=[task_input, tasks_state],
        outputs=[
            tasks_state,
            task_list,
            task_input,
            message,
            stats
        ]
    )

    # Complete selected tasks
    complete_button.click(
        fn=complete_tasks,
        inputs=[task_list, tasks_state],
        outputs=[
            tasks_state,
            task_list,
            message,
            stats
        ]
    )

    # Reopen selected tasks
    reopen_button.click(
        fn=reopen_tasks,
        inputs=[task_list, tasks_state],
        outputs=[
            tasks_state,
            task_list,
            message,
            stats
        ]
    )

    # Delete selected tasks
    delete_button.click(
        fn=delete_tasks,
        inputs=[task_list, tasks_state],
        outputs=[
            tasks_state,
            task_list,
            message,
            stats
        ]
    )

    # Clear completed tasks
    clear_completed_button.click(
        fn=clear_completed,
        inputs=tasks_state,
        outputs=[
            tasks_state,
            task_list,
            message,
            stats
        ]
    )

    # Clear all tasks
    clear_all_button.click(
        fn=clear_all_tasks,
        inputs=tasks_state,
        outputs=[
            tasks_state,
            task_list,
            message,
            stats
        ]
    )


# Run inside Google Colab
app.launch(share=True, debug=True)
