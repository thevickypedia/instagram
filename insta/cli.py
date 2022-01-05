from os import environ, path, remove
from shutil import copyfileobj
from subprocess import call

import requests
from click import group, option, secho
from dotenv import load_dotenv
from instaloader import Instaloader, Profile, exceptions

if path.isfile('.env'):
    load_dotenv(dotenv_path='.env', verbose=True, override=True)


class InstagramCLI:
    """Class for documentation.

    >>> InstagramCLI

    Methods:
        main
            References:
                >>> main

            Initiates IG client. Takes username and password as arguments for authentication.

            - Shows the help message:
                ``Store your Instagram login credentials as env vars.``

                ``export insta_user=<username>``

                ``export insta_pass=<password>``

        dp
            References:
                >>> dp

            Gets display picture of a profile and saves it locally. Also asks for deletion post preview.

            Args:
                - target_profile: User id of the profile for which the display picture has to be downloaded.

            Yields:
                Profile picture of the targeted profile

            Examples:
                ``insta dp --profile vignesh.vikky``

        followers
            References:
                >>> followers

            Prints followers' username and bio.

            Examples:
                ``insta followers``

        followees
            References:
                >>> followees

            Prints followees' username and bio.

            Examples:
                ``insta followees``

        ungrateful
            References:
                >>> ungrateful

            Prints who don't follow you back and who you don't follow back.

            Args:
                - them: Takes boolean value to retrieve people who don't follow you back.
                - me: Takes boolean value to retrieve people who you don't follow back.

            Examples:
                ``insta ungrateful --them``

                ``insta ungrateful --me``

    """

    @staticmethod
    def login() -> tuple:
        """Logs in to the instagram client using username and password stored as env vars.

        Returns:
            tuple:
            instagram module and profile information
        """
        if (insta_user := environ.get('insta_user')) and (insta_pass := environ.get('insta_pass')):
            client = Instaloader()
            client.login(user=insta_user, passwd=insta_pass)
            insta_profile = Profile.from_username(client.context, insta_user)
            return client, insta_profile
        else:
            exit("Store your Instagram login credentials as env vars.\n"
                 "export insta_user=<username>\nexport insta_pass=<password>")


@group()
def main() -> None:
    """Initiates IG client. Takes username and password as arguments for authentication.

    >>> Instaloader

    Store your Instagram login credentials as env vars.

    export insta_user=<username>

    export insta_pass=<password>
    """


@main.command()
@option("--profile", prompt="Enter target profile name", help='Enter target username')
def dp(profile) -> None:
    """Gets display picture of a profile and saves it locally. Also asks for deletion post preview.

    Args:
        profile: User id of the profile for which the display picture has to be downloaded.
    """
    try:
        client, insta_profile = InstagramCLI.login()
    except exceptions.BadCredentialsException:
        secho(message='Credentials are invalid.', bold=True, fg='red')
        return
    profile_ = Profile.from_username(client.context, profile)  # use target user here to download the dp
    filename = f'{profile}.jpg'
    response = requests.get(url=profile_.get_profile_pic_url(), stream=True)
    response.raw.decode_content = True
    with open(filename, 'wb') as file:
        copyfileobj(response.raw, file)
        file.close()
    call(["open", filename])
    delete_res = input('Do you want to delete the picture? (Y/N)\n')
    if delete_res == 'y' or delete_res.lower() == 'yes':
        remove(filename)
        secho(message='Profile picture has been deleted.', fg='green')


@main.command()
def followers():
    """Prints followers' username and bio."""
    client, insta_profile = InstagramCLI.login()
    for follower in insta_profile.get_followers():
        if username := follower.username:
            secho(message=f'Username: {username}', fb='green')
        if bio := follower.biography:
            secho(message=f'Bio: {bio}', fb='green')


# noinspection PyUnresolvedReferences.
@main.command()
def followees():
    """Prints followees' username and bio."""
    client, insta_profile = InstagramCLI.login()
    for followee in insta_profile.get_followees():
        if username := followee.username:
            secho(message=f'Username: {username}', fb='green')
        if bio := followee.biography:
            secho(message=f'Bio: {bio}', fb='green')


@main.command()
@option("--them", is_flag=True, help="People who don't follow you back.")
@option("--me", is_flag=True, help="People who you don't follow back.")
def ungrateful(them, me):
    """Prints who don't follow you back and who you don't follow back.

    Args:
        them: Takes boolean value to retrieve people who don't follow you back.
        me: Takes boolean value to retrieve people who you don't follow back.
    """
    client, insta_profile = InstagramCLI.login()
    if them or me:
        followers_ = [follower.username for follower in insta_profile.get_followers()]
        followees_ = [followee.username for followee in insta_profile.get_followees()]

        if them:
            ug_them = [followee for followee in followees_ if followee not in followers_]
            print(f'Ungrateful Them: {len(ug_them)}\n{sorted(ug_them)}')

        if me:
            ug_me = [follower for follower in followers_ if follower not in followees_]
            print(f'Ungrateful Me: {len(ug_me)}\n{sorted(ug_me)}')


if __name__ == '__main__':
    main()
