from pathlib import Path
import re
import json
import shutil
import zipfile
import markdown

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
SITE = ROOT / "site"
DIST = ROOT / "dist"

CSS = """
:root{--ink:#20343c;--muted:#657a80;--accent:#008f83;--line:#dce5e3;--bg:#f4f7f5}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.9 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}a{color:#007c73;text-decoration:none}a:hover{text-decoration:underline}header{background:#17343d;color:#fff;padding:34px max(6vw,24px)}header p{margin:0;letter-spacing:.1em;font-size:13px;color:#b9d7d3}header strong{display:block;font-size:25px;margin:8px 0}header span{font-size:14px;color:#d1e3df}.layout{display:grid;grid-template-columns:265px minmax(0,940px);gap:34px;max-width:1300px;margin:32px auto;padding:0 24px}aside{position:sticky;top:20px;align-self:start;max-height:94vh;overflow:auto;font-size:13px;line-height:1.65;padding:18px 12px;background:#fff;border:1px solid var(--line);border-radius:12px}aside ul{list-style:none;margin:0;padding-left:12px}aside>div>ul{padding:0}aside li{margin:9px 0}aside ul ul{border-left:1px solid var(--line);font-size:12px}article{min-width:0;padding:38px 44px;background:#fff;border:1px solid var(--line);border-radius:16px}h1{font-size:31px;line-height:1.5;margin:0 0 22px}h2{font-size:25px;line-height:1.55;margin:52px 0 18px;padding-top:8px}h3{font-size:20px;margin:30px 0 12px}p{margin:16px 0}li{margin:6px 0}strong{color:#153f45}blockquote{margin:22px 0;padding:8px 20px;border-left:4px solid var(--accent);background:#eff7f4;font-size:15px}img,video{display:block;max-width:100%;height:auto;margin:24px auto;border-radius:10px;border:1px solid #e6ece9}pre{overflow:auto;background:#17343d;color:#e8f3ef;border-radius:10px;padding:20px;font:13px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace}code{background:#edf3f1;border-radius:4px;padding:2px 5px;font-size:.88em;overflow-wrap:anywhere}pre code{padding:0;background:none;font-size:inherit;overflow-wrap:normal}table{display:block;overflow:auto;width:100%;border-collapse:collapse;font-size:14px;margin:24px 0}th,td{border:1px solid var(--line);padding:10px 13px;min-width:100px;text-align:left}th{background:#eaf3ef}tr:nth-child(even){background:#f8faf9}hr{border:0;border-top:1px solid var(--line);margin:40px 0}footer{text-align:center;color:var(--muted);font-size:13px;margin:28px 20px 40px}.toplink{display:inline-block;margin:10px 0}
@media(max-width:1000px){.layout{display:block;max-width:880px}aside{position:static;max-height:360px;margin-bottom:24px}aside ul ul{display:none}article{padding:28px}}@media(max-width:600px){body{font-size:16px}.layout{padding:0 12px;margin:16px auto}article{padding:22px 18px}h1{font-size:25px}h2{font-size:22px}pre{padding:14px;font-size:12px}header{padding:24px}header strong{font-size:21px}}@media print{header,aside,footer{display:none}.layout{display:block;margin:0;padding:0}article{border:0;padding:0}body{background:#fff}h2,h3{break-after:avoid}img,table,pre{break-inside:avoid}a{color:inherit}}
"""


def article_dirs():
    found = []
    for folder in ARTICLES.iterdir():
        if folder.is_dir() and not folder.name.startswith("_") and (folder / "article.json").is_file() and (folder / "index.md").is_file():
            meta = json.loads((folder / "article.json").read_text(encoding="utf-8"))
            found.append((folder, meta))
    return sorted(found, key=lambda item: (item[1].get("date", ""), item[0].name), reverse=True)


