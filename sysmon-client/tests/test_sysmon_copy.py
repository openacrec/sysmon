from sysmon_client.task import Task

task = Task("Example")

# task.get_free_remotes()  # How to credential?

task.add_remote("asraphael.uni-koblenz.de", "matthias", create_target=True)

task.copy("~/test_script.py", "test_sysmon2/test_script.py")
task.copy("~/test_script.py", "test_script.py")

task.copy("~/testdata", "test_sysmon2/")

task.install_req("copy_test.txt")
task.install_req(["pip-install-test"])

task.run("test_sysmon/test_script.py")

# can this be yielded from a generator? or only after task finished?
print(task.output[0])
