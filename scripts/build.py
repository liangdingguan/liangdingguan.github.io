import html
import json
import pathlib
import re
import shutil
from datetime import date


ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
POSTS_DIR = ROOT / "posts"


LEGACY_POSTS = [
    {
        "title": "进程、线程、协程",
        "url": "/2020/05/12/%E8%BF%9B%E7%A8%8B%E3%80%81%E7%BA%BF%E7%A8%8B%E3%80%81%E5%8D%8F%E7%A8%8B/",
        "summary": "整理并发相关基础概念，区分进程、线程与协程的职责边界。",
        "date": "2020/05/12",
        "tags": "Python 相关",
    },
    {
        "title": "Python 深入理解",
        "url": "/2020/05/12/python%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3/",
        "summary": "围绕 Python 面向对象、继承、初始化流程和常见语言特性做复习。",
        "date": "2020/05/12",
        "tags": "Python 相关",
    },
    {
        "title": "Beautiful Soup 重点简述",
        "url": "/2020/04/08/beautiful-%E9%87%8D%E7%82%B9%E7%AE%80%E8%BF%B0/",
        "summary": "记录 Beautiful Soup 的对象类型、选择方式和爬虫解析常用操作。",
        "date": "2020/04/08",
        "tags": "爬虫",
    },
    {
        "title": "基本语法部分（持续更新）",
        "url": "/2020/04/07/%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E9%83%A8%E5%88%86-%E6%8C%81%E7%BB%AD%E6%9B%B4%E6%96%B0/",
        "summary": "英语语法与基础概念笔记，适合作为长期补充的知识清单。",
        "date": "2020/04/07",
        "tags": "英语",
    },
    {
        "title": "Python 基础复习笔记 v1.0",
        "url": "/2020/04/07/Python%E5%9F%BA%E7%A1%80%E5%A4%8D%E4%B9%A0%E7%AC%94%E8%AE%B0-v1-0/",
        "summary": "从标识符、关键字、函数、切片等角度回顾 Python 基础。",
        "date": "2020/04/07",
        "tags": "Python 相关",
    },
    {
        "title": "异步、同步，并发、并行，阻塞非阻塞",
        "url": "/2020/04/07/%E5%BC%82%E6%AD%A5%E3%80%81%E5%90%8C%E6%AD%A5%EF%BC%8C%E5%B9%B6%E5%8F%91%E3%80%81%E5%B9%B6%E8%A1%8C%EF%BC%8C%E9%98%BB%E5%A1%9E%E9%9D%9E%E9%98%BB%E5%A1%9E/",
        "summary": "把容易混淆的执行模型概念放在一起对比。",
        "date": "2020/04/07",
        "tags": "计算机网络相关",
    },
]

ARCHIVE_LINKS = [
    ("会话保持与负载均衡", "/2020/04/05/%E4%BC%9A%E8%AF%9D%E4%BF%9D%E6%8C%81%E4%B8%8E%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1/"),
    ("计算机存储单位", "/2020/03/31/%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%AD%98%E5%82%A8%E5%8D%95%E4%BD%8D/"),
    ("XPath 等", "/2020/03/31/xpath%E7%AD%89/"),
    ("正则表达式", "/2020/03/31/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/"),
]


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "note"


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    meta = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key.strip()] = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        else:
            meta[key.strip()] = value.strip("'\"")
    return meta, body


