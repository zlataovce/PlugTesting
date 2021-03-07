import json
from os.path import exists
from libs.jobs import Deploy

if __name__ == '__main__':
    with open('config.json') as config_json:
        cfg = json.load(config_json)
        print("PlugDeploy " + cfg['version'] + "\n")
        if not exists(cfg['job_path']):
            print("No job configs!")
            exit(-1)
        if not exists("builds.txt"):
            with open("builds.txt", "w") as bf:
                bf.write("1")
            build_number = "1"
        else:
            with open("builds.txt", "r") as rf:
                build_number = str(int(rf.read()) + 1)
                with open("builds.txt", "w") as bf:
                    bf.write(build_number)
        try:
            with open(cfg['job_path']) as job_json:
                job = json.load(job_json)
        except json.JSONDecodeError:
            print("Your job config isn't valid!")
            exit(-1)
        # init done, jobs next
        # noinspection PyUnboundLocalVariable
        inst = Deploy(cfg, build_number, job)
        inst.prepare_server()
        inst.resolve_deps()
        inst.resolve_subjects()
        inst.finalize()
        print("Done.")
