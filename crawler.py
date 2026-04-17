# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
import re
from bs4 import BeautifulSoup

# 从环境变量读取 API Key
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")

def crawl_hanchacha(lesson_name):
    """从 hanchacha.com 爬取所有相关资料"""
    print(f"  🔍 正在从 hanchacha.com 搜索《{lesson_name}》...")
    
    all_text = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        search_url = f"https://hanchacha.com/?s={lesson_name}"
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        found_urls = []
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().lower()
            if lesson_name.lower() in text and 'hanchacha.com' in href:
                if href not in found_urls:
                    found_urls.append(href)
        
        print(f"    找到 {len(found_urls)} 个相关页面")
        
        for url in found_urls[:3]:
            try:
                page_resp = requests.get(url, headers=headers, timeout=10)
                page_soup = BeautifulSoup(page_resp.text, 'html.parser')
                content_div = page_soup.find('article') or page_soup.find('div', class_='entry-content')
                
                if content_div:
                    text = content_div.get_text(strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    all_text += f"\n\n---\n{text[:1500]}"
            except:
                continue
                
    except Exception as e:
        print(f"  hanchacha 爬取失败: {e}")
    
    return all_text[:4000]

def generate_with_ai(lesson_name, raw_materials):
    """使用 AI 生成详细的学霸笔记"""
    
    print(f"  🤖 AI 状态: {'已启用' if ZHIPU_API_KEY else '未配置'}")
    
    if not ZHIPU_API_KEY:
        return generate_fallback_note(lesson_name, raw_materials)
    
    try:
        print("  🤖 正在调用智谱 AI API...")
        
        # 合并爬取的资料
        detailed_materials = raw_materials if raw_materials else f"无网络资料，请根据课文《{lesson_name}》合理推断内容"
        
        prompt = f"""你是小学语文特级教师，有20年教学经验。请为课文《{lesson_name}》生成一份超级详细、超级专业的学霸综合笔记。

【写作要求 - 必须严格遵守！！！】
1. 内容必须极其详细、详实、完整
2. 表格必须100%填满，不能有任何空项
3. 禁止使用"请根据课文填写"、"略"、"待补充"等敷衍性语句
4. 如果不确定具体内容，请根据课文标题合理推断小学二三年级水平的内容并详细写出
5. 字数要求：至少3000字以上
6. 每个章节都要有实质性内容，不能蜻蜓点水

【笔记完整结构 - 必须全部包含】：

# 🌸 探秘{lesson_name} · 小学霸综合笔记 🌸

> 📚 一份集**知识点、课堂笔记、写作技巧、练习题目**于一体的超实用手册

---

## 📖 一、课文基本信息

### 课文档案卡

| 项目 | 内容 |
|------|------|
| 课文名称 | {lesson_name} |
| 课文类型 | （判断类型：写景散文/写人记事/科普说明文/童话故事等） |
| 适合年级 | 小学X年级 |
| 课文特点 | （详细描述课文特色，如：语言优美/故事生动/道理深刻等） |

### 课文简介（至少300字）
（详细描述课文的写作背景、内容主题、表达情感等，可以合理推断）

---

## 🔍 二、文章结构分析

### 结构概览

| 结构部分 | 包含段落 | 主要内容 | 写作作用 |
|----------|---------|----------|----------|
| 开头 | 第X段 | （详细描述开头内容，如：描写了什么、怎么描写的） | （分析开头的巧妙之处，如：开门见山/设置悬念/引出下文等） |
| 主体 | 第X-X段 | （详细描述主体内容，按顺序描述每个段落或层次） | （分析主体内容如何层层递进/对比呈现/具体展开等） |
| 结尾 | 第X段 | （详细描述结尾内容） | （分析结尾的作用，如：总结全文/点明中心/升华主题等） |

### 段落详解
**第1段**：写了什么内容，用了什么手法，表达什么
**第2段**：写了什么内容，用了什么手法，表达什么
（继续详细分析每一段）

---

## ✍️ 三、写作特色深挖

### 修辞手法分析

| 修辞手法 | 例句原文 | 出处段落 | 表达效果分析 |
|----------|----------|----------|--------------|
| 比喻 | （完整摘录使用了"像""如""仿佛"等比喻词的句子） | 第X段 | （分析把什么比作什么，生动形象地写出...） |
| 拟人 | （完整摘录把物当作人来写的句子） | 第X段 | （分析把XX当作XX来写，赋予了XX人的XX行为，写出...） |
| 排比 | （完整摘录三个及以上相同句式的句子） | 第X段 | （分析增强了语气，突出强调了...） |
| 夸张 | （摘录夸张句） | 第X段 | （分析突出强调了什么，给人深刻印象） |

### 重点句子解析

> **句子1**：
> - **原文**：（完整摘录优美句子）
> - **理解**：（详细分析句子的含义和表达效果）
> - **仿写技巧**：（这个句式可以用于什么场景的写作）

> **句子2**：
> - **原文**：（完整摘录）
> - **理解**：（详细分析）
> - **仿写技巧**：（仿写建议）

---

## 📝 四、字词知识大盘点

### 会写字

| 生字 | 拼音 | 部首 | 笔画 | 常见组词 |
|------|------|------|------|----------|
| （根据课文推测重点生字） | | | | |
| （继续列出更多生字） | | | | |
| | | | | |

### 多音字

| 字 | 读音 | 词语 | 含义 |
|----|------|------|------|
| （课文中的多音字） | | | |

### 近义词

| 词语 | 近义词（2-3个） |
|------|----------------|
| （课文中的重点词语） | |
| | |

### 反义词

| 词语 | 反义词 |
|------|--------|
| （课文中的重点词语） | |
| | |

### 四字词语/AABC式/ABAC式

| 词语类型 | 课文中的词语 |
|----------|--------------|
| 四字词语 | |
| AABC式 | |
| ABAC式 | |

---

## 🖋️ 五、句式训练营

### 仿写练习1

> **句式**：课文中出现的优美句式（如"有的...有的...有的..."）
> - **原句**：（完整摘录课文原句）
> - **仿写1**：夏天到了，公园里的花开了，有的好像（ ），有的好像（ ），还有的好像（ ）。
> - **仿写2**：下课了，同学们在操场上活动，有的在（ ），有的在（ ），还有的在（ ）。

### 仿写练习2

> **句式**：另一个重要句式
> - **原句**：（摘录）
> - **仿写**：（自己仿写）

---

## 🎯 六、课后挑战

1. **背诵小达人**
   - 要求：背诵课文第X-X段
   - 技巧：（背诵方法，如：先理解再背诵/关键词背诵法等）
   - 奖励：背熟后可以画一颗星！

2. **小小演说家**
   - 任务：（根据课文主题设计的演讲任务，如：向大家介绍春天来了的变化）
   - 准备：先说给爸爸妈妈听，让他们帮你提建议
   - 目标：说得清楚、有条理

3. **写作小能手**
   - 题目：（根据课文主题拟定的小练笔，如：以"我眼中的春天"为题写一段话）
   - 要求：（具体写作要求）
   - 字数：XX字以上
   - 小技巧：（写作建议）

4. **知识小达人**
   - 挑战：把今天学到的修辞手法讲给家人听
   - 要求：能说出至少2种修辞手法，并能举出例子

---

## 🌟 七、知识点拓展

### 延伸阅读
（推荐1-2篇同类型或同主题的文章/书籍，如：读了《春天来了》，还可以读《春雨的色彩》《找春天》等）

### 趣味小知识
（与课文相关的趣味小知识，增加学习兴趣，如：春天的花为什么是五颜六色的？）

### 小测验（自己检测一下）
1. 课文主要写了什么？
2. 文中用了哪些修辞手法？请举例。
3. 你最喜欢课文中的哪句话？为什么？

---

【参考材料】
{detailed_materials[:5000]}

请严格按照以上格式生成笔记，确保：
✅ 内容详实完整
✅ 字数3000字以上
✅ 表格全部填满
✅ 每个章节都有实质性内容"""

        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": "你是小学语文特级教师，擅长写超详细、超专业的课文笔记。必须生成3000字以上的详细笔记，每个章节都要填满内容，禁止留空。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.9,
                "max_tokens": 8000
            },
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            note = result["choices"][0]["message"]["content"]
            print(f"  ✅ AI 生成成功！笔记长度: {len(note)} 字")
            return note
        else:
            print(f"  ⚠️ AI 调用失败: {response.status_code}")
            return generate_fallback_note(lesson_name, raw_materials)
            
    except Exception as e:
        print(f"  ⚠️ AI 异常: {e}")
        return generate_fallback_note(lesson_name, raw_materials)

