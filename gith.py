#!/usr/bin/env python3

import requests, json, subprocess, os, re, webbrowser, sys
from os import path

config_path = path.expanduser('~/.config/gith')

user_auth = ('', '')
username = ''

def init():

    # load username, email and access token from config file if it
    # exists, otherwise we ask the user for email and access token
    # and fetch the username.
    if path.exists(config_path):

        # reads an <e-mail> <personal access token> <username> combo in the following format
        # email@email.com abe5d7edafi564da84dasf45648asd5s4d4fa5aa UserName
        f = open(config_path)

        creds = f.read().split(' ', 2)

        f.close()
        
        user_auth = (creds[0], creds[1])
        username = creds[2]

        return (user_auth, username)

    else:

        email = input('Insert your e-mail: ')
        token = input('Insert a GitHub personal access token: ')

        user_auth = (email, token)

        response = requests.get('https://api.github.com/user', auth = user_auth)

        if response.status_code == 200:

            username = response.json()['login']

            f = open(config_path, 'x')

            # save email, access token, and username
            f.write(f'{email} {token} {username}')

            f.close()

            return (user_auth, username)

def list_repos(user_auth):

    response = requests.get('https://api.github.com/user/repos?sort=created', auth = user_auth)

    if response.status_code == 200:
        json = response.json()

        for repo in json:
            print(repo['html_url'])



def clone_repo(username, repo_name):
    subprocess.check_call(['git', 'clone', f'https://github.com/{username}/{repo_name}'])




def view_curr_repo():

    try:
        out = subprocess.check_output(['git', 'remote', 'show', 'origin', '-n'], text = True)

        match = re.search('Fetch URL: (.+)', out.splitlines()[1])
        if match != None:
            url = match.group(1)
            webbrowser.open_new_tab(url)
        else:
            print('Could not figure out the URL of the origin remote')
    
    except:
        print('Not a git repository.')


def create_repo(user_auth, username, private):

    # get the name of the current working directory
    working_dir_name = os.getcwd().split('/')[-1]

    request_body = {
        'name': working_dir_name,
        'private': private,
        'auto_init': False,
    }

    response = requests.post('https://api.github.com/user/repos',
        auth = user_auth,
        json = request_body
    )

    if True or response.status_code == 201:
        print('Create successful.')

        repo_url = response.json()['html_url']

        subprocess.check_output(['git', 'remote', 'add', 'origin', repo_url])
        subprocess.check_output(['git', 'push', '--set-upstream',  'origin', 'master'])


    else:
        print('Failed to create repo.')
        print(response.status_code)
        print(response.text)

if __name__ == '__main__':

    (user_auth, username) = init()

    if len(sys.argv) >= 2:

        if sys.argv[1] == 'list':
            list_repos(user_auth)

        elif sys.argv[1] == 'clone' and len(sys.argv) >= 3:
            clone_repo(username, sys.argv[2])

        elif sys.argv[1] == 'view':
            view_curr_repo()

        elif sys.argv[1] == 'create':
            create_repo(user_auth, username, len(sys.argv) >= 3 and (sys.argv[2] == '-p' or sys.argv[2] == '--private'))