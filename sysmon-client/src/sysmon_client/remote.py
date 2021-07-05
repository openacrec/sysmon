"""
Establish remote connection and issue commands over ssh
"""
import spur

# TODO: Evaluate if i can provide an easier interface for our use cases
# Otherwise integrate spur into the functions that would call this
# One immediate pro: Can save this for use throughout, no need to provide
# login information multiple times (in code)


class Remote:
    def __init__(self):
        self.hostname = ""
        self.user_name = ""
        self.password = ""
        self.key_file = ""  # Maybe Path
        self.port = 22

    # This was a small test of spur, ignore for now
    @staticmethod
    def connect_with_ssh(hostname: str,
                         username: str,
                         password: str = None,
                         key_file: str = None,
                         port: int = None):
        shell = spur.SshShell(hostname=hostname,
                              username=username,
                              password=password,
                              private_key_file=key_file,
                              port=port)
        with shell:
            result = shell.run(["pwd"])

            return result.output


if __name__ == '__main__':
    host = input("Host: ")
    user = input("User: ")
    passw = input("Password: ")
    test = Remote.connect_with_ssh(host, user, passw)

    print(test)
