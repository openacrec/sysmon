from sysmon_client.task import Task

# Name the Task, used to display a name if you publish the task to a server
# and to initialize a new Task object
print("Creating task.")
task = Task("Example")
print("Done.")

# Define the remote server on which all these tests run
# You need to be in the university network, using the keyfile search function
# that spur (the used ssh wrapper) provides
print("Adding remotes.")
task.add_remote("asraphael", "asraphael.uni-koblenz.de", "matthias",
                do_connection_test=False, create_target=True)
print("Done.")

# Test if the publishing of some task status information works
# print("Init notify service.")
# task.publish_task_on("http://127.0.0.1:5000")  # needs a running sysmon server
# print("Done.")

# Test different copy scenarios: copy a single file,
# copy into a (non-existing?) subdirectory
# and copying a whole directory into a (non-existing?) one
print("Copy files over.")
task.copy("~/test_script.py", "test_script.py")
task.copy("~/test_script.py", "test_sysmon2/test_script.py")
task.copy("~/testdata", "test_sysmon2/")
print("Done.")


# Test changing default python version to use
print("Specify global python version.")
task.use_python_version(3.7)
print("Done.")

# Test usage of venv
# Note: used test server did not have venv, tested locally as close
# to program as manageable
print("Create venv.")
task.create_venv("~/testdata/venv")
print("Done.")

# Test both supported methods to install requirements:
# Via a requirements file and via a list of packages
print("Install req.")
task.install_req("copy_test.txt")
task.install_req(["pip-install-test"])
print("Done.")

print("Execute test script.")
# Test running a python file on the remote
task.run("test_sysmon/test_script.py")
print("Done.")

# This is not needed, if run does not deactivate output to stdout (use_stdout=False)
# Since the task gathers output from all remotes, currently this is how you print it
print(task.output[0])
