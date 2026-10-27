# EgoDemo 学习文章

这里集中维护 EgoDemo 相关的博客文章、配图和阅读页。正文以 Markdown 为主，Git 记录每次修改，方便查看改了什么、需要时也能恢复旧版本。

## 目录

- `articles/`：文章 Markdown 源稿。
- `assets/`：配图、GIF 和短视频。
- `site/`：生成后的 HTML 阅读页。
- `source_evidence/`：用于核对文章数据的汇总文件。
- `docs/`：发布说明。
- `dist/`：生成的发布素材包，不纳入 Git。

## 修改和预览

1. 编辑 `articles/` 里的 Markdown。配图放进 `assets/`，正文用相对路径引用。
2. 安装一次构建依赖：`python3 -m pip install -r requirements.txt`
3. 生成 HTML 和发布素材包：`python3 scripts/build.py`
4. 用浏览器打开 `site/index.html` 预览。

## 保存修改

```bash
git status
git diff
git add articles assets site docs source_evidence README.md scripts requirements.txt
git commit -m "说明这次改了什么"
```

Git 暂时只在本机记录修改，项目没有配置远程仓库。
