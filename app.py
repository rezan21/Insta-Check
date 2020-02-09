import streamlit as st
import altair as alt
from instagram_private_api import Client, ClientCompatPatch
import instaHandler


logged_in  = False
user_field = st.empty()
pass_field = st.empty()
loginBtn = st.empty()
logoutBtn = st.empty()
chBox = st.empty()
if not logged_in:
    username = user_field.text_input("User (i.e: Username/Email)")
    password = pass_field.text_input("Password", type="password")
    submitBtn = loginBtn.button("Log In")
    if submitBtn:
        with st.spinner("Verifying ..."):
            try:
                api = Client(username, password)
                mainToken = str(api.generate_uuid())
                mainUserID = api.authenticated_user_id
                user = api.authenticated_user_name
                #user = "rey"
                logged_in = True

            except Exception as e:
                st.error(e)

if logged_in:
    # clean up
    user_field.empty() 
    pass_field.empty()
    loginBtn.empty()
    logoutBtn = logoutBtn.button("Log Out")
    st.success(f"Successfuly logged in as {user}")
    st.title("Dashboard")

    def quick_ff_objs(userId=mainUserID, api=api, token=mainToken):
        return(instaHandler.get_ff_objs(api=api, userId=userId, token=token))

    flwing_obj, flwer_obj = quick_ff_objs()
    user_stat = instaHandler.get_user_stat(flwing_obj, flwer_obj)
    main_followers = user_stat["followers"]
    main_followings = user_stat["followings"]
    main_mutuals = user_stat["mutuals"]
    main_i_dont_follow_back = user_stat["i_dont_follow_back"]
    main_they_dont_follow_back = user_stat["they_dont_follow_back"]
    user_id_dict = {}
    for user in flwing_obj["users"]:
        user_id_dict.update({user['username']:user['pk']})
    friends = list(user_id_dict.keys())

    st.header("Analysis:")
    st.subheader(f"Followings: {len(main_followings)}")
    st.subheader(f"Followers: {len(main_followers)}")
    st.subheader(f"Mutuals: {len(main_mutuals)}")
    st.subheader(f"You're Not Following Back: {len(main_i_dont_follow_back)}")
    st.subheader(f"They're Not Following Back: {len(main_they_dont_follow_back)}")

    st.header("Stalking:")
