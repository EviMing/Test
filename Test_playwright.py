#程序文件名绝对不能为playwright.py，否则会报错

from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor,as_completed

def Browser(url_str,page_int):

    #创建浏览器实例
    with sync_playwright() as p:

        #选择浏览器内核
        browser = p.chromium.launch()
            #chromium：使用官方自带的Chromium

        #设置timeout时间
        s = 60

        #新建标签页
        page = browser.new_page()

        try:
            #跳转页面
            page.goto(f"{url_str}",timeout=int(s*1000))
        except TimeoutError:
            print(f"[报错] timeout('{s}'秒) -> [原因] '{url_str}' URL跳转时间超时")

        #定位标签，CSS选择器语法
        css = 'span[class*="page-item_M4MDr"]'

        try:
            #等待第int(x)页标签出现，出现则说明html渲染到最下方了
            page.locator(f'{css}',has_text=f'{page_int}').wait_for(state='visible',timeout=int(s*1000))
        except TimeoutError:
            print(f"[报错] timeout('{s}'秒) -> [原因] '{css}' CSS未找到满足条件的标签 'or' 未出现 '{page_int}' 页面标签")

        #content方法返回当前页面的html(txt形式)，若前方有渲染操作，则html是经过渲染的
        html = page.content()

        with open(rf"C:\Users\Administrator\Desktop\TestFolder\html\baidu\baidu_{page_int}.html","w",encoding="utf-8") as f:
            f.write(html)

        print(f"'{page_int}'_html_OK")

Directory = r"C:\Users\Administrator\Desktop\TestFolder\html\baidu"

list_futures = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(0,10,1):
        wd = "Python"
        pn = 0+(i*10)
        url = f"https://www.baidu.com/s?wd={wd}&base_query=Python&pn={pn}"
        list_futures.append(executor.submit(Browser,url,i))

for future in as_completed(list_futures):
    pass