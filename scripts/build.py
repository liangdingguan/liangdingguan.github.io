import html
import hashlib
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
        "slug": "legacy-process-thread-coroutine",
        "source": "2020/05/12/进程、线程、协程/index.html",
        "date": "2020-05-12",
        "tags": ["Python 相关"],
        "summary": "进程、线程、协程与并发执行模型的早期学习笔记。",
    },
    {
        "title": "Python 深入理解",
        "slug": "legacy-python-deep-dive",
        "source": "2020/05/12/python深入理解/index.html",
        "date": "2020-05-12",
        "tags": ["Python 相关"],
        "summary": "围绕 Python 面向对象、继承、初始化流程和常见语言特性做复习。",
    },
    {
        "title": "Beautiful Soup 重点简述",
        "slug": "legacy-beautiful-soup-notes",
        "source": "2020/04/08/beautiful-重点简述/index.html",
        "date": "2020-04-08",
        "tags": ["爬虫"],
        "summary": "Beautiful Soup 对象类型、选择方式和爬虫解析常用操作。",
    },
    {
        "title": "Python 基础复习笔记 v1.0",
        "slug": "legacy-python-basic-review",
        "source": "2020/04/07/Python基础复习笔记-v1-0/index.html",
        "date": "2020-04-07",
        "tags": ["Python 相关"],
        "summary": "从标识符、关键字、函数、切片等角度回顾 Python 基础。",
    },
    {
        "title": "基本语法部分（持续更新）",
        "slug": "legacy-basic-grammar",
        "source": "2020/04/07/基本语法部分-持续更新/index.html",
        "date": "2020-04-07",
        "tags": ["英语"],
        "summary": "英语语法与基础概念笔记。",
    },
    {
        "title": "异步、同步，并发、并行，阻塞非阻塞",
        "slug": "legacy-async-sync-concurrency",
        "source": "2020/04/07/异步、同步，并发、并行，阻塞非阻塞/index.html",
        "date": "2020-04-07",
        "tags": ["计算机网络相关"],
        "summary": "同步、异步、并发、并行、阻塞与非阻塞概念对比。",
    },
    {
        "title": "会话保持与负载均衡",
        "slug": "legacy-session-load-balancing",
        "source": "2020/04/05/会话保持与负载均衡/index.html",
        "date": "2020-04-05",
        "tags": ["计算机网络相关"],
        "summary": "会话保持、NAT 与负载均衡基础概念。",
    },
    {
        "title": "计算机存储单位",
        "slug": "legacy-storage-units",
        "source": "2020/03/31/计算机存储单位/index.html",
        "date": "2020-03-31",
        "tags": ["计算机基础"],
        "summary": "bit、byte、KB、MB、GB 等计算机存储单位换算。",
    },
    {
        "title": "XPath 等",
        "slug": "legacy-xpath-notes",
        "source": "2020/03/31/xpath等/index.html",
        "date": "2020-03-31",
        "tags": ["爬虫相关"],
        "summary": "XPath 基础语法与 HTML/XML 节点选择笔记。",
    },
    {
        "title": "正则表达式",
        "slug": "legacy-regex-notes",
        "source": "2020/03/31/正则表达式/index.html",
        "date": "2020-03-31",
        "tags": ["其他"],
        "summary": "正则表达式和 Python re 模块基础笔记。",
    },
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


def extract_legacy_body(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'<article class="article-entry">\s*(.*?)\s*</article>', text, re.S)
    if not match:
        return "<p>旧文章正文提取失败，请查看原始页面。</p>"
    body = match.group(1)
    body = re.sub(r'<script.*?</script>', "", body, flags=re.S)
    return body


