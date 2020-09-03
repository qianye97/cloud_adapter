import paramiko


def ssh_connect(host_ip, host_port, username, password):
    # SSH远程连接
    ssh = paramiko.SSHClient()  # 创建sshclient
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 指定当对方主机没有本机公钥的情况时应该怎么>办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
    ssh.connect(host_ip, host_port, username, password)

    print(ssh)


if __name__ == '__main__':
    ssh_connect('192.168.109', 22, 'root', 'tusdt')
