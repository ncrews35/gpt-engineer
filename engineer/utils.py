File Name: app.py

```python
import subprocess
from .utils import prompt_string, prompt_confirm
from .repo import RepoConfig
from .engineer import Engineer, Workspace

temp_path = "./tmp/repo"


def main():
    repo = prompt_string("Repository URL:")
    base_branch = prompt_string("Base Branch:", default="mainline")
    dev_branch = prompt_string("Development Branch:", default="gpt-eng")
    path = prompt_string("Path to directory/file:", default="/")
    goal = prompt_string("Goal:")

    print("GETTING READY")

    subprocess.run(
        f"rm -r -f {temp_path}",
        shell=True,
        stdout=subprocess.PIPE
    )
    subprocess.run(
        script([
            f"git clone {repo} " + temp_path,
            f"cd {temp_path}",
            f"git fetch",
            f"git checkout {base_branch}",
            f"git pull origin {base_branch}",
            f"git checkout -b {dev_branch}",
            f"touch ./tmp/session.csv"
        ]),
        shell=True,
        stdout=subprocess.PIPE
    )

    print("GETTING TO WORK")

    repo = RepoConfig(temp_path)
    workspace = Workspace(
        path=temp_path + path,
        goal=goal,
        repo_name=repo.name,
        repo_description=repo.description,
        exclude_list=repo.exclude_list
    )
    engineer = Engineer(workspace)
    engineer.execute()

    print("FINISHED WORK")

    subprocess.run(
        script([
            f"cd {temp_path}",
            f"git add .",
            "git commit -m '[GPT] Generated Suggestions\n## Goal\n{0}\n\n#### Path: {1}'".format(
                goal, path),
            f"git push origin {dev_branch}"
        ]),
        shell=True,
        stdout=subprocess.PIPE
    )

    print("SUCCESS! Generation complete.")


def script(cmds: list[str]):
    return " && ".join(cmds)
```

File Name: engineer.py

```python
File Name: memory.py
```