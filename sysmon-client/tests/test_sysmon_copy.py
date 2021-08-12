from sysmon_client.task import Task

# Name the Task, used to display a name if you publish the task to a server
# and to initialize a new Task object
task = Task("Example")

# Define the remote server on which all these tests run
# You need to be in the university network, using the keyfile search function
# that spur (the used ssh wrapper) provides
task.add_remote("asraphael", "asraphael.uni-koblenz.de", "matthias",
                do_connection_test=False, create_target=True)

# Test if the publishing of some task status information works
task.publish_task_on("http://127.0.0.1:5000")

# Test different copy scenarios: copy a single file,
# copy into a (non-existing?) subdirectory
# and copying a whole directory into a (non-existing?) one
task.copy("~/test_script.py", "test_script.py")
task.copy("~/test_script.py", "test_sysmon2/test_script.py")
task.copy("~/testdata", "test_sysmon2/")

# Test changing default python version to use
task.use_python_version(3.7)

# Test both supported methods to install requirements:
# Via a requirements file and via a list of packages
task.install_req("copy_test.txt")
task.install_req(["pip-install-test"])

# Test running a python file on the remote
task.run("test_sysmon/test_script.py")

# This is not needed, if run does not deactivate output to stdout (use_stdout=False)
# Since the task gathers output from all remotes, currently this is how you print it
print(task.output[0])
