import json
import requests


class PaperAPI:
    class BuildError(Exception):
        pass

    def __init__(self, version):
        self.endpoint = "https://papermc.io/api/v2/projects/paper/versions/" + version
        self.version = version
        r = requests.get(self.endpoint).content
        self.response = json.loads(r)

    def latest(self):
        lbuild = str(self.response['builds'][-1])
        return self.endpoint + "/builds/" + lbuild + "/downloads/paper-" + self.version + "-" + lbuild + ".jar"

    def build(self, nbuild):
        if nbuild in self.response['builds']:
            return self.endpoint + "/builds/" + str(nbuild) + "/downloads/paper-" + \
                   self.version + "-" + str(nbuild) + ".jar"
        else:
            raise PaperAPI.BuildError("Invalid build number")
