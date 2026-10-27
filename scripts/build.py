from pathlib import Path
import re
import zipfile
import markdown

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "articles" / "egodemo-learning-log.md"
OUTPUT = ROOT / "site" / "index.html"

CSS = """
:root{--ink:#20343c;--muted:#657a80;--accent:#008f83;--line:#dce5e3;--bg:#f4f7f5}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.9 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}a{color:#007c73;text-decoration:none}a:hover{text-decoration:underline}header{background:#17343d;color:#fff;padding:34px max(6vw,24px)}header p{margin:0;letter-spacing:.1em;font-size:13px;color:#b9d7d3}header strong{display:block;font-size:25px;margin:8px 0}header span{font-size:14px;color:#d1e3df}.layout{display:grid;grid-template-columns:265px minmax(0,940px);gap:34px;max-width:1300px;margin:32px auto;padding:0 24px}aside{position:sticky;top:20px;align-self:start;max-height:94vh;overflow:auto;font-size:13px;line-height:1.65;padding:18px 12px;background:#fff;border:1px solid var(--line);border-radius:12px}aside ul{list-style:none;margin:0;padding-left:12px}aside>div>ul{padding:0}aside li{margin:9px 0}aside ul ul{border-left:1px solid var(--line);font-size:12px}article{min-width:0;padding:38px 44px;background:#fff;border:1px solid var(--line);border-radius:16px}h1{font-size:31px;line-height:1.5;margin:0 0 22px}h2{font-size:25px;line-height:1.55;margin:52px 0 18px;padding-top:8px}h3{font-size:20px;margin:30px 0 12px}p{margin:16px 0}li{margin:6px 0}strong{color:#153f45}blockquote{margin:22px 0;padding:8px 20px;border-left:4px solid var(--accent);background:#eff7f4;font-size:15px}img,video{display:block;max-width:100%;height:auto;margin:24px auto;border-radius:10px;border:1px solid #e6ece9}pre{overflow:auto;background:#17343d;color:#e8f3ef;border-radius:10px;padding:20px;font:13px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace}code{background:#edf3f1;border-radius:4px;padding:2px 5px;font-size:.88em;overflow-wrap:anywhere}pre code{padding:0;background:none;font-size:inherit;overflow-wrap:normal}table{display:block;overflow:auto;width:100%;border-collapse:collapse;font-size:14px;margin:24px 0}th,td{border:1px solid var(--line);padding:10px 13px;min-width:100px;text-align:left}th{background:#eaf3ef}tr:nth-child(even){background:#f8faf9}hr{border:0;border-top:1px solid var(--line);margin:40px 0}footer{text-align:center;color:var(--muted);font-size:13px;margin:28px 20px 40px}.toplink{display:inline-block;margin:10px 0}
@media(max-width:1000px){.layout{display:block;max-width:880px}aside{position:static;max-height:360px;margin-bottom:24px}aside ul ul{display:none}article{padding:28px}}@media(max-width:600px){body{font-size:16px}.layout{padding:0 12px;margin:16px auto}article{padding:22px 18px}h1{font-size:25px}h2{font-size:22px}pre{padding:14px;font-size:12px}header{padding:24px}header strong{font-size:21px}}@media print{header,aside,footer{display:none}.layout{display:block;margin:0;padding:0}article{border:0;padding:0}body{background:#fff}h2,h3{break-after:avoid}img,table,pre{break-inside:avoid}a{color:inherit}}
"""

source = ARTICLE.read_text(encoding="utf-8")
parser = markdown.Markdown(
    extensions=["extra", "toc", "sane_lists"],
    extension_configs={"toc": {"toc_depth": "2-3"}},
)
body = parser.convert(source)
title = re.search(r"^#\s+(.+)$", source, re.M).group(1).strip()
html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="EgoDemo 与具身智能数据学习记录。"><title>{title}</title><style>{CSS}</style></head>
<body id="top"><header><p>个人学习记录</p><strong>{title}</strong><span>EgoDemo · 可离线阅读</span></header>
<div class="layout"><aside aria-label="文章目录"><b>文章目录</b>{parser.toc}<a class="toplink" href="#top">↑ 回到顶部</a></aside><article>{body}</article></div>
<footer>图片与动画为原创教学示意。动画采用合成数据，非 EgoDemo 原始采集或模型预测。</footer></body></html>'''
OUTPUT.write_text(html, encoding="utf-8")

package = ROOT / "dist" / "EgoDemo博客与配图素材.zip"
include = [ROOT / "README.md", ARTICLE, OUTPUT, ROOT / "requirements.txt"]
include += sorted((ROOT / "assets").glob("*"))
include += sorted((ROOT / "docs").glob("*"))
include += sorted((ROOT / "source_evidence").glob("*"))
with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in include:
        archive.write(path, path.relative_to(ROOT))
print(f"已生成阅读页：{OUTPUT}")
print(f"已生成发布素材包：{package}")
