import requests
from kazoo.client import KazooClient

# todo  回滚失败的 事务的 补偿 处理   模拟3中情况的  全成功  失败  回滚失败
# 各系统的 API 接口 URL
API_URLS = {
    "A_school": "http://127.0.0.1:5001/prepare",
    "B_school": "http://127.0.0.1:5002/prepare",
    "A_district": "http://127.0.0.1:5003/prepare",
    "B_district": "http://127.0.0.1:5004/prepare",
    "workflow": "http://127.0.0.1:5005/prepare"
}
# 定义路径前缀
PREFIX = "transfer_"
# 分布式锁路径

LOCK_PATH = PREFIX + "/transfer_lock"
# zk = kazoo("127.0.0.1:2181") 10.0.9.1
# 10.0.9.2
# 10.0.9.3s
zk = KazooClient("10.0.9.1:2181,10.0.9.2:2181,10.0.9.3:2181")
def api_call(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

def prepare_transaction(data):
    prepare_responses = {}
    for system, url in API_URLS.items():
        response = api_call(url, data)
        if response and response.get("status") == "prepared":
            prepare_responses[system] = response
        else:
            rollback_transaction(prepare_responses)
            return False
    return prepare_responses

def pre_commit_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"http://127.0.0.1:5000{response.get('pre_commit_url')}"
        if not api_call(url, response):
            rollback_transaction(prepare_responses)
            return False
    return True

def commit_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"http://127.0.0.1:5000{response.get('commit_url')}"
        api_call(url, response)

def rollback_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"http://127.0.0.1:5000{response.get('rollback_url')}"
        api_call(url, response)

def execute_transfer(data):
    lock = zk.Lock(LOCK_PATH)

    if lock.acquire(blocking=True):
        try:
            prepare_responses = prepare_transaction(data)
            if prepare_responses:
                if pre_commit_transaction(prepare_responses):
                    commit_transaction(prepare_responses)
                    print("Transaction committed successfully.")
                else:
                    print("Pre-commit failed, transaction rolled back.")
            else:
                print("Prepare phase failed, transaction rolled back.")
        finally:
            lock.release()
    else:
        print("Failed to acquire lock, transaction aborted.")

if __name__ == '__main__':
    transfer_data = {
        "student_id": "123456",
        "new_school": "A_school",
        "old_school": "B_school",
        "new_district": "A_district",
        "old_district": "B_district"
    }
    execute_transfer(transfer_data)

# 关闭 Zookeeper 客户端
zk.stop()