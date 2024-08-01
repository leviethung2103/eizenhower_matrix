import streamlit as st
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

st.set_page_config(layout="wide")

# import streamlit_shadcn_ui as ui

# ui.checkbox(default_checked=True, label="I am a Checkbox 1")

# ui.alert_dialog(
#     show=trigger_btn,
#     title="Alert Dialog",
#     description="This is an alert dialog",
#     confirm_label="OK",
#     cancel_label="Cancel",
#     key="alert_dialog1",
# )

# Replace the API Key
TODOIST_API_KEY = ""
api = TodoistAPI(TODOIST_API_KEY)

assert len(TODOIST_API_KEY) != 0

def fetch_todoist():
    try:
        u1, u2, u3, u4 = [], [], [], []
        tasks = api.get_tasks()
        for task in tasks:
            task_dict = task.to_dict()
            is_completed = task_dict["is_completed"]
            content = task_dict["content"]
            created_at = task_dict["created_at"]
            priority = task_dict["priority"]
            id = task_dict["id"]
            # 4 -> P1 , 3 -> P2 , 2 -> P3 , 1 -> P4
            if priority == 4:
                u1.append((content, created_at, id))
            elif priority == 3:
                u2.append((content, created_at, id))
            elif priority == 2:
                u3.append((content, created_at, id))
            elif priority == 1:
                u4.append((content, created_at, id))

        return u1, u2, u3, u4

    except Exception as error:
        print(error)


def update_task(**kwargs):
    task_id = kwargs.get("task_id")
    api.close_task(task_id=task_id)


def handle_task_checkbox(task):
    task_name = task[0]
    task_id = task[2]

    st.checkbox(task_name, key=task_id, on_change=update_task, kwargs=dict(task_id=task_id, task_name=task_name))


def submit_task():
    # add task
    api.add_task(
        content=st.session_state["foo"],
        due_string="tomorrow at 12:00",
        due_lang="en",
        priority=4,
    )
    # clear
    st.session_state["foo"] = ""


# UI
st.write("## Tasks & Priorities")
st.text_input("Enter new task", on_change=submit_task, key="foo")
# BACKEND
u1, u2, u3, u4 = fetch_todoist()

st.write("#### Matrix")
c1, c2 = st.columns(2)
c1.markdown("**Urgent & important**")

with c1:
    for t in u1:
        handle_task_checkbox(t)


c2.markdown("**Not urgent & important**")
with c2:
    for t in u2:
        handle_task_checkbox(t)


s1, s2 = st.columns(2)

s1.markdown("**Urgent & not important**")
with s1:
    for t in u3:
        handle_task_checkbox(t)

s2.markdown("**Not urgent & not important**")
with s2:
    for t in u4:
        handle_task_checkbox(t)
