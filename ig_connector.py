def instagram():
    import os
    from instaloader import Instaloader, Profile
    import requests
    import shutil
    import subprocess
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

    def dp(target_profile):
        profile = Profile.from_username(client.context, target_profile)  # use target user here to download the dp
        filename = f'{target_profile}.jpg'
        response = requests.get(profile.get_profile_pic_url(), stream=True)
        response.raw.decode_content = True
        with open(filename, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
            file.close()
        subprocess.call(["open", filename])

    def post_info(tagged=False):
        if tagged:
            posts = profile.get_tagged_posts()
        else:
            posts = profile.get_posts()
        for post in posts:
            profile = post.profile
            location = post.location
            url = post.url
            title = post.title
            caption = post.caption
            hashtags = post.caption_hashtags
            mentions = post.caption_mentions
            comments = post.comments
            date_local = post.date_local
            likes = post.likes
            tagged_users = post.tagged_users
            print(profile, location, title, caption, hashtags, mentions, comments, likes, tagged_users)

            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            filename = f'{str(date_local).replace(" ", "_")}'
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
                file.close()
            subprocess.call(["open", filename])

    followees()
    followers()
    dp('vignesh.vikky')
    post_info(tagged=True)


instagram()
