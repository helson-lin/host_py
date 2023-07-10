import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import schedule

# 设置重试策略
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

url = 'https://cdn.jsdelivr.net/gh/521xueweihan/GitHub520@main/hosts'


def clear():
    with open('/etc/hosts') as f:
        lines = f.readlines()

    in_content = False
    with open('/etc/hosts', 'w') as f:
        for line in lines:
            if line.startswith('# GitHub520 Host Start'):
                in_content = True
            elif line.startswith('# GitHub520 Host End'):
                in_content = False
            else:
                if not in_content:
                    f.write(line)


def download_hosts():
    clear()
    print('Refreshing hosts...')
    resp = session.get(url)
    print('Writing hosts to file')
    with open('/etc/hosts', 'a') as f:
        f.write(resp.text)
    print('Hosts file updated successfully!')


schedule.every(5).minutes.do(download_hosts)

while True:
    schedule.run_pending()
