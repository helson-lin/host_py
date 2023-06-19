import os
import requests
import schedule

url = 'https://cdn.jsdelivr.net/gh/521xueweihan/GitHub520@main/hosts'
hosts_path = '/etc/hosts' if os.name != 'nt' else r'C:\Windows\System32\drivers\etc\hosts'


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
    print('Refreshing hosts...')
    clear()
    resp = requests.get(url)
    with open(hosts_path, 'a') as f:
        f.write(resp.text)
    print('Hosts file updated successfully!')


schedule.every(10).minutes.do(download_hosts)

while True:
    schedule.run_pending()

