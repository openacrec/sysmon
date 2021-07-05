# TODO: Make context manager like, probably as a class instead of generator:
"""
with sysmon_task("Working on UTD"):
    sysmon.loadbalancer.copy(X, Y)
    sysmon.run(Z)

which ensures that afterwards the notification is removed again.
"""

# TODO: Contemplate if a parent class for all makes sense that contains:
# The servers in use for this task
# status of task execution (ENUM: RUNNING; FINISHED; FAILED; UNKNOWN)
# ...

# Use Remote() for that, since this uses most of these classes


class Notify:
    def __init__(self):
        self.server = "or servers?"
        self.severs = []

    def notify(self):
        """Notify sysmon sever that a task is executing on a client."""
        # Use a string, that gets displayed? Can be funny but will be a risk
        # if this user input is handled wrong on server side
        # Could use TaskStatus (from task_status import TaskStatus

        # If this method remains the only one, maybe add it into Remote
        # or be classless
        raise NotImplementedError
