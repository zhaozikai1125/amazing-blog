# amazing-blog

个人 Blog 文章合集。每篇文章单独管理正文、图片、视频和资料；合集首页会自动收录各篇文章。

目前包含 EgoDemo 学习记录和 FineVLA 项目调研，后续可以继续添加其他主题。

## 目录结构

```text
articles/
├── _template/                     # 新文章模板
├── egodemo-learning-log/           # EgoDemo 学习记录
└── FineVLA/                        # FineVLA 项目调研
    ├── article.json                # 标题、日期、摘要和标签
    ├── index.md                    # Markdown 正文
    └── assets/                     # 该文章专用图片和视频
site/
├── index.html                      # 全部文章的合集首页
└── <文章目录>/index.html           # 单篇阅读页
scripts/
├── build.py                        # 构建首页、阅读页和文章发布包
└── preview.sh                      # 启动本地预览
启动博客.command                    # macOS 双击启动入口
docs/                               # 新增和发布文章说明
```

## 一键预览

macOS 上双击 `启动博客.command`。首次运行会在项目内创建 `.venv` 并安装构建依赖，然后生成页面、启动本机预览并打开浏览器。预览地址是 <http://127.0.0.1:8765/>。停止时，在弹出的终端窗口按 `Ctrl+C`。

也可以在终端运行 `./scripts/preview.sh`。

## 新增文章

1. 复制 `articles/_template/`，改成新的文章目录名，例如 `robotics-notes`。
2. 编辑 `article.json`，填写文章标题、日期、摘要和标签。
3. 编辑 `index.md` 写正文，图片和视频放在该篇的 `assets/` 目录下。
4. 重新运行 `./scripts/preview.sh`。新文章会出现在合集首页。

## 保存修改

```bash
git status
git diff
git add articles site docs scripts README.md requirements.txt .gitignore "启动博客.command"
git commit -m "说明这次改了什么"
```

GitHub 远程仓库：<https://github.com/zhaozikai1125/amazing-blog>