def inline(text):
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def table_block(lines):
    rows = []
    for line in lines:
        cells = [inline(cell.strip()) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    out = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    out.extend(f"<th>{cell}</th>" for cell in rows[0])
    out.append("</tr></thead><tbody>")
    for row in rows[2:]:
        out.append("<tr>")
        out.extend(f"<td>{cell}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def markdown_to_html(md):
    lines = md.splitlines()
    out = []
    paragraph = []
    list_stack = []
    in_code = False
    code_lang = ""
    code_lines = []
    i = 0

    def close_paragraph():
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + inline(" ".join(paragraph).strip()) + "</p>")
            paragraph = []

    def close_lists(to_level=0):
        while len(list_stack) > to_level:
            out.append("</ul>")
            list_stack.pop()

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if stripped.startswith("```"):
            close_paragraph()
            close_lists()
            if not in_code:
                in_code = True
                code_lang = stripped[3:].strip()
                code_lines = []
            else:
                cls = f" class=\"language-{html.escape(code_lang)}\"" if code_lang else ""
                out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code_lines))}</code></pre>")
                in_code = False
                code_lang = ""
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        if not stripped:
            close_paragraph()
            close_lists()
            i += 1
            continue

        if stripped == "---":
            close_paragraph()
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            close_paragraph()
            close_lists()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(table_block(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            close_paragraph()
            close_lists()
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_paragraph()
            close_lists()
            out.append(f"<blockquote>{inline(stripped.lstrip('>').strip())}</blockquote>")
            i += 1
            continue

        item = re.match(r"^(\s*)-\s+(.+)$", raw)
        if item:
            close_paragraph()
            indent = len(item.group(1).replace("\t", "    "))
            level = indent // 2 + 1
            while len(list_stack) < level:
                out.append("<ul>")
                list_stack.append("ul")
            close_lists(level)
            out.append(f"<li>{inline(item.group(2).strip())}</li>")
            i += 1
            continue

        close_lists()
        paragraph.append(stripped)
        i += 1

    close_paragraph()
    close_lists()
    return "\n".join(out)


def excerpt_from(markdown):
    text = re.sub(r"```.*?```", "", markdown, flags=re.S)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"[*_`>|-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:110] + ("..." if len(text) > 110 else "")


def load_notes():
    notes = []
    NOTES_DIR.mkdir(exist_ok=True)
    for path in sorted(NOTES_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        title = meta.get("title") or re.sub(r"^#\s*", "", body.splitlines()[0]).strip()
        slug = meta.get("slug") or slugify(path.stem)
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        notes.append(
            {
                "title": title,
                "slug": slug,
                "date": meta.get("date") or str(date.today()),
                "summary": meta.get("summary") or excerpt_from(body),
                "tags": tags,
                "body": body,
                "source": str(path.relative_to(ROOT)).replace("\\", "/"),
                "url": f"/posts/{slug}/",
            }
        )
    return sorted(notes, key=lambda item: item["date"], reverse=True)


def render_post(note):
    body = markdown_to_html(note["body"])
    tag_text = "、".join(note["tags"]) if note["tags"] else "Notes"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="liangdingguan">
  <meta name="description" content="{html.escape(note['summary'])}">
  <title>{html.escape(note['title'])} | liangdingguan</title>
  <link rel="icon" href="/assets/favicon.ico">
  <link rel="stylesheet" href="/css/redesign.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">liangdingguan</a>
    <nav class="nav" aria-label="主导航">
      <a href="/">首页</a>
      <a href="/#notes">文章</a>
      <a href="/archives/">归档</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>
  <main class="article-page">
    <article class="article-shell">
      <header class="article-hero">
        <p class="eyebrow">{html.escape(tag_text)}</p>
        <h1>{html.escape(note['title'])}</h1>
        <p>{html.escape(note['date'])} · 来源：{html.escape(note['source'])}</p>
      </header>
      <div class="article-content">
{body}
      </div>
    </article>
  </main>
  <footer class="site-footer">
    <a href="/">回到首页</a>
    <span>© liangdingguan</span>
  </footer>
</body>
</html>
"""


def render_index(notes):
    all_count = len(notes) + 10
    dynamic_cards = []
    for note in notes:
        dynamic_cards.append(
            f"""          <article class="post-card featured">
            <a href="{html.escape(note['url'])}">{html.escape(note['title'])}</a>
            <p>{html.escape(note['summary'])}</p>
            <span>{html.escape(note['date'].replace('-', '/'))} · {html.escape('、'.join(note['tags']) or 'Notes')}</span>
          </article>"""
        )
    for item in LEGACY_POSTS:
        dynamic_cards.append(
            f"""          <article class="post-card">
            <a href="{item['url']}">{html.escape(item['title'])}</a>
            <p>{html.escape(item['summary'])}</p>
            <span>{item['date']} · {html.escape(item['tags'])}</span>
          </article>"""
        )
    archive_links = "\n".join(f'        <a href="{url}">{html.escape(title)}</a>' for title, url in ARCHIVE_LINKS)
    post_cards = "\n".join(dynamic_cards)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="liangdingguan">
  <meta name="description" content="liangdingguan 的个人主页：技术笔记、学习记录与个人链接。">
  <meta property="og:type" content="website">
  <meta property="og:title" content="liangdingguan">
  <meta property="og:description" content="技术笔记、学习记录与个人链接。">
  <meta property="og:url" content="https://liangdingguan.github.io/">
  <title>liangdingguan | 个人主页</title>
  <link rel="icon" href="/assets/favicon.ico">
  <link rel="stylesheet" href="/css/redesign.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">liangdingguan</a>
    <nav class="nav" aria-label="主导航">
      <a href="#notes">文章</a>
      <a href="/archives/">归档</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="hero-inner">
        <p class="eyebrow">Personal Homepage</p>
        <h1>你好，我是 liangdingguan。</h1>
        <p class="hero-copy">这里收集我的技术笔记、学习路线和一些阶段性的思考。以后只需要维护 notes 里的 Markdown，网站会自动生成。</p>
        <div class="hero-actions">
          <a class="button primary" href="#notes">查看文章</a>
          <a class="button" href="mailto:2280426623@qq.com">联系我</a>
        </div>
      </div>
    </section>

    <section class="overview" aria-label="站点概览">
      <article>
        <span class="stat">{all_count}</span>
        <p>篇文章，Markdown 自动发布</p>
      </article>
      <article>
        <span class="stat">notes</span>
        <p>新增、修改、删除都从 notes/*.md 开始</p>
      </article>
      <article>
        <span class="stat">Auto</span>
        <p>GitHub Actions 自动生成页面</p>
      </article>
    </section>

    <section class="content-shell" id="notes">
      <div class="section-heading">
        <p class="eyebrow">Notes</p>
        <h2>最近的技术笔记</h2>
      </div>

      <div class="layout">
        <div class="posts">
{post_cards}
        </div>

        <aside class="profile" aria-label="个人信息">
          <img src="/avatar/Misaka.jpg" alt="liangdingguan 的头像">
          <h2>liangdingguan</h2>
          <p>持续学习，持续记录。现在这个页面可以从 Markdown 自动生成，适合长期维护课程笔记、技术文章和项目记录。</p>
          <div class="profile-links">
            <a href="mailto:2280426623@qq.com">Email</a>
            <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
            <a href="/about/">About</a>
          </div>
        </aside>
      </div>
    </section>

    <section class="archive-strip">
      <div>
        <p class="eyebrow">Archive</p>
        <h2>更多旧文仍然保留</h2>
      </div>
      <div class="archive-links">
{archive_links}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <span>© liangdingguan</span>
    <span>Built from notes/*.md</span>
  </footer>
</body>
</html>
"""


def build_content_json(notes):
    return {
        "meta": {
            "title": "liangdingguan",
            "description": "技术笔记、学习记录与个人链接。",
            "author": "liangdingguan",
            "url": "https://liangdingguan.github.io",
            "root": "/",
        },
        "posts": [
            {
                "title": note["title"],
                "date": note["date"],
                "path": f"posts/{note['slug']}/",
                "permalink": f"https://liangdingguan.github.io/posts/{note['slug']}/",
                "categories": [],
                "tags": [{"name": tag, "slug": slugify(tag), "permalink": ""} for tag in note["tags"]],
            }
            for note in notes
        ],
    }


def main():
    notes = load_notes()
    if POSTS_DIR.exists():
        shutil.rmtree(POSTS_DIR)
    POSTS_DIR.mkdir(exist_ok=True)
    for note in notes:
        target = POSTS_DIR / note["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(render_post(note), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(notes), encoding="utf-8")
    (ROOT / "content.json").write_text(
        json.dumps(build_content_json(notes), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Built {len(notes)} note(s).")


if __name__ == "__main__":
    main()
