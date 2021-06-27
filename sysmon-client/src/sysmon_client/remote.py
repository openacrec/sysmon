"""
Handles remote connections
"""

import spur


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
    test = connect_with_ssh(host, user, passw)

    print(test)
