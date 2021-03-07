from os import mkdir
from os.path import exists
from shutil import rmtree, copyfile, make_archive
from libs.paper_api import PaperAPI
from urllib.request import urlretrieve
from libs.jenkins_api import JenkinsAPI
from libs.github_api import GitHubAPI


class Deploy:
    def __init__(self, cfg, build_number, job_cfg):
        self.cfg = cfg
        self.build_number = build_number
        self.job_folder = cfg['jobs_directory'] + "/" + build_number
        self.job_cfg = job_cfg
        print("Preparing build directories...")
        if not exists(cfg['jobs_directory']):
            mkdir(cfg['jobs_directory'])
        if exists(self.job_folder):
            print("Build already exists! Overriding.")
            rmtree(self.job_folder)
        mkdir(self.job_folder)
        mkdir(self.job_folder + "/plugins")

    def prepare_server(self):
        api = PaperAPI(self.job_cfg['version'])
        print("Resolving build info from PaperAPI...")
        if self.job_cfg['paper_build'] == "latest":
            url = api.latest()
        else:
            url = api.build(self.job_cfg['paper_build'])
        print("Downloading the Paper jar... This may take a while.")
        urlretrieve(url, self.job_folder + "/paper.jar")
        print("Copying files...")
        copyfile("libs/eula.txt", self.job_folder + "/eula.txt")
        copyfile(self.job_cfg['properties'], self.job_folder + "/server.properties")

    def resolve_deps(self):
        print("Resolving dependencies...")
        for i in self.job_cfg['dependencies']:
            print("Getting " + i + "...")
            if self.job_cfg['dependencies'][i]["jenkins"] is not False and self.job_cfg['dependencies'][i]["jenkins"][0] is True:
                api = JenkinsAPI(self.job_cfg['dependencies'][i]["url"])
                url = api.latest(self.job_cfg['dependencies'][i]["jenkins"][-1])
                urlretrieve(url, self.job_folder + "/plugins/" + i + ".jar")
            elif self.job_cfg['dependencies'][i]["github"] is not False and self.job_cfg['dependencies'][i]["github"][0] is True:
                api = GitHubAPI(self.job_cfg['dependencies'][i]["url"])
                if self.job_cfg['dependencies'][i]["github"][-1] is None:
                    url = api.latest(None)
                else:
                    url = api.latest(self.job_cfg['dependencies'][i]["github"][-1])
                urlretrieve(url, self.job_folder + "/plugins/" + i + ".jar")
            else:
                urlretrieve(self.job_cfg['dependencies'][i]["url"], self.job_folder + "/plugins/" + i + ".jar")

    def resolve_subjects(self):
        print("Resolving testing subjects...")
        for i in self.job_cfg['subject']:
            print("Getting " + i + "...")
            if self.job_cfg['subject'][i]["jenkins"] is not False and self.job_cfg['subject'][i]["jenkins"][0] is True:
                api = JenkinsAPI(self.job_cfg['subject'][i]["url"])
                url = api.latest(self.job_cfg['subject'][i]["jenkins"][-1])
                urlretrieve(url, self.job_folder + "/plugins/" + i + ".jar")
            elif self.job_cfg['subject'][i]["github"] is not False and self.job_cfg['subject'][i]["github"][0] is True:
                api = GitHubAPI(self.job_cfg['subject'][i]["url"])
                if self.job_cfg['subject'][i]["github"][-1] is None:
                    url = api.latest(None)
                else:
                    url = api.latest(self.job_cfg['subject'][i]["github"][-1])
                urlretrieve(url, self.job_folder + "/plugins/" + i + ".jar")
            else:
                urlretrieve(self.job_cfg['subject'][i]["url"], self.job_folder + "/plugins/" + i + ".jar")

    def finalize(self):
        print("Packing artifacts...")
        make_archive("artifact.zip", "zip", self.job_folder)
