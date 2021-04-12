from os import environ, remove
from shutil import copyfileobj
from subprocess import call

from instaloader import Instaloader, Profile
from requests import get


class Instagram:
    def __init__(self):
        self.client = Instaloader()
        insta_user, insta_pass = environ.get('insta_user'), environ.get('insta_pass')
        if not (insta_user or insta_pass):
            print("Store your Instagram login credentials in env variables.\n"
                  "'insta_user=<username>'\n'insta_pass=<password>'")
            exit()
        self.client.login(insta_user, insta_pass)
        self.profile = Profile.from_username(self.client.context, insta_user)

    def dp(self, target_profile):
        profile = Profile.from_username(self.client.context, target_profile)  # use target user here to download the dp
        filename = f'{target_profile}.jpg'
        response = get(profile.get_profile_pic_url(), stream=True)
        response.raw.decode_content = True
        with open(filename, 'wb') as file:
            copyfileobj(response.raw, file)
            file.close()
        call(["open", filename])
        delete_res = input('Do you want to delete the picture? (Y/N)\n')
        if delete_res == 'y' or delete_res.lower() == 'yes':
            remove(filename)
            print('Profile picture has been deleted.')

    def followers(self):
        for follower in self.profile.get_followers():
            username = follower.username
            print(username)

    def followees(self):
        for followee in self.profile.get_followees():
            username = followee.username
            print(username)

    def post_info(self, tagged=False):
        if tagged:
            posts = self.profile.get_tagged_posts()
        else:
            posts = self.profile.get_posts()
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
            extension = '.jpg'

            if post.is_video:
                extension = '.mp4'
                view_count = post.video_view_count
                url = post.video_url
                video_duration = post.video_duration
                print(f'Views: {view_count}') if view_count else None
                print(f'Duration: {video_duration}') if video_duration else None

            response = get(url, stream=True)
            response.raw.decode_content = True
            filename = f'{str(date_local).replace(" ", "_") + extension}'
            with open(filename, 'wb') as file:
                copyfileobj(response.raw, file)
                file.close()
            call(["open", filename])

            print(f'Title: {title}') if title else None
            print(f'Caption: {caption}') if caption else None
            print(f'Profile: {profile}') if profile else None
            print(f'Likes: {likes}') if likes else None
            print(f'Comments: {comments}') if comments else None
            print(f'Tagged: {", ".join(tagged_users)}') if tagged_users else None
            print(f'Hashtags: {"#" + ", #".join(hashtags)}') if hashtags else None
            print(f'Mentions: {"@" + ", @".join(mentions)}') if mentions else None
            print(f'Date: {date_local}')
            print(f'Location: {location}') if location else None
            print('\n')


if __name__ == '__main__':
    Instagram().dp(target_profile='vignesh.vikky')
    Instagram().post_info(tagged=False)
    Instagram().post_info(tagged=True)
