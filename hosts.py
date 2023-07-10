import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import schedule

# 设置重试策略
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

session = requests.Session() 
session.mount('https://', HTTPAdapter(max_retries=retries))

url = 'https://cdn.jsdelivr.net/gh/521xueweihan/GitHub520@main/hosts'

def download_hosts():
    print('Refreshing hosts...')  
    resp = session.get(url)
    print('Writing hosts to file')  
    with open('/etc/hosts', 'a') as f:
        f.write(resp.text)  
    print('Hosts file updated successfully!')

schedule.every(1).minutes.do(download_hosts)

while True:
    schedule.run_pending()      
