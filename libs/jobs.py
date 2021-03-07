from os import mkdir
from os.path import exists
from shutil import rmtree, copyfile, make_archive
from libs.paper_api import PaperAPI
from urllib.request import urlretrieve
from libs.jenkins_api import JenkinsAPI
from libs.github_api import GitHubAPI
from libs.termcolor import colored


class Deploy:
    def __init__(self, cfg, build_number, job_cfg):
        self.cfg = cfg
        self.build_number = build_number
        self.job_folder = cfg['jobs_directory'] + "/" + build_number
        self.job_cfg = job_cfg
        print(colored("Preparing build directories...", "cyan"))
        if not exists(cfg['jobs_directory']):
            mkdir(cfg['jobs_directory'])
        if exists(self.job_folder):
            print(colored("Build already exists! Overriding.", "yellow"))
            rmtree(self.job_folder)
        mkdir(self.job_folder)
        mkdir(self.job_folder + "/plugins")

    def prepare_server(self):
        api = PaperAPI(self.job_cfg['version'])
        print(colored("Resolving build info from PaperAPI...", "cyan"))
        if self.job_cfg['paper_build'] == "latest":
            url = api.latest()
        else:
            url = api.build(self.job_cfg['paper_build'])
        print(colored("Downloading the Paper JAR... This may take a while.", "cyan"))
        urlretrieve(url, self.job_folder + "/paper.jar")
        print(colored("Copying files...", "cyan"))
        copyfile("libs/eula.txt", self.job_folder + "/eula.txt")
        copyfile(self.job_cfg['properties'], self.job_folder + "/server.properties")

    def resolve_deps(self):
        print(colored("Resolving dependencies...", "cyan"))
        for i in self.job_cfg['dependencies']:
            print(colored("Getting " + i + "...", "magenta"))
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
        print(colored("Resolving testing subjects...", "cyan"))
        for i in self.job_cfg['subject']:
            print(colored("Getting " + i + "...", "magenta"))
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
        print(colored("Packing artifacts...", "cyan"))
        make_archive(self.cfg['jobs_directory'] + "/artifact" + self.build_number, "zip", self.job_folder)
