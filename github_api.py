import json
import requests


class GitHubAPI:
    class BuildError(Exception):
        pass

    def __init__(self, repo):
        self.endpoint = "https://api.github.com/repos/" + repo + "/releases/latest"
        r = requests.get(self.endpoint).content
        self.response = json.loads(r)

    def latest(self, keyword):
        for i in self.response["assets"]:
            if keyword is None:
                return i["browser_download_url"]
            elif keyword in i["browser_download_url"]:
                return i["browser_download_url"]
        raise GitHubAPI.BuildError("Keyword not found")
