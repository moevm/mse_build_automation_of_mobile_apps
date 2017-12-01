import sys
import os
import jenkins
import xml.etree.ElementTree as ET


def create_dirs(rep_lst):
    dir_path = os.path.realpath('./repos')
    repo_dirs = []

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for repo in rep_lst:
        repo_dir = dir_path + '/' + repo[repo.rfind('/') + 1::]
        if not os.path.exists(repo_dir):
            os.mkdir(repo_dir)
        repo_dirs.append(repo_dir)
    return repo_dirs


def edit_xml(rep_lst):
    tree = ET.ElementTree(file='template_config.xml')
    root = tree.getroot()
    dir_path = os.path.realpath('./repos')

    for repo in rep_lst:
        for url in root.iter('url'):
            url.text = repo
        for url in root.iter('projectUrl'):
            url.text = repo + '/'
        repo_dir = dir_path + '/' + repo[repo.rfind('/') + 1::]
        tree.write(repo_dir + '/config.xml')


def read_xml(file_name):
    f = open(file_name)
    res = ''
    line = f.readline().strip()
    res += line + ' '
    while line:
        line = f.readline().strip()
        res += line + ' '
    f.close()
    return res


def get_job_names(dirs):
    res = []
    for repository in dirs:
        res.append(repository[repository.rfind('/') + 1::])
    return res


def contains(jobs, repo_name):
    for job in jobs:
        if job['fullname'] == repo_name:
            return True
    return False


print('*****************')
print('Jenkins Automator')
print('*****************')
file_name = 'repo_list.txt'
if len(sys.argv) > 1:
    file_name = sys.argv[1]
print('Using ' + file_name + ' as repo list source\n')
f = open(file_name)
line = f.readline().strip()
repo_list = []
if line:
    repo_list.append(line)
while line:
    line = f.readline().strip()
    if line != '':
        repo_list.append(line)
f.close()
dirs = create_dirs(repo_list)
job_names = get_job_names(dirs)
edit_xml(repo_list)

server = jenkins.Jenkins('http://localhost:8080', 'sgn', 'toor')

print('Number of jobs before adding: ' + str(server.jobs_count()))
print('Number of jobs to add: ' + str(len(dirs)))
jobs = server.get_jobs()

for repository in dirs:
    job_name = repository[repository.rfind('/') + 1::]
    # if contains(jobs, job_name):
    if server.job_exists(job_name):
        print('Repo with name ' + job_name + ' already added')
    else:
        configure_xml = read_xml(repository + '/config.xml')
        server.create_job(job_name, configure_xml)

print('Number of jobs after adding: ' + str(server.jobs_count()) + '\n')

print('Starting building jobs')
for job_name in job_names:
    print('Building ' + job_name)
    server.build_job(job_name)
print('Now wait for building jobs')
