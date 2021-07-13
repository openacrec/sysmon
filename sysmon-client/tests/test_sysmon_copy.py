from sysmon_client import Task

task = Task("Example")

# task.get_free_remotes()  # How to credential?

task.add_remote("asraphael.uni-koblenz.de", "matthias")

task.copy("~/test_sysmon_copy.py", "test_sysmon/test_sysmon_copy.py")
task.copy("~/testdata", "test_sysmon/")


# task.install_req(file or list of modules)

# task.run("python trainer.py")  # Force "python" as first argument? Easy to circumvent

# task.output  # can this be yielded from a generator? or only after task finished?
