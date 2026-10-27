# 个人 Blog 文章合集

这个仓库用来长期收集和发布多篇博客文章。每篇文章、它自己的图片与视频、阅读页和发布包都按文章分开管理。现在收录的第一篇是 EgoDemo 学习记录；之后可以继续添加其他主题。

## 项目结构

```text
articles/
├── _template/                    # 新文章模板
└── egodemo-learning-log/
    ├── article.json               # 标题、日期、摘要、标签
    ├── index.md                   # Markdown 正文
    ├── assets/                    # 这篇文章自己的图片、GIF、视频
    └── source_evidence/           # 支撑文中数据的资料
site/
├── index.html                     # 全部文章的合集首页
└── egodemo-learning-log/index.html
scripts/build.py                   # 生成首页、单篇页面和发布包
docs/                              # 发布说明
```

## 新增一篇文章

1. 复制 `articles/_template/`，把副本改成简短英文目录名，例如 `robotics-notes`。
2. 编辑该目录下的 `article.json`，填写标题、日期、摘要和标签。
3. 编辑 `index.md` 写正文，图片、GIF 和视频放进自己的 `assets/`，用相对路径引用。
4. 运行 `python3 scripts/build.py`，更新合集首页、各篇 HTML 阅读页和 `dist/` 发布包。
5. 用浏览器打开 `site/index.html` 预览所有文章。

首次构建前安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 保存修改

```bash
git status
git diff
git add articles site docs scripts README.md requirements.txt .gitignore
git commit -m "说明这次改了什么"
```

Git 目前只在本机记录版本，仓库尚未连接 GitHub、GitLab 等远程服务。
