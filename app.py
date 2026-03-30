import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule  # Import your logic classes

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Owner & Pet Inputs ---
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize the Owner object (persist in session_state)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner

# Initialize pet (create new pet if the name is not already in session)
if "pets" not in st.session_state:
    st.session_state.pets = {}
if pet_name and pet_name not in st.session_state.pets:
    pet = Pet(name=pet_name, species=species)
    st.session_state.pets[pet_name] = pet
    # Also add pet to the owner's list (assuming Owner has a pets attribute)
    if not hasattr(owner, "pets"):
        owner.pets = []
    owner.pets.append(pet)

# --- Task Inputs ---
st.subheader("Add Tasks")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if pet_name:
        task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        st.session_state.tasks.append(task)
        # Add the task to the corresponding pet
        st.session_state.pets[pet_name].tasks.append(task)

# Display current tasks
if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([{"title": t.title, "duration": t.duration_minutes, "priority": t.priority} for t in st.session_state.tasks])
else:
    st.info("No tasks yet. Add one above.")

# --- Generate Schedule ---
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    schedule = Schedule(owner=owner, pet=st.session_state.pets[pet_name])
    schedule.build_from_tasks(st.session_state.tasks)
    st.markdown("### Today's Schedule")
    st.text(schedule.summary())