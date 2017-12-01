from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from tab_class import report_tab
import sys
import os
import jenkins
import xml.etree.ElementTree as ET


def add_repo(repo_url):
    model = window.lstRepos.model()
    if model is None:
        model = QStandardItemModel()
    # repo_url = window.lineRepo.text()
    job_name = repo_url[repo_url.rfind('/') + 1::]

    # print(job_name)
    if server.job_exists(job_name) or repo_url == '':
        print('Repo with name ' + job_name + ' already added')
    else:
        repo_dir = create_dir(repo_url)
        edit_xml(repo_dir, repo_url)
        configure_xml = read_xml(repo_dir + '/config.xml')
        server.create_job(job_name, configure_xml)

    item = QStandardItem(repo_url)
    item.setEditable(False)
    model.appendRow(item)
    window.lstRepos.setModel(model)
    new_tab = report_tab(job_name)
    window.tabMain.addTab(new_tab, job_name)
    dir = create_dir(repo_url)
    window.tabMain.findChild(QtWidgets.QPushButton, "btnBuild").clicked.connect(lambda: run_build(job_name))
    window.tabMain.findChild(QtWidgets.QPushButton, "btnGetLogs").clicked.connect(lambda: get_logs(job_name))
    # window.tabMain.findChild(QtGui.QWidget, repo_name + "_tab").setTabText(repo_name)
    # print('Репозиторий %s добавлен' % repo_url)


def create_dir(repo_url):
    repos_path = os.path.realpath('./repos')
    if not os.path.exists(repos_path):
        os.mkdir(repos_path)

    repo_dir = repos_path + '/' + repo_url[repo_url.rfind('/') + 1::]
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    return repo_dir


def edit_xml(repo_dir, repo_url):
    tree = ET.ElementTree(file=template_file)
    root = tree.getroot()
    for url in root.iter('url'):
        url.text = repo_url
    # dir_path = os.path.realpath('./repos')
    # repo_dir = dir_path + '/' + repo[repo.rfind('/') + 1::]
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


def contains(jobs, repo_name):
    for job in jobs:
        if job['fullname'] == repo_name:
            return True
    return False


def run_build(job_name):
    server.build_job(job_name)
    # self.parent().parent()
    print('Запуск построения проекта %s' % job_name)


def load_template(self):
    file_name = QFileDialog.getOpenFileName(None, "Open File", ".", "Jenkins job settings (*.xml)")
    if file_name[0] != '':
        self.template_file = file_name
    # print('Репозитории добавлены')


def get_logs(job_name):
    from jenkinsapi.jenkins import Jenkins as Japi
    japi_serv = Japi('http://localhost:8080', username='sgn', password='toor')
    job = japi_serv[job_name]
    lgb = job.get_last_completed_build()
    status = lgb.get_status()
    log = lgb.get_console()
    window.tabMain.findChild(QtWidgets.QLabel, job_name + "_status").setText(status)
    window.tabMain.findChild(QtWidgets.QTextEdit, job_name + "_log").setText(log)


def load_repos(self):
    file_name = QFileDialog.getOpenFileName(None, "Open File", ".", "Text (*.txt)")
    if file_name[0] != '':
        f = open(file_name[0])
        model = QStandardItemModel()
        line = f.readline().strip()
        add_repo(line)
        while line:
            add_repo(line)
            model.appendRow(QStandardItem(line))
            line = f.readline().strip()
        f.close()
        window.lstRepos.setModel(model)


if __name__ == "__main__":
    import sys

    server = jenkins.Jenkins('http://localhost:8080', 'sgn', 'toor')
    template_file = 'temp.xml'
    app = QtWidgets.QApplication(sys.argv)
    window = uic.loadUi("mainwindow.ui")
    window.btnAddRepo.clicked.connect(lambda: add_repo(window.lineRepo.text()))
    window.btnLoadRepos.clicked.connect(load_repos)
    window.actLoadTemplate.triggered.connect(load_template)
    window.show()
    sys.exit(app.exec_())