def generate_fallback_note(lesson_name, raw_materials):
    """备用笔记"""
    return f"""# 📖 {lesson_name} · 学习笔记

> 正在努力生成中...

---

## 📚 课文内容

{raw_materials[:500] if raw_materials else f"《{lesson_name}》是一篇优美的课文。"}

---

## 📝 学习建议

1. 朗读课文3遍
2. 标出生字词
3. 思考课文主要内容

---

*生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}*
"""

def main():
    if len(sys.argv) < 2:
        print("请提供课文名称")
        sys.exit(1)
    
    lesson_name = sys.argv[1]
    print("=" * 50)
    print(f"🕷️ 正在为《{lesson_name}》生成笔记...")
    print(f"🤖 智谱 AI API: {'已配置' if ZHIPU_API_KEY else '未配置'}")
    print("=" * 50)
    
    print("\n⭐ 爬取 hanchacha.com...")
    hanchacha_text = crawl_hanchacha(lesson_name)
    
    print("\n🤖 调用 AI 生成笔记...")
    note = generate_with_ai(lesson_name, hanchacha_text)
    
    os.makedirs('data', exist_ok=True)
    output_file = f"data/{lesson_name}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(note)
    
    print(f"\n✅ 笔记已保存: {output_file}")

if __name__ == "__main__":
    main()
