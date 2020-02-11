import streamlit as st
import altair as alt
from instagram_private_api import Client, ClientCompatPatch
import instaHandler
import pandas as pd
import plotly.express as px


username = st.text_input("User (i.e: Username/Email)")
password = st.text_input("Password", type="password")
submitBtn = st.checkbox("Log In/Out")

if submitBtn:
    print("running again!")
    with st.spinner("Verifying ..."):
        try:
            api = Client(username, password)
            mainToken = str(api.generate_uuid())
            mainUserID = api.authenticated_user_id
            user = api.authenticated_user_name
            st.success(f"Successfuly logged in as {user}")

            st.title("Dashboard")
            st.header("Analysis:")
            st.markdown("""<div><span>Here you can find out which accounts are not following you back, or you are not following them back.</span><div> """, unsafe_allow_html=True)
       
            def quick_ff_objs(userId=mainUserID, api=api, token=mainToken):
                return(instaHandler.get_ff_objs(api=api, userId=userId, token=token))
            flwing_obj, flwer_obj = quick_ff_objs()

            user_stat = instaHandler.get_user_stat(flwing_obj, flwer_obj)
            main_followers = len(user_stat["followers"])
            main_followings = len(user_stat["followings"])
            main_mutuals = user_stat["mutuals"]
            main_i_dont_follow_back = user_stat["i_dont_follow_back"]
            main_they_dont_follow_back = user_stat["they_dont_follow_back"]
            flwing_privates = 0
            flwing_verifieds = 0
            flwer_privates = 0
            flwer_verifieds = 0

            for i,j in enumerate(flwing_obj["users"]):
                private = flwing_obj["users"][i]["is_private"]
                verified = flwing_obj["users"][i]["is_verified"]
                if private: flwing_privates += 1
                if verified: flwing_verifieds += 1
            for i,j in enumerate(flwer_obj["users"]):
                private = flwer_obj["users"][i]["is_private"]
                verified = flwer_obj["users"][i]["is_verified"]
                if private: flwer_privates += 1
                if verified: flwer_verifieds += 1
            # privacy stat:
            dic1 = {
            "status":["Followings", "Followings", "Followers", "Followers"],
            "Privacy" : ["Private", "Public","Private", "Public"],
            "count" : [
                flwing_privates,
                (main_followings - flwing_privates),
                flwer_privates,
                (main_followers - flwer_privates)
                ]}
            df1 = pd.DataFrame(dic1)
            fig1 = px.bar(df1, x="status", y="count", color='Privacy', width=630, color_discrete_sequence=["#f63266","#fcc4d3"])
            # verification stat:
            dic2 = {
            "status":["Followings", "Followings", "Followers", "Followers"],
            "Verification" : ["Verified", "Not Verified","Verified", "Not Verified"],
            "count" : [
                flwing_verifieds,
                (main_followings - flwing_verifieds),
                flwer_verifieds,
                (main_followers - flwer_verifieds)
                ]}
            df2 = pd.DataFrame(dic2)
            # graphs
            fig2 = px.bar(df2, x="status", y="count", color='Verification',width=630, color_discrete_sequence=["#f63266","#fcc4d3"])
            y_style = dict(title='No. of Accounts', titlefont_size=16, tickfont_size=14)
            x_style = dict(title='Status (i.e: Followings/Followers)', titlefont_size=16, tickfont_size=14)
            leg_style = dict(x=1.0, y=1.0, bgcolor='#fff',bordercolor='#f63266')
            fig1.update_layout(
                title='Accounts Privacy Aspect',
                xaxis=x_style,
                yaxis=y_style,
                legend=leg_style)
            fig1.layout.plot_bgcolor="#fff"
            fig2.update_layout(
                title='Accounts Verification Aspect',
                xaxis=x_style,
                yaxis=y_style,
                legend=leg_style)
            fig2.layout.plot_bgcolor="#fff"

            st.text(f"Followings: {main_followings}")
            st.text(f"Followers: {main_followers}")
            st.text(f"Mutuals: {len(main_mutuals)}")
            st.text(f"You're Not Following Back: {len(main_i_dont_follow_back)}")
            st.text(main_i_dont_follow_back)
            st.text(f"They're Not Following Back: {len(main_they_dont_follow_back)}")
            st.text(main_they_dont_follow_back)


            st.header("Charts:")
            st.write(fig1)
            st.write(fig2)

        except Exception as e:
            st.error(e)

