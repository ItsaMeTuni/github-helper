# gith

`gith` is a very simple command-line tool to view and create GitHub repositories.

To install it just copy the `gith` file to somewhere in your computer and add it to the `PATH` environment variable. I put it on `~/scripts/gith`, for example.

I only tested this on Ubuntu, so idk if it works on Windows, Mac or any other linux distro (it probably does, but it _might_ not).

**IMPORTANT:** I made this script for myself only. If the script somehow fucks up your shit I do not take responsibility for it. **You are on your own and executing this at your own risk.** Also, before running a command, please read its description below so you don't make easily avoidable mistakes.

## First run

When you first run this script it will ask you for your gh account email and a _personal access token_. You can get a personal access token by going into GitHub settings > Developer Settings > Personal access tokens and creating a token with the `repo` and `user` permissions.

The script will store the email, the token and your username in the file `~/.config/gith`.

If you end up changing your github username you have to delete the `~/.config/gith` file and run the script again so it can update the username cache.

## Commands

### List repositories

Show a list of all GitHub repositories you own.

```
gith list
```

### View repository

If the current working directory is a git repository, you can run the following to open the project's GitHub page in the browser:

```
gith view
```

### Create repository

If the current working directory is a git repository, you can run the following to create a GitHub repository with the same name as the working directory:

```
gith create
```

If you want a private repository use the `-p` or `--private` flag.

```
gith create -p
```

This command creates a gh repository with the same name as the current directory and, immediately after, executes `git remote add origin` and then `git push --set-upstream origin master`.

For example, if the current working directory is `my-project` a repository at `github.com/username/my-project` will be created.

### Clone

Clones a gh repository.

```
gith clone <repo name>
```

It will run `git clone https://github.com/username/reponame`

### Help

Shows some help information about `gith`.

```
gith help
```