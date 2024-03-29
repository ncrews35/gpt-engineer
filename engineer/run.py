import json
import subprocess
from .repo import RepoConfig
from .engineer import Engineer, Workspace

__all__ = ["Configuration", "run"]


class Configuration:
    def __init__(
        self,
        repository_url: str,
        base_branch: str,
        dev_branch: str,
        path: str,
        goal: str,
        bot_name: str = None,
        bot_email: str = None,
        access_token: str = None,
    ):
        """
        Initializes the Configuration class.

        Parameters:
        repository_url (str): The URL of the repository.
        base_branch (str): The base branch of the repository.
        dev_branch (str): The development branch of the repository.
        path (str): The path to the file in the repository.
        goal (str): The goal for the GPT Engineer.
        bot_name (str): The name of the bot.
        bot_email (str): The email of the bot.
        access_token (str): The access token for the repository.
        """

        if access_token:
            self.repository_url = repository_url.replace(
                "https://", f"https://{access_token}@"
            )
        else:
            self.repository_url = repository_url
        self.base_branch = base_branch
        self.dev_branch = dev_branch
        self.path = path
        self.goal = goal
        self.bot_name = bot_name
        self.bot_email = bot_email


def run(configuration: Configuration):
    temp_path = "/tmp/repo"

    print("GETTING READY")

    subprocess.run(f"rm -r -f {temp_path}", shell=True, stdout=subprocess.PIPE)

    if configuration.bot_name and configuration.bot_email:
        subprocess.run(
            script(
                [
                    f"cd {temp_path}",
                    f'git config user.name "{configuration.bot_name}"',
                    f'git config user.email "{configuration.bot_email}"',
                ]
            ),
            shell=True,
            stdout=subprocess.PIPE,
        )

    subprocess.run(
        script(
            [
                f"git clone {configuration.repository_url} " + temp_path,
                f"cd {temp_path}",
                f"git fetch",
                f"git checkout {configuration.base_branch}",
                f"git pull origin {configuration.base_branch}",
                f"git checkout -b {configuration.dev_branch}",
                f"touch /tmp/session.csv",
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
    )

    print("GETTING TO WORK")

    repo = RepoConfig(temp_path)
    engineer = Engineer(
        Workspace(
            path=temp_path + configuration.path,
            goal=configuration.goal,
            repo_name=repo.name,
            repo_description=repo.description,
            exclude_list=repo.exclude_list,
        )
    )

    engineer.execute()

    print("FINISHED WORK")

    config_cmds = []
    if configuration.bot_name and configuration.bot_email:
        config_cmds = [
            f'git config user.name "{configuration.bot_name}"',
            f'git config user.email "{configuration.bot_email}"',
        ]

    subprocess.run(
        script(
            [
                f"cd {temp_path}",
                *config_cmds,
                f"git add .",
                "git commit -m '[GPT] Generated Suggestions\nThis code was auto generated by AI.'",
                "git push {0} {1} -f".format(
                    configuration.repository_url, configuration.dev_branch
                ),
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
    )

    print("SUCCESS! Generation complete.")


def script(cmds):
    return " && ".join(cmds)
