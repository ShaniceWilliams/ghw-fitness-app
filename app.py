import random
import streamlit as st
from yt_api import get_video_info
import database as dbs
from datetime import date


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

email = st.text_input("To receive daily emails with the day's workout, enter your email address here: ")
if email:
    email_dict = {"email_id": email, "date_added": str(date.today())}
    dbs.add_email(email_dict)
    st.text("Email added to mailing list!")
    st.cache_resource.clear()

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
    st.write("Please note: the link follow the following format - https://youtu.be/video_id where"
            " video id is a mix of letters and numbers.")

    url = st.text_input('Enter the video url')
    if url:
        workout_data = get_video_info(url)
        if workout_data is None:
            st.text("Could not find video")
        else:
            st.text(workout_data['title'])
            st.text(workout_data['channelTitle'])
            st.video(url)
            if st.button("Add workout"):
                add = dbs.insert_workout(workout_data)
                st.text("Added workout!")
                st.cache_resource.clear()
                st.experimental_rerun()

else:
    st.markdown(f"## Today's workouts")

    workouts = get_workouts()
    if not workouts:
        st.text("No workouts in Database")
    else:
        wo = dbs.get_todays_workout()

        if not wo:
            workouts = get_workouts()
            n = len(workouts)
            index = random.randint(0, n - 1)
            wo = workouts[index]
            dbs.update_workout_today(wo, insert=True)
        else:
            wo = wo[0]

        if st.button("Choose another workout"):
            workouts = get_workouts()
            n = len(workouts)
            if n > 1:
                index = random.randint(0, n - 1)
                wo_new = workouts[index]
                while wo_new["video_id"] == wo["video_id"]:
                    index = random.randint(0, n - 1)
                    wo_new = workouts[index]
                wo = wo_new
                dbs.update_workout_today(wo)

        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(wo['channelTitle'])
        st.video(url)
