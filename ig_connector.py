def instagram():
    import os
    from instaloader import Instaloader, Profile
    client = Instaloader()
    insta_user, insta_pass = os.getenv('insta_user'), os.getenv('insta_pass')
    if not (insta_user or insta_pass):
        print('Store your Instagram login credentials in env variables')
        exit()
    client.login(insta_user, insta_pass)
    profile = Profile.from_username(client.context, insta_user)

    def followers():
        for follower in profile.get_followers():
            username = follower.username
            print(username)

    def followees():
        for follower in profile.get_followees():
            username = follower.username
            print(username)

    followees()
    followers()


instagram()
