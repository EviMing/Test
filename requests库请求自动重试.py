import requests
from time import sleep
import sys
import traceback
from typing import Literal

def request(url:str, headers:dict, file_path:str, time:int=10, sleep_time:int=10, proxy:None|str=None, method:str='get') -> Literal[0,1]:
    method = method.lower()
    _ = 0
    while True:
        try:
            with requests.request(
                method=method,
                url=url,
                headers=headers,
                proxies={
                    'http': proxy,
                    'https': proxy
                } if proxy else None,
                stream=True,
                timeout=(10, None)
            ) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1*1024*1024):
                        if chunk:
                            f.write(chunk)
            return 0
        except KeyboardInterrupt:
            print('[done] 用户主动退出')
            sys.exit()
        except:
            error_type, error_str, error_traceback = sys.exc_info()
            _ += 1
            if _ >= time:
                print(f'[\n[error]\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n]')
                traceback.print_exc()
                return 1
            print(f'[\n[error]\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n]')
            sleep(sleep_time)
            continue
