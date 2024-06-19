from kazoo.client import KazooClient

# 使用 with 语句和上下文管理器来确保资源正确释放
class SafeKazooClient:
    def __init__(self, hosts):
        self.zk = KazooClient(hosts)

    def __enter__(self):
        self.zk.start()
        return self.zk

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.zk.stop()
        self.zk.close()
