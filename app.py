import streamlit as st
import altair as alt
from instagram_private_api import Client, ClientCompatPatch
import instaHandler


logged_in  = False
user_field = st.empty()
pass_field = st.empty()
loginBtn = st.empty()
logoutBtn = st.empty()

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
    user_field.empty() # clean up
    pass_field.empty()
    loginBtn.empty()
    logoutBtn = logoutBtn.button("Log Out")
    ## functions ##

    def get_following_followers_obj(user=mainUserID, token=mainToken):
        followings_obj = api.user_following(user, token)
        followers_obj = api.user_followers(user, token)
        return([followings_obj,followers_obj])

    st.success(f"Successfuly logged in as {user}")
    st.title("Dashboard")

    main_user_stat = instaHandler.get_user_stat(get_following_followers_obj()[0],get_following_followers_obj()[1])
    st.write(main_user_stat["followers"])

    #import someModule
    #instaHandler.init(the_authd_user)


    #instaHandler.testFun()




    # submitBtn.button("Log Out")
    # if submitBtn:
    #     logged_in = False


# if not logged_in:
#     showLogin()
#     logged_in = changeLogState()

# if logged_in:
#     showDashboard()

