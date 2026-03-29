import requests
import sys
import os
import json
import time
from bs4 import BeautifulSoup

def crawl_baidu(lesson_name):
    """从百度搜索爬取资料"""
    results = []
    
    # 搜索关键词
    keywords = [f"{lesson_name} 课文知识点", f"{lesson_name} 教学设计"]
    
    for keyword in keywords:
        try:
            url = f"https://www.baidu.com/s?wd={keyword}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取搜索结果
            for result in soup.find_all('div', class_='result')[:3]:
                text = result.get_text()
                if len(text) > 100:
                    results.append(text[:800])
            time.sleep(1)
        except Exception as e:
            print(f"搜索出错: {e}")
    
    return results

def crawl_chusan(lesson_name):
    """爬取初三网"""
    try:
        url = f"http://www.chusan.com/zhongkao/{lesson_name}.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('article') or soup.find('div', class_='content')
        if content:
            return content.get_text()[:1500]
    except:
        pass
    return ""

def crawl_yuwenmi(lesson_name):
    """爬取语文迷"""
    try:
        url = f"https://www.yuwenmi.com/tag/{lesson_name}/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')[:2]
        text = ""
        for art in articles:
            text += art.get_text()[:500]
        return text
    except:
        pass
    return ""

def generate_note(lesson_name, materials):
    """生成笔记"""
    
    # 合并所有爬取的内容
    all_content = "\n\n".join(materials) if materials else f"《{lesson_name}》是一篇优美的课文。"
    
    note = f"""# 📖 {lesson_name} · 智能笔记

> 本笔记由爬虫自动从网络收集整理

---

## 📚 课文资料

{all_content[:2000]}

---

## 📝 生字词积累

（请根据课文内容填写）

| 生字 | 拼音 | 组词 |
|------|------|------|
| | | |
| | | |

---

## ✨ 重点句子赏析

> 请在下面抄写你喜欢的句子：

________________________________

________________________________

---

## 🎯 课后练习

1. 朗读课文3遍
2. 抄写生字词
3. 完成课后思考题

---

## 💡 我的思考

通过学习这篇课文，我学到了：________________

---

*📅 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*🔍 数据来源: 百度搜索、初三网、语文迷等*
"""
    return note

def main():
    if len(sys.argv) < 2:
        print("请提供课文名称")
        sys.exit(1)
    
    lesson_name = sys.argv[1]
    print(f"🔍 正在为《{lesson_name}》爬取资料...")
    
    # 爬取各个网站
    all_materials = []
    
    print("📡 正在搜索百度...")
    baidu_results = crawl_baidu(lesson_name)
    all_materials.extend(baidu_results)
    
    print("📡 正在爬取初三网...")
    chusan_result = crawl_chusan(lesson_name)
    if chusan_result:
        all_materials.append(chusan_result)
    
    print("📡 正在爬取语文迷...")
    yuwenmi_result = crawl_yuwenmi(lesson_name)
    if yuwenmi_result:
        all_materials.append(yuwenmi_result)
    
    print(f"✅ 共收集到 {len(all_materials)} 条资料")
    
    # 生成笔记
    note = generate_note(lesson_name, all_materials)
    
    # 保存到文件
    os.makedirs('data', exist_ok=True)
    output_file = f"data/{lesson_name}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(note)
    
    print(f"✅ 笔记已保存: {output_file}")

if __name__ == "__main__":
    main()
