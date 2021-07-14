from sysmon_client.task import Task

task = Task("Example")

# task.get_free_remotes()  # How to credential?

task.add_remote("asraphael.uni-koblenz.de", "matthias")

task.copy("~/test_script.py", "test_sysmon/test_script.py")
task.copy("~/testdata", "test_sysmon/")


# task.install_req(file or list of modules)

task.run("test_sysmon/test_script.py")

print(task.output)  # can this be yielded from a generator? or only after task finished?