def load_notes():
    notes = []
    NOTES_DIR.mkdir(exist_ok=True)
    for path in sorted(NOTES_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        title = meta.get("title") or re.sub(r"^#\s*", "", body.splitlines()[0]).strip()
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        slug = meta.get("slug") or slugify(path.stem)
        notes.append(
            {
                "kind": "note",
                "title": title,
                "slug": slug,
                "date": meta.get("date") or str(date.today()),
                "summary": meta.get("summary") or excerpt_from(body),
                "tags": tags,
                "body": markdown_to_html(body),
                "source": str(path.relative_to(ROOT)).replace("\\", "/"),
                "url": f"/posts/{slug}/",
            }
        )
    return notes


def load_legacy_posts():
    posts = []
    for item in LEGACY_POSTS:
        source = ROOT / item["source"]
        posts.append(
            {
                "kind": "legacy",
                "title": item["title"],
                "slug": item["slug"],
                "date": item["date"],
                "summary": item["summary"],
                "tags": item["tags"],
                "body": extract_legacy_body(source),
                "source": item["source"],
                "url": f"/posts/{item['slug']}/",
                "old_url": "/" + item["source"].replace("index.html", "").replace("\\", "/"),
            }
        )
    return posts


def tag_text(post):
    return "、".join(post["tags"]) if post["tags"] else "Notes"


def collect_categories(posts):
    categories = {}
    for post in posts:
        tags = post["tags"] or ["Notes"]
        for tag in tags:
            categories.setdefault(tag, []).append(post)
    return dict(sorted(categories.items(), key=lambda item: (-len(item[1]), item[0].lower())))


def category_slug(name):
    slug = slugify(name)
    if slug != "note" or name.lower() in {"note", "notes"}:
        return slug
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    return f"topic-{digest}"


def render_post(post):
    old_link = ""
    if post.get("old_url"):
        old_link = f'<p class="article-note">这篇文章从 2020 旧页面迁移而来，旧链接仍保留：<a href="{html.escape(post["old_url"])}">查看旧版</a></p>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="liangdingguan">
  <meta name="description" content="{html.escape(post['summary'])}">
  <title>{html.escape(post['title'])} | liangdingguan</title>
  <link rel="icon" href="/assets/favicon.ico">
  <link rel="stylesheet" href="/css/redesign.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">liangdingguan</a>
    <nav class="nav" aria-label="主导航">
      <a href="/">首页</a>
      <a href="/#notes">文章</a>
      <a href="/posts/">全部文章</a>
      <a href="/categories/">文章分类</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>
  <main class="article-page">
    <article class="article-shell">
      <header class="article-hero">
        <p class="eyebrow">{html.escape(tag_text(post))}</p>
        <h1>{html.escape(post['title'])}</h1>
        <p>{html.escape(post['date'])} · 来源：{html.escape(post['source'])}</p>
      </header>
      <div class="article-content">
        {old_link}
{post['body']}
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


def render_post_cards(posts):
    cards = []
    for post in posts:
        featured = " featured" if post["kind"] == "note" else ""
        cards.append(
            f"""          <article class="post-card{featured}">
            <a href="{html.escape(post['url'])}">{html.escape(post['title'])}</a>
            <p>{html.escape(post['summary'])}</p>
            <span>{html.escape(post['date'].replace('-', '/'))} · {html.escape(tag_text(post))}</span>
          </article>"""
        )
    return "\n".join(cards)


def render_sidebar(posts):
    groups = {}
    for post in posts:
        groups.setdefault(post["date"][:4], []).append(post)

    recent_links = "\n".join(
        f'              <a href="{html.escape(post["url"])}"><span>{html.escape(post["date"][5:].replace("-", "/"))}</span>{html.escape(post["title"])}</a>'
        for post in posts[:5]
    )

    years = sorted(groups.keys(), reverse=True)
    sections = []
    for index, year in enumerate(years):
        links = "\n".join(
            f'              <a href="{html.escape(post["url"])}"><span>{html.escape(post["date"][5:].replace("-", "/"))}</span>{html.escape(post["title"])}</a>'
            for post in groups[year]
        )
        open_attr = " open" if index == 0 else ""
        sections.append(
            f"""          <details class="archive-year-panel"{open_attr}>
            <summary>{html.escape(year)} <span>{len(groups[year])}</span></summary>
            <div class="archive-list">
{links}
            </div>
          </details>"""
        )

    return f"""          <section>
            <h3>最近文章</h3>
            <div class="archive-list">
{recent_links}
            </div>
          </section>
          <a class="archive-all-link" href="/posts/">查看全部文章</a>
          <a class="archive-all-link" href="/categories/">按分类浏览</a>
{chr(10).join(sections)}"""


def render_archive_index(posts):
    groups = {}
    for post in posts:
        groups.setdefault(post["date"][:4], []).append(post)

    sections = []
    for year in sorted(groups.keys(), reverse=True):
        cards = "\n".join(
            f"""          <article class="archive-page-item">
            <a href="{html.escape(post['url'])}">{html.escape(post['title'])}</a>
            <p>{html.escape(post['summary'])}</p>
            <span>{html.escape(post['date'].replace('-', '/'))} · {html.escape(tag_text(post))}</span>
          </article>"""
            for post in groups[year]
        )
        sections.append(
            f"""      <section class="archive-page-year">
        <h2>{html.escape(year)}</h2>
        <div class="archive-page-list">
{cards}
        </div>
      </section>"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="liangdingguan">
  <meta name="description" content="liangdingguan 的全部文章归档。">
  <title>全部文章 | liangdingguan</title>
  <link rel="icon" href="/assets/favicon.ico">
  <link rel="stylesheet" href="/css/redesign.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">liangdingguan</a>
    <nav class="nav" aria-label="主导航">
      <a href="/">首页</a>
      <a href="/posts/">全部文章</a>
      <a href="/categories/">文章分类</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>
  <main class="archive-page">
    <header class="archive-page-hero">
      <p class="eyebrow">Archive</p>
      <h1>全部文章</h1>
      <p>共 {len(posts)} 篇，按年份归档。主页只保留最近文章和折叠入口，这里保留完整列表。</p>
    </header>
{chr(10).join(sections)}
  </main>
  <footer class="site-footer">
    <a href="/">回到首页</a>
    <span>© liangdingguan</span>
  </footer>
</body>
</html>
"""


def render_categories_index(posts):
    categories = collect_categories(posts)
    category_nav = "\n".join(
        f'        <a href="#category-{html.escape(category_slug(name))}">{html.escape(name)}<span>{len(items)}</span></a>'
        for name, items in categories.items()
    )
    sections = []
    for name, items in categories.items():
        cards = "\n".join(
            f"""          <article class="archive-page-item">
            <a href="{html.escape(post['url'])}">{html.escape(post['title'])}</a>
            <p>{html.escape(post['summary'])}</p>
            <span>{html.escape(post['date'].replace('-', '/'))} · {html.escape(tag_text(post))}</span>
          </article>"""
            for post in items
        )
        sections.append(
            f"""      <section class="category-group" id="category-{html.escape(category_slug(name))}">
        <div class="category-heading">
          <h2>{html.escape(name)}</h2>
          <span>{len(items)} 篇</span>
        </div>
        <div class="archive-page-list">
{cards}
        </div>
      </section>"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="liangdingguan">
  <meta name="description" content="liangdingguan 的文章分类索引。">
  <title>文章分类 | liangdingguan</title>
  <link rel="icon" href="/assets/favicon.ico">
  <link rel="stylesheet" href="/css/redesign.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">liangdingguan</a>
    <nav class="nav" aria-label="主导航">
      <a href="/">首页</a>
      <a href="/#notes">文章</a>
      <a href="/posts/">全部文章</a>
      <a href="/categories/">文章分类</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>
  <main class="archive-page">
    <header class="archive-page-hero">
      <p class="eyebrow">Categories</p>
      <h1>文章分类</h1>
      <p>共 {len(posts)} 篇文章，按主题聚合为 {len(categories)} 个分类。点选分类可以快速跳到对应文章列表。</p>
    </header>
    <nav class="category-index" aria-label="文章分类索引">
{category_nav}
    </nav>
{chr(10).join(sections)}
  </main>
  <footer class="site-footer">
    <a href="/">回到首页</a>
    <span>© liangdingguan</span>
  </footer>
</body>
</html>
"""


def render_index(posts):
    post_cards = render_post_cards(posts)
    sidebar = render_sidebar(posts)
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
      <a href="/categories/">文章分类</a>
      <a href="/about/">关于</a>
      <a href="https://github.com/liangdingguan" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </header>

  <main>
    <section class="hero compact-hero">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="hero-inner">
        <p class="eyebrow">Personal Homepage</p>
        <h1>liangdingguan</h1>
        <p class="hero-copy">技术笔记、课程记录和阶段性思考。新文章从 notes/*.md 自动生成，旧文章也已迁移到统一的 posts 阅读样式。</p>
        <div class="hero-actions">
          <a class="button primary" href="#notes">查看文章</a>
          <a class="button" href="mailto:2280426623@qq.com">联系我</a>
          <a class="button" href="/categories/">文章分类</a>
        </div>
      </div>
    </section>

    <section class="overview" aria-label="站点概览">
      <article>
        <span class="stat">{len(posts)}</span>
        <p>篇文章统一收进 posts</p>
      </article>
      <article>
        <span class="stat">notes</span>
        <p>新文章继续维护 notes/*.md</p>
      </article>
      <article>
        <span class="stat">legacy</span>
        <p>2020 旧文已迁移为统一样式</p>
      </article>
    </section>

    <section class="content-shell" id="notes">
      <div class="section-heading">
        <p class="eyebrow">Notes</p>
        <h2>文章</h2>
      </div>

      <div class="home-layout">
        <div class="posts">
{post_cards}
        </div>

        <aside class="archive-sidebar" aria-label="文章归档">
          <div class="sidebar-card profile-mini">
            <img src="/avatar/Misaka.jpg" alt="liangdingguan 的头像">
            <div>
              <h2>liangdingguan</h2>
              <p>持续学习，持续记录。</p>
            </div>
          </div>
          <div class="sidebar-card">
            <p class="eyebrow">Archive</p>
{sidebar}
          </div>
        </aside>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <span>© liangdingguan</span>
    <span>Built from notes/*.md and legacy HTML</span>
  </footer>
</body>
</html>
"""


def build_content_json(posts):
    categories = collect_categories(posts)
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
                "title": post["title"],
                "date": post["date"],
                "path": f"posts/{post['slug']}/",
                "permalink": f"https://liangdingguan.github.io/posts/{post['slug']}/",
                "categories": [{"name": tag, "slug": category_slug(tag), "permalink": f"https://liangdingguan.github.io/categories/#category-{category_slug(tag)}"} for tag in post["tags"]],
                "tags": [{"name": tag, "slug": slugify(tag), "permalink": ""} for tag in post["tags"]],
            }
            for post in posts
        ],
        "categories": [
            {
                "name": name,
                "slug": category_slug(name),
                "permalink": f"https://liangdingguan.github.io/categories/#category-{category_slug(name)}",
                "count": len(items),
            }
            for name, items in categories.items()
        ],
    }


def main():
    posts = load_notes() + load_legacy_posts()
    posts = sorted(posts, key=lambda item: item["date"], reverse=True)
    if POSTS_DIR.exists():
        shutil.rmtree(POSTS_DIR)
    POSTS_DIR.mkdir(exist_ok=True)
    for post in posts:
        target = POSTS_DIR / post["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(render_post(post), encoding="utf-8")
    (POSTS_DIR / "index.html").write_text(render_archive_index(posts), encoding="utf-8")
    categories_dir = ROOT / "categories"
    categories_dir.mkdir(exist_ok=True)
    (categories_dir / "index.html").write_text(render_categories_index(posts), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(posts), encoding="utf-8")
    (ROOT / "content.json").write_text(
        json.dumps(build_content_json(posts), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Built {len(posts)} post(s).")


if __name__ == "__main__":
    main()
