# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
import re
from bs4 import BeautifulSoup

# ============================================
# 优先爬取 hanchacha.com 的课文资料
# 其他网站作为补充
# ============================================

def crawl_hanchacha(lesson_name):
    """优先爬取 hanchacha.com 的资料"""
    print(f"  🔍 优先搜索 hanchacha.com...")
    
    results = {
        "knowledge": "",      # 知识点
        "notes": "",          # 课堂笔记
        "exercises": "",      # 同步习题
        "reading": ""         # 类文阅读
    }
    
    # 常见的课文URL模式
    # 例如：https://hanchacha.com/yuwen/xxxx.html
    # 或者：https://hanchacha.com/yuwen/三年级下/海底世界.html
    
    # 先尝试直接搜索
    search_url = f"https://hanchacha.com/?s={lesson_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"    搜索: {search_url}")
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找搜索结果中的链接
        links = soup.find_all('a', href=True)
        found_urls = []
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().lower()
            if lesson_name.lower() in text or lesson_name.lower() in href:
                if 'hanchacha.com' in href and href not in found_urls:
                    found_urls.append(href)
                    print(f"    找到链接: {href}")
        
        # 访问找到的页面获取内容
        for url in found_urls[:3]:  # 最多取3个
            try:
                print(f"    正在获取: {url}")
                page_resp = requests.get(url, headers=headers, timeout=10)
                page_soup = BeautifulSoup(page_resp.text, 'html.parser')
                
                # 提取文章内容
                content_div = page_soup.find('article') or page_soup.find('div', class_='entry-content') or page_soup.find('div', class_='post-content')
                
                if content_div:
                    text = content_div.get_text(strip=True)
                    
                    # 根据页面标题判断内容类型
                    title = page_soup.find('title')
                    title_text = title.get_text() if title else ""
                    
                    if '知识点' in title_text or '知识' in title_text:
                        results["knowledge"] = text[:2000]
                    elif '笔记' in title_text or '课堂笔记' in title_text:
                        results["notes"] = text[:2000]
                    elif '习题' in title_text or '练习' in title_text:
                        results["exercises"] = text[:1500]
                    else:
                        # 默认放到笔记里
                        if not results["notes"]:
                            results["notes"] = text[:2000]
                            
            except Exception as e:
                print(f"    获取页面失败: {e}")
                
    except Exception as e:
        print(f"  hanchacha 搜索失败: {e}")
    
    return results

def crawl_baidu(lesson_name):
    """百度搜索补充资料"""
    print(f"  📡 百度搜索补充...")
    results = []
    
    keywords = [f"{lesson_name} 课文讲解", f"{lesson_name} 教学重点"]
    
    for keyword in keywords[:1]:  # 只搜一个关键词，节省时间
        try:
            url = f"https://www.baidu.com/s?wd={keyword}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=8)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results_div = soup.find_all('div', class_='result')
            for result in results_div[:2]:
                text = result.get_text(strip=True)
                if len(text) > 100:
                    results.append(text[:800])
            time.sleep(1)
        except Exception as e:
            print(f"    百度搜索出错: {e}")
    
    return results

def crawl_chusan(lesson_name):
    """初三网补充"""
    try:
        print(f"  📡 初三网补充...")
        url = f"http://www.chusan.com/zhongkao/{lesson_name}.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=6)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('article') or soup.find('div', class_='content')
            if content:
                return content.get_text(strip=True)[:1000]
    except:
        pass
    return ""

def generate_note(lesson_name, hanchacha_data, other_materials):
    """生成笔记，优先使用 hanchacha 的数据"""
    
    # 提取 hanchacha 的数据
    knowledge = hanchacha_data.get("knowledge", "")
    notes = hanchacha_data.get("notes", "")
    exercises = hanchacha_data.get("exercises", "")
    
    # 合并其他网站的资料
    other_text = "\n\n".join(other_materials) if other_materials else ""
    
    # 如果 hanchacha 没找到资料，使用其他来源
    if not knowledge and not notes:
        main_content = other_text if other_text else f"《{lesson_name}》是一篇优美的课文，建议查阅教材学习。"
    else:
        main_content = ""
        if knowledge:
            main_content += f"\n### 📖 知识点整理\n{knowledge}\n\n"
        if notes:
            main_content += f"\n### 📝 课堂笔记\n{notes}\n\n"
        if exercises:
            main_content += f"\n### ✏️ 同步习题\n{exercises}\n\n"
        if other_text:
            main_content += f"\n### 🔗 其他网站补充\n{other_text[:1000]}\n\n"
    
    # 生成笔记
    note = f"""# 📖 {lesson_name} · 智能笔记

> 本笔记由网络爬虫自动收集整理
> **优先来源**：hanchacha.com 语文同步
> 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📚 一、课文资料

{main_content}

---

## 📝 二、生字词积累

请根据课文内容填写：

| 生字 | 拼音 | 组词 | 造句 |
|------|------|------|------|
| | | | |
| | | | |
| | | | |

---

## ✨ 三、重点句子赏析

请抄写你认为最精彩的句子：

> ________________________________
> 
> ________________________________

**我的理解**：________________________________

---

## 🎯 四、课文结构分析

| 部分 | 自然段 | 主要内容 |
|------|--------|----------|
| 开头 | | |
| 经过 | | |
| 结尾 | | |

---

## 💡 五、中心思想

这篇课文主要写了：________________________________

表达了作者：________________________________

---

## 📝 六、我的思考

通过学习这篇课文，我学到了：________________________________

---

## 🎯 七、课后练习

1. **朗读**：有感情地朗读课文3遍
2. **背诵**：背诵指定段落
3. **仿写**：模仿课文写法，写一段话
4. **拓展**：在 hanchacha.com 上查找更多关于《{lesson_name}》的资料

---

*✨ 每天进步一点点！* 
*🔍 数据来源：hanchacha.com（优先）、百度搜索、初三网*
"""
    return note

def main():
    if len(sys.argv) < 2:
        print("请提供课文名称")
        sys.exit(1)
    
    lesson_name = sys.argv[1]
    print("=" * 50)
    print(f"🕷️ 正在为《{lesson_name}》爬取教学资料...")
    print("=" * 50)
    
    # 1. 优先爬取 hanchacha
    print("\n⭐ [优先] 爬取 hanchacha.com...")
    hanchacha_data = crawl_hanchacha(lesson_name)
    
    # 2. 其他网站作为补充
    other_materials = []
    
    print("\n📡 [补充] 百度搜索...")
    baidu_results = crawl_baidu(lesson_name)
    other_materials.extend(baidu_results)
    
    print("\n📡 [补充] 初三网...")
    chusan_result = crawl_chusan(lesson_name)
    if chusan_result:
        other_materials.append(chusan_result)
        print(f"    找到内容")
    else:
        print(f"    未找到")
    
    # 统计结果
    has_hanchacha = any([hanchacha_data.get("knowledge"), hanchacha_data.get("notes"), hanchacha_data.get("exercises")])
    
    if has_hanchacha:
        print(f"\n✅ 从 hanchacha 找到资料！")
    else:
        print(f"\n⚠️ hanchacha 未找到《{lesson_name}》，使用其他来源")
    
    print(f"   其他来源共 {len(other_materials)} 条资料")
    
    # 生成笔记
    print("\n📝 正在生成笔记...")
    note = generate_note(lesson_name, hanchacha_data, other_materials)
    
    # 保存到文件
    os.makedirs('data', exist_ok=True)
    output_file = f"data/{lesson_name}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(note)
    
    print(f"\n✅ 笔记已保存: {output_file}")
    print("=" * 50)

if __name__ == "__main__":
    main()
