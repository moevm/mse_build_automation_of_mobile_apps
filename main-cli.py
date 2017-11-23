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


print('*****************')
print('Jenkins Automator')
print('*****************')
file_name = 'repo_list.txt'
if len(sys.argv) > 1:
    file_name = sys.argv[1]
print('Using ' + file_name + ' as repo list source')
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
edit_xml(repo_list)

server = jenkins.Jenkins('http://localhost:8080', 'sgn', 'toor')

print('Number of jobs before adding: ' + str(server.jobs_count()))
print('Number of jobs to add: ' + str(len(dirs)))

for repository in dirs:
    job_name = repository[repository.rfind('/') + 1::]
    configure_xml = read_xml(repository + '/config.xml')
    server.create_job(job_name, configure_xml)

print('Number of jobs after adding: ' + str(server.jobs_count()))
