from paramiko import SSHClient
from scp import SCPClient
import inspect
import io
import sys

HOST_DIRECTORY_PREFIX = '~/.sshrpc/'
HOST_MAIN_SCRIPT_NAME = 'rpc-host-main.py'
HOST_FUNC_SCRIPT_NAME = 'rpcfunc.py'

class SSHRPC():
    def __init__(self, hostname, port, username, password):
        ssh = SSHClient()
        ssh.load_system_host_keys() # load file '~/.ssh/known_hosts' with trusted servers
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        scp = SCPClient(ssh.get_transport())
        self.ssh = ssh
        self.scp = scp
        self._prepare()
    def exec_func(self, func, in_str: str) -> str:
        code_str = self._func_to_source_str(func)
        self._str_to_remote_file(code_str, (HOST_DIRECTORY_PREFIX+HOST_FUNC_SCRIPT_NAME))
        return self._exec_write_read('python {}'.format(HOST_DIRECTORY_PREFIX+HOST_MAIN_SCRIPT_NAME), in_str)
    def _prepare(self):
        self.ssh.exec_command('mkdir -p {}'.format(HOST_DIRECTORY_PREFIX))
        self.scp.put(HOST_MAIN_SCRIPT_NAME, remote_path=(HOST_DIRECTORY_PREFIX+HOST_MAIN_SCRIPT_NAME))
    def _func_to_source_str(self, func) -> str:
        func_str = inspect.getsource(func)
        pos = func_str.find('\n')
        func_def_str = 'def func(in_str: str) -> str:\n'
        code_str = func_def_str + func_str[pos+1:]
        return code_str
    def _str_to_remote_file(self, s: str, path: str):
        f = io.BytesIO()
        f.write(s.encode('UTF-8'))
        f.seek(0)
        self.scp.putfo(f, path)
    def _exec_write_read(self, command: str, in_str: str) -> str:
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdin.write(in_str)
        stdin.close()
        out_str = stdout.read().decode('UTF-8')
        err_str = stderr.read().decode('UTF-8')
        if len(err_str) > 1:
            print('Error message from remote host', file=sys.stderr)
            print(err_str, file=sys.stderr)
        stdout.close()
        stderr.close()
        return out_str

