from jenkinsapi.jenkins import Jenkins


def get_server_instance():
    jenkins_url = 'http://localhost:8080'
    server = Jenkins(jenkins_url, username='sgn', password='toor')
    return server


def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print('Job Name:%s' % (job_instance.name))
        print('Job Description:%s' % (job_instance.get_description()))
        print('Is Job running:%s' % (job_instance.is_running()))
        print('Is Job enabled:%s' % (job_instance.is_enabled()))


def getSCMInfoFromLatestBuild(url, jobName, username=None, password=None):
    J = Jenkins(url, username, password)
    job = J[jobName]
    lgb = job.get_last_completed_build()
    lgb.get_console()
    return lgb.get_console()


# get_job_details()
print(getSCMInfoFromLatestBuild('http://localhost:8080', 'todo-api', 'sgn', 'toor'))
