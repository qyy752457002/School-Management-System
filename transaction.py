import requests
from kazoo.client import KazooClient
import os
import logging

# 使用环境变量或配置文件来获取敏感信息
API_URLS = {
    "A_school": os.getenv("API_A_SCHOOL", "http://127.0.0.1:5001/prepare"),
    "B_school": os.getenv("API_B_SCHOOL", "http://127.0.0.1:5002/prepare"),
    "A_district": os.getenv("API_A_DISTRICT", "http://127.0.0.1:5003/prepare"),
    "B_district": os.getenv("API_B_DISTRICT", "http://127.0.0.1:5004/prepare"),
    "workflow": os.getenv("API_WORKFLOW", "http://127.0.0.1:5005/prepare")
}
PREFIX = "transfer_"
LOCK_PATH = PREFIX + "/transfer_lock"
ZOOKEEPER_HOSTS = os.getenv("ZOOKEEPER_HOSTS", "10.0.9.1:2181,10.0.9.2:2181,10.0.9.3:2181")

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

zk = KazooClient(ZOOKEEPER_HOSTS)
zk.start()

def api_call(url, data):
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        logging.info(f"API call succeeded: {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API call failed: {e}")
        return None

def prepare_transaction(data):
    prepare_responses = {}
    for system, url in API_URLS.items():
        response = api_call(url, data)
        if response and response.get("status") == "prepared":
            response["baseurl"]= url.replace('prepare','')
            prepare_responses[system] = response
        else:
            # 尝试回滚已准备的操作
            rollback_transaction(prepare_responses)
            return False
    return prepare_responses

def pre_commit_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"{response.get('baseurl')}{response.get('pre_commit_url')}"
        if not api_call(url, response):
            # 如果预提交失败，则回滚
            rollback_transaction(prepare_responses)
            return False
    return True

def commit_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"{response.get('baseurl')}{response.get('commit_url')}"
        api_call(url, response)
    logging.info("Transaction committed successfully.")

def rollback_transaction(prepare_responses):
    for system, response in prepare_responses.items():
        url = f"{response.get('baseurl')}{response.get('rollback_url')}"
        api_call(url, response)
    logging.info("Transaction rolled back.")

def execute_transfer(data):
    lock = zk.Lock(LOCK_PATH)

    try:
        if lock.acquire(blocking=True, timeout=10):
            try:
                prepare_responses = prepare_transaction(data)
                if prepare_responses:
                    if pre_commit_transaction(prepare_responses):
                        commit_transaction(prepare_responses)
                    else:
                        logging.info("Pre-commit failed, transaction rolled back.")
                else:
                    logging.info("Prepare phase failed, transaction rolled back.")
            finally:
                lock.release()
        else:
            logging.info("Failed to acquire lock, transaction aborted.")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        zk.stop()
        zk.close()
        raise

if __name__ == '__main__':
    transfer_data = {
        "student_id": "123456",
        "new_school": "A_school",
        "old_school": "B_school",
        "new_district": "A_district",
        "old_district": "B_district"
    }
    execute_transfer(transfer_data)
    zk.stop()
    zk.close()
