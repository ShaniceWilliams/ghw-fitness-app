import random
import streamlit as st
from yt_api import get_video_info
import database as dbs


@st.cache_resource()
def get_workouts():
    return dbs.all_workouts()


# def get_duration_text(duration):
#     seconds = duration % 60
#     minutes = int((duration / 60) % 60)
#     hours = int((duration / (60*60)) % 24)
#     text = ''
#     if hours > 0:
#         text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
#     else:
#         text += f'{minutes:02d}:{seconds:02d}'
#     return text


st.title("Find your Fitness")

menu_options = ("Today's workout", "All workouts", "Add workout")
selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "All workouts":
    st.markdown(f"## All workouts")
    workouts = get_workouts()
    for wo in workouts:
        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(f"{wo['channelTitle']}")

        ok = st.button('Delete workout?', key=wo["video_id"])
        if ok:
            dbs.delete_workout(wo["video_id"])
            st.cache_resource.clear()
            st.experimental_rerun()
        st.video(url)
    else:
        st.text("No workouts in Database")

elif selection == "Add workout":
    st.markdown(f"## Add workouts")


else:
    st.markdown(f"## Today's workouts")