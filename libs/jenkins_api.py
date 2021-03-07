import json
import requests
import re


class JenkinsAPI:
    class BuildError(Exception):
        pass

    def __init__(self, endpoint):
        self.endpoint = endpoint + "/lastSuccessfulBuild/api/json?pretty=true"
        r = requests.get(self.endpoint).content
        self.response = json.loads(r)

    def latest(self, keyword):
        buildendpoint = None
        for i in self.response['artifacts']:
            if re.search(keyword, i['displayPath']):
                if "api/json?pretty=true" in self.endpoint:
                    buildendpoint = self.endpoint.replace("api/json?pretty=true", "artifact/" + i['relativePath'])
                elif "api/json" in self.endpoint:
                    buildendpoint = self.endpoint.replace("api/json", "artifact/" + i['relativePath'])
                else:
                    raise JenkinsAPI.BuildError("Invalid endpoint, need JSON")
        if buildendpoint is None:
            raise JenkinsAPI.BuildError("Keyword not found")
        return buildendpoint
