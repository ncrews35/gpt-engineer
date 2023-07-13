import yaml
import json

__all__ = ["RepoConfig"]

class RepoConfig:
    def __init__(self, path: str):
        with open(f"{path}/ai.yaml", 'r') as file:
            config = yaml.safe_load(file)
            self.name = config.get("name")
            self.description = config.get("description")
            self.exclude_list = config.get("exclude")

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)