#标准文件名应为 -> 'request.py'

#[引入库] 辅助库
import traceback
from typing import Literal
import sys

#[引入库] 同步库
import requests
from time import sleep

#[引入库] 异步库
import asyncio
import aiohttp
import aiofiles

#[定义函数] 同步实现
def request(
    url:str,
    headers:dict,
    file_path:str,
    time:int=10,
    timeout: None | tuple[None|int, None|int] = None,
    sleep_time:int=10,
    proxy:None|str=None,
    method:str='get'
) -> tuple[Literal[0]] | tuple[Literal[1], tuple[type, str, str]]:
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
                timeout=timeout
            ) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1*1024*1024):
                        if chunk:
                            f.write(chunk)
            return (0,)
        except SystemExit:
            raise SystemExit
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            error_type, error_str, error_traceback = sys.exc_info()
            _ += 1
            if _ >= time:
                print(f'{'{'}\n[error]\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n{'}'}')
                return (1, (error_type, str(error_str), traceback.format_exc()))
            print(f'[error]->[\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n]')
            sleep(sleep_time)
            continue

#[定义函数] 异步实现
async def async_request(
    url: str,
    headers: dict,
    file_path: str,
    time: int = 10,
    timeout: None | tuple[None | int, None | int] = None,
    sleep_time: int = 10,
    proxy: None | str = None,
    method: str = 'get'
) -> tuple[Literal[0]] | tuple[Literal[1], tuple[type, str, str]]:
    method = method.lower()
    _ = 0
    aio_timeout = None
    if timeout is not None:
        connect_timeout, read_timeout = timeout
        aio_timeout = aiohttp.ClientTimeout(
            total=None, 
            connect=connect_timeout, 
            sock_read=read_timeout
        )
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    proxy=proxy,
                    timeout=aio_timeout
                ) as response:
                    response.raise_for_status()

                    async with aiofiles.open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(1 * 1024 * 1024):
                            if chunk:
                                await f.write(chunk)
            return (0,)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception as e:
            error_type = type(e).__name__
            error_str = str(e)
            _ += 1
            if _ >= time:
                print(f'{'{'}\n[error]\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n{'}'}')
                return (1, (error_type, str(error_str), traceback.format_exc()))
            print(f'[error]->[\nerror.class=\'{error_type}\',\nerror.str=\"{error_str}\",\nurl={url},\nnum={_}\n]')
            await asyncio.sleep(sleep_time)
            continue
