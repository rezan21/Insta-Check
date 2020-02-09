def get_user_stat(followings_obj, followers_obj):
    
    followings_usernames = [followings_obj['users'][i]["username"] for i,j in enumerate(followings_obj['users'])]
    followers_usernames = [followers_obj['users'][i]["username"] for i,j in enumerate(followers_obj['users'])]
    
    mutual_following = []
    i_dont_follow = []
    they_dont_follow = []

    for follower in followers_usernames:
        if follower in followings_usernames:
            mutual_following.append(follower)
        else:
            i_dont_follow.append(follower)

    for following in followings_usernames:
        if following not in followers_usernames:
            they_dont_follow.append(following)

    return {"followings":followings_usernames,
            "followers":followers_usernames,
            "mutuals":mutual_following,
            "i_dont_follow_back":i_dont_follow,
            "they_dont_follow_back":they_dont_follow}

def get_ff_objs(api, userId, token):
    followings_obj = api.user_following(userId, token)
    followers_obj = api.user_followers(userId, token)
    return([followings_obj,followers_obj])

def testFun():
    print("hey bitch")