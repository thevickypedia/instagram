import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import NoReturn

import requests
from instaloader import Instaloader, Profile

from .config import env


class Instagram:
    """Initiates IG client. Takes username and password as arguments for authentication.

    >>> Instagram

    Args:
        insta_user: Username for the authentication instagram account.
        insta_pass: Password for the authentication instagram account.
    """

    def __init__(self, insta_user: str = env.insta_user, insta_pass: str = env.insta_pass):
        self.client = Instaloader()
        self.client.login(insta_user, insta_pass)
        self.profile = Profile.from_username(self.client.context, insta_user)

    def dp(self, target_profile: str) -> NoReturn:
        """Gets display picture of a profile and saves it locally. Also asks for deletion post preview.

        Args:
            target_profile: User id of the profile for which the display picture has to be downloaded.
        """
        profile = Profile.from_username(self.client.context, target_profile)  # use target user here to download the dp
        filename = f'{target_profile}.jpg'
        response = requests.get(profile.get_profile_pic_url(), stream=True)
        response.raw.decode_content = True
        with open(filename, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
            file.close()
        subprocess.call(["open", filename])
        delete_res = input('Do you want to delete the picture? (Y/N)\n')
        if delete_res == 'y' or delete_res.lower() == 'yes':
            os.remove(filename)
            print('Profile picture has been deleted.')

    def followers(self) -> NoReturn:
        """Prints followers' username and bio."""
        for follower in self.profile.get_followers():
            username = follower.username
            bio = follower.biography
            print(f'Username: {username}') if username else None
            print(f'Bio: {bio}') if bio else None

    def followees(self) -> NoReturn:
        """Prints followees' username and bio."""
        for followee in self.profile.get_followees():
            username = followee.username
            bio = followee.biography
            print(f'Username: {username}') if username else None
            print(f'Bio: {bio}') if bio else None

    def post_info(self, tagged: bool = True) -> NoReturn:
        """Prints information of posts.

        Gets tagged posts' information when 'tagged' is set to True
        Gets self post information when 'tagged' flag is not used

        Args:
            tagged: Takes boolean value as argument. Set to False by default.
        """
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

            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            filename = f'{str(date_local).replace(" ", "_") + extension}'
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
                file.close()
            subprocess.call(["open", filename])

            print(f'Profile: {profile}') if profile else None
            if tagged:
                username = post.owner_username
                print(f'Username: {username}') if username else None
            print(f'Title: {title}') if title else None
            print(f'Caption: {caption}') if caption else None
            print(f'Likes: {likes}') if likes else None
            print(f'Comments: {comments}') if comments else None
            print(f'Tagged: {", ".join(tagged_users)}') if tagged_users else None
            print(f'Hashtags: {"#" + ", #".join(hashtags)}') if hashtags else None
            print(f'Mentions: {"@" + ", @".join(mentions)}') if mentions else None
            print(f'Date: {date_local}')
            print(f'Location: {location}') if location else None
            print('\n')

    @staticmethod
    def followers_thread(follower: Profile) -> NoReturn:
        """Takes follower's profile data as input and prints their username and bio.

        Args:
            follower: Takes follower profile data as argument.
        """
        username = follower.username
        bio = str(follower.biography).replace('\n', '\t')
        if username and bio:
            print(f'Username: {username}\tBio: {bio}')
        else:
            print(f'Username: {username}')

    def followers_threaded(self) -> NoReturn:
        """Get followers' information concurrently.

        Initiates Instagram().followers_thread() in a multi-threaded execution.
        Set max_workers to 5 as anything exceeding 10 will block the origin IP range for 10 minutes.

        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.followers_thread, self.profile.get_followers())

    @staticmethod
    def following_thread(followee: Profile) -> NoReturn:
        """Takes following people's profile data as input and prints their username and bio.

        Args:
            followee: Take followee profile data as argument.
        """
        username = followee.username
        bio = str(followee.biography).replace('\n', '\t')
        if username and bio:
            print(f'Username: {username}\tBio: {bio}')
        else:
            print(f'Username: {username}')

    def following_threaded(self) -> NoReturn:
        """Get followees' information concurrently.

        Initiates Instagram().following_thread() in a multi-threaded execution.
        Set max_workers to 5 as anything exceeding 10 will block the origin IP range for 10 minutes.
        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.following_thread, self.profile.get_followees())

    def ungrateful(self) -> NoReturn:
        """Prints who doesn't follow you back and who you don't follow back."""
        followers = [follower.username for follower in self.profile.get_followers()]
        followees = [followee.username for followee in self.profile.get_followees()]
        ug_them = [followee for followee in followees if followee not in followers]
        print(f'Ungrateful Them: {len(ug_them)}')
        print(sorted(ug_them))

        ug_me = [follower for follower in followers if follower not in followees]
        print(f'\n\nUngrateful Me: {len(ug_me)}')
        print(sorted(ug_me))
