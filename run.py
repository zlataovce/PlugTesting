import json
from os.path import exists
from libs.jobs import Deploy

if __name__ == '__main__':
    cfg = json.loads("config.json")
    print("PlugDeploy " + cfg['version'] + "\n")
    if not exists(cfg['job_path']):
        print("No job configs!")
        exit(-1)
    if not exists("builds.txt"):
        with open("builds.txt", "w") as bf:
            bf.write("1")
        build_number = "1"
    else:
        with open("builds.txt", "r+") as bf:
            build_number = str(int(bf.read()) + 1)
            bf.write(build_number)
    try:
        job = json.loads(cfg['job_path'])
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
