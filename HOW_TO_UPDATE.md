# 如何维护这个网站

以后新增、修改、删除文章，只需要维护 `notes/*.md`。

## 新增文章

在 `notes/` 里新建一个 `.md` 文件，例如：

```md
---
title: 文章标题
date: 2026-07-06
tags: [C++, 课程笔记]
summary: 这一句会显示在首页文章卡片里。
slug: my-note-slug
---

# 文章标题

这里写正文。
```

提交后 GitHub Actions 会自动生成首页和文章页。

## 修改文章

直接修改对应的 `.md` 文件并提交。

## 删除文章

删除对应的 `.md` 文件并提交。下一次自动构建时，生成出来的文章页也会被移除。

## 在线编辑入口

打开：

`https://github.dev/liangdingguan/liangdingguan.github.io`

它会像网页版 VS Code 一样编辑仓库。