INDEX_CSS = """
*{box-sizing:border-box}body{margin:0;background:#f4f7f5;color:#20343c;font:17px/1.8 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}header{background:#17343d;color:white;padding:64px max(7vw,24px)}header p{margin:0;color:#b9d7d3;font-size:14px}header h1{font-size:36px;margin:12px 0 4px}header span{color:#d1e3df}.wrap{max-width:1060px;margin:40px auto;padding:0 24px}.count{color:#657a80;font-size:14px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}.card{display:block;background:white;color:inherit;text-decoration:none;padding:24px;border:1px solid #dce5e3;border-radius:14px;transition:transform .15s,box-shadow .15s}.card:hover{transform:translateY(-2px);box-shadow:0 10px 28px #17343d16}.date{font-size:13px;color:#657a80}.card h2{font-size:22px;margin:10px 0}.card p{margin:8px 0;color:#435b61}.tag{display:inline-block;background:#eff7f4;color:#007c73;border-radius:99px;padding:2px 10px;font-size:12px;margin:10px 5px 0 0}footer{text-align:center;color:#657a80;font-size:13px;margin:60px 12px 32px}@media(max-width:600px){header h1{font-size:29px}.wrap{padding:0 14px}}
"""


def render_article(folder, meta):
    source = (folder / "index.md").read_text(encoding="utf-8")
    parser = markdown.Markdown(extensions=["extra", "toc", "sane_lists"], extension_configs={"toc": {"toc_depth": "2-3"}})
    body = parser.convert(source)
    title = meta.get("title") or re.search(r"^#\s+(.+)$", source, re.M).group(1).strip()
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{meta.get('summary', '')}"><title>{title}</title><style>{CSS}</style></head>
<body id="top"><header><p>个人 Blog · 学习记录</p><strong>{title}</strong><span>{meta.get('date', '')}</span></header>
<div class="layout"><aside aria-label="文章目录"><b>文章目录</b>{parser.toc}<a class="toplink" href="#top">↑ 回到顶部</a><p><a href="../index.html">← 全部文章</a></p></aside><article>{body}</article></div>
<footer>图片与动画为原创教学示意。动画采用合成数据，非 EgoDemo 原始采集或模型预测。</footer></body></html>'''
    out = SITE / folder.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    for name in ("assets", "source_evidence"):
        source_dir = folder / name
        target_dir = out / name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if source_dir.is_dir():
            shutil.copytree(source_dir, target_dir)


def build_index(entries):
    cards = []
    for folder, meta in entries:
        tags = "".join(f'<span class="tag">{tag}</span>' for tag in meta.get("tags", []))
        cards.append(f'<a class="card" href="{folder.name}/index.html"><span class="date">{meta.get("date", "")}</span><h2>{meta["title"]}</h2><p>{meta.get("summary", "")}</p>{tags}</a>')
    listing = "\n".join(cards) or "<p>这里还没有文章。复制 articles/_template/，开始写第一篇吧。</p>"
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="个人博客文章合集"><title>文章合集 · 我的 Blog</title><style>{INDEX_CSS}</style></head><body><header><p>个人 Blog · 文章合集</p><h1>我的文章</h1><span>学习记录、项目实践与随笔</span></header><main class="wrap"><p class="count">目前收录 {len(entries)} 篇</p><section class="cards">{listing}</section></main><footer>新文章会自动出现在这里</footer></body></html>'''
    (SITE / "index.html").write_text(page, encoding="utf-8")


def build_package(folder):
    page_dir = SITE / folder.name
    package = DIST / f"{folder.name}.zip"
    paths = [folder / "article.json", folder / "index.md"]
    for base in (folder, page_dir):
        for name in ("assets", "source_evidence"):
            subdir = base / name
            if subdir.is_dir():
                paths.extend(sorted(path for path in subdir.rglob("*") if path.is_file()))
    paths.append(page_dir / "index.html")
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.relative_to(ROOT))


def main():
    SITE.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)
    for child in SITE.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
    for old_zip in DIST.glob("*.zip"):
        old_zip.unlink()
    entries = article_dirs()
    for folder, meta in entries:
        render_article(folder, meta)
    build_index(entries)
    for folder, _ in entries:
        build_package(folder)
    print(f"已生成合集首页：{SITE / 'index.html'}（{len(entries)} 篇）")
    print("单篇阅读页和发布包已生成到 site/ 与 dist/。")


if __name__ == "__main__":
    main()
