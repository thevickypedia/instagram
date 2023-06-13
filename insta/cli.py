import os
import shutil
import subprocess
from typing import NoReturn, Tuple

import click
import requests
from instaloader import Instaloader, Profile, exceptions

from .config import env


def login() -> Tuple[Instaloader, Profile]:
    """Logs in to the instagram client using username and password stored as env vars.

    Returns:
        tuple:
        instagram module and profile information
    """
    client = Instaloader()
    client.login(user=env.insta_user, passwd=env.insta_pass)
    insta_profile = Profile.from_username(context=client.context, username=env.insta_user)
    return client, insta_profile


@click.group()
def main() -> NoReturn:
    """Initiates IG client. Takes username and password as arguments for authentication.

    >>> Instaloader

    Store your Instagram login credentials as env vars.

    export insta_user=<username>

    export insta_pass=<password>
    """


@main.command()
@click.option("--profile", prompt="Enter target profile name", help='Enter target username')
def dp(profile: str) -> NoReturn:
    """Gets display picture of a profile and saves it locally. Also asks for deletion post preview.

    Args:
        profile: User id of the profile for which the display picture has to be downloaded.
    """
    try:
        client, insta_profile = login()
    except exceptions.BadCredentialsException:
        click.secho(message='Credentials are invalid.', bold=True, fg='red')
        return
    except exceptions.InstaloaderException as error:
        click.secho(message=error.__str__(), bold=True, fg='red')
        return
    profile_ = Profile.from_username(context=client.context, username=profile)  # use target user to download the dp
    filename = f'{profile}.jpg'
    response = requests.get(profile_.get_profile_pic_url(), stream=True)
    response.raw.decode_content = True
    with open(filename, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
        file.close()
    subprocess.call(["open", filename])
    delete_res = input('Do you want to delete the picture? (Y/N)\n')
    if delete_res == 'y' or delete_res.lower() == 'yes':
        os.remove(filename)
        click.secho(message='Profile picture has been deleted.', fg='green')


@main.command()
def followers():
    """Prints followers' username and bio."""
    try:
        client, insta_profile = login()
    except exceptions.BadCredentialsException:
        click.secho(message='Credentials are invalid.', bold=True, fg='red')
        return
    except exceptions.InstaloaderException as error:
        click.secho(message=error.__str__(), bold=True, fg='red')
        return
    for follower in insta_profile.get_followers():
        if username := follower.username:
            click.secho(message=f'Username: {username}', fb='green')
        if bio := follower.biography:
            click.secho(message=f'Bio: {bio}', fb='green')


# noinspection PyUnresolvedReferences.
@main.command()
def followees():
    """Prints followees' username and bio."""
    try:
        client, insta_profile = login()
    except exceptions.BadCredentialsException:
        click.secho(message='Credentials are invalid.', bold=True, fg='red')
        return
    except exceptions.InstaloaderException as error:
        click.secho(message=error.__str__(), bold=True, fg='red')
        return
    for followee in insta_profile.get_followees():
        if username := followee.username:
            click.secho(message=f'Username: {username}', fb='green')
        if bio := followee.biography:
            click.secho(message=f'Bio: {bio}', fb='green')


@main.command()
@click.option("--them", is_flag=True, help="People who don't follow you back.")
@click.option("--me", is_flag=True, help="People who you don't follow back.")
def ungrateful(them: bool, me: bool):
    """Prints who don't follow you back and who you don't follow back.

    Args:
        them: Takes boolean value to retrieve people who don't follow you back.
        me: Takes boolean value to retrieve people who you don't follow back.
    """
    try:
        client, insta_profile = login()
    except exceptions.BadCredentialsException:
        click.secho(message='Credentials are invalid.', bold=True, fg='red')
        return
    except exceptions.InstaloaderException as error:
        click.secho(message=error.__str__(), bold=True, fg='red')
        return
    if them or me:
        followers_ = [follower.username for follower in insta_profile.get_followers()]
        followees_ = [followee.username for followee in insta_profile.get_followees()]

        if them:
            ug_them = [followee for followee in followees_ if followee not in followers_]
            click.secho(message=f'Ungrateful Them: {len(ug_them)}\n{sorted(ug_them)}', fb='green')

        if me:
            ug_me = [follower for follower in followers_ if follower not in followees_]
            click.secho(message=f'\n\nUngrateful Me: {len(ug_me)}\n{sorted(ug_me)}', fb='green')


if __name__ == '__main__':
    main()
