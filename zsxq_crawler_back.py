import re
import requests
import json
from bs4 import BeautifulSoup

def get_articles(group_id, user_id, access_token):
    headers = {
        'Cookie': f'zsxq_access_token={access_token};sajssdk_2015_cross_new_user=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Sec-Ch-Ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"'
            }
            
    # 获取文章列表
    api_url = f'https://api.zsxq.com/v2/users/{user_id}/footprints?count=20&group_id={group_id}&end_time=2024-12-17T14%3A54%3A21.852%2B0800&filter_group_id={group_id}'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        with open('response_data.txt', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return []

def download_article(url, access_token):
    headers = {
        'Cookie': f'zsxq_access_token={access_token};sajssdk_2015_cross_new_user=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Sec-Ch-Ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', {'class': 'content ql-editor'})
        if content_div:
            return str(content_div)
        else:
            return None
    except Exception as e:
        print(f"文章下载失败: {e}")
        return None


def save_as_html(html_content, filename, group_id):
    import os
    filename = re.sub(r'[\\/:*?"<>|\n\r\[\]]', '', filename)
    folder = str(group_id)
    if not os.path.exists(folder):
        os.makedirs(folder)
    html_filename = os.path.join(folder, f"{filename}.html")
    try:
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"已将内容保存为HTML文件: {html_filename}")
        return True
    except Exception as e:
        print(f"HTML保存失败: {e}")
        return False


if __name__ == '__main__':
    group_id = '28888122422841'
    user_id = '415841524882588'
    access_token = '4FE0F814-8AED-4F04-A8C8-FC58D5804C2A_33DEA2472F68523D'
    articles = get_articles(group_id, user_id, access_token)
    with open('response_data.txt', 'r', encoding='utf-8') as f:
        data = json.load(f)
    footprints = data.get('resp_data', {}).get('footprints', [])
    # 排序逻辑：无括号数字的最前，有括号数字的按数字升序
    def extract_sort_key(item):
        topic = item.get('topic', {})
        talk = topic.get('talk', {})
        # 获取title
        if 'article' in talk and 'title' in talk['article']:
            title = talk['article']['title']
        elif 'title' in topic:
            title = topic['title']
        elif 'text' in talk:
            title = talk['text']
        else:
            title = ''
        # 查找括号内数字
        match = re.search(r'\((\d+)\)\s*$', title)
        if match:
            return (1, int(match.group(1)))
        else:
            return (0, 0)
    footprints = sorted(footprints, key=extract_sort_key)
    for i, item in enumerate(footprints):
        topic = item.get('topic', {})
        talk = topic.get('talk', {})
        # 判断有无article_url
        article_url = None
        title = None
        content = None
        if 'article' in talk and 'article_url' in talk['article']:
            article_url = talk['article']['article_url']
            title = talk['article'].get('title', '')
        elif 'article_url' in talk:
            article_url = talk['article_url']
            title = topic.get('title', '') or talk.get('text', '')
        if article_url:
            # 有article_url，访问获取内容
            if not title:
                title = f'article_{i}'
            title = re.sub(r'[\\/:*?"<>|\n\r\[\]]', '', title[:100])
            content = download_article(article_url, access_token)
            if content:
                save_as_html(content, title, group_id)
                print(f'Saved article {i} as {title}.html')
            else:
                print(f'Failed to download article {i}')
        else:
            # 没有article_url，直接用text内容，title为topic["title"]去特殊字符
            title = topic.get('title', '')
            if not title:
                title = f'article_{i}'
            title = re.sub(r'[\\/:*?"<>|\n\r\[\]]', '', title[:100])
            text = talk.get('text', '')
            if text:
                html_content = f'<div class="content ql-editor">{text}</div>'
                save_as_html(html_content, title, group_id)
                print(f'Saved text article {i} as {title}.html')
            else:
                print(f'No text content for article {i}')