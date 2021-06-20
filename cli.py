from os import environ, remove
from shutil import copyfileobj
from subprocess import call

from click import group, option
from instaloader import Instaloader, Profile
from requests import get

if (insta_user := environ.get('insta_user')) and (insta_pass := environ.get('insta_pass')):
    client = Instaloader()
    client.login(user=insta_user, passwd=insta_pass)
    insta_profile = Profile.from_username(client.context, insta_user)
else:
    exit("Store your Instagram login credentials as env vars.\n"
         "export insta_user=<username>\nexport insta_pass=<password>")


@group()
def main():
    """Initiates IG client. Takes username and password as arguments for authentication.
    >>> Instaloader
    """


# noinspection PyUnresolvedReferences
@main.command()
@option("--target-profile", prompt="Enter target profile name", help='Enter target username')
def dp(target_profile):
    """Gets display picture of a profile and saves it locally. Also asks for deletion post preview.

    Args:
        target_profile: User id of the profile for which the display picture has to be downloaded.

    """
    profile_ = Profile.from_username(client.context, target_profile)  # use target user here to download the dp
    filename = f'{target_profile}.jpg'
    response = get(profile_.get_profile_pic_url(), stream=True)
    response.raw.decode_content = True
    with open(filename, 'wb') as file:
        copyfileobj(response.raw, file)
        file.close()
    call(["open", filename])
    delete_res = input('Do you want to delete the picture? (Y/N)\n')
    if delete_res == 'y' or delete_res.lower() == 'yes':
        remove(filename)
        print('Profile picture has been deleted.')


# noinspection PyUnresolvedReferences
@main.command()
def followers():
    """Prints followers' username and bio."""
    for follower in insta_profile.get_followers():
        if username := follower.username:
            print(f'Username: {username}')
        if bio := follower.biography:
            print(f'Bio: {bio}')


# noinspection PyUnresolvedReferences
@main.command()
def followees():
    """Prints followees' username and bio."""
    for followee in insta_profile.get_followees():
        if username := followee.username:
            print(f'Username: {username}')
        if bio := followee.biography:
            print(f'Bio: {bio}')


# noinspection PyUnresolvedReferences
@main.command()
@option("--them", default=False, help="People who don't follow you back.")
@option("--me", default=False, help="People who you don't follow back.")
def ungrateful(them, me):
    """Prints who don't follow you back and who you don't follow back.

    Args:
        them: Takes boolean value to retrieve people who don't follow you back.
        me: Takes boolean value to retrieve people who you don't follow back.

    """
    if them or me:
        followers_ = [follower.username for follower in insta_profile.get_followers()]
        followees_ = [followee.username for followee in insta_profile.get_followees()]

        if them:
            ug_them = [followee for followee in followees_ if followee not in followers_]
            print(f'Ungrateful Them: {len(ug_them)}\n{sorted(ug_them)}')

        if me:
            ug_me = [follower for follower in followers_ if follower not in followees_]
            print(f'\n\nUngrateful Me: {len(ug_me)}\n{sorted(ug_me)}')


if __name__ == '__main__':
    main()
