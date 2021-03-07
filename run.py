import json
from os.path import exists
from libs.jobs import Deploy
from termcolor import colored

if __name__ == '__main__':
    with open('config.json') as config_json:
        cfg = json.load(config_json)
    print("PaperPacker " + cfg['version'] + "\n")
    if not exists(cfg['job_path']):
        print(colored("No job configs!", "red"))
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
        print(colored("Your job config isn't valid!", "red"))
        exit(-1)
    # init done, jobs next
    # noinspection PyUnboundLocalVariable
    inst = Deploy(cfg, build_number, job)
    inst.prepare_server()
    inst.resolve_deps()
    inst.resolve_subjects()
    inst.finalize()
    print(colored("Done.", "green"))
