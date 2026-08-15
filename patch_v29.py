# -*- coding: utf-8 -*-
import io, sys

PATH = r"C:\Users\Administrator\WorkBuddy\2026-08-15-14-17-26\site\index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

reps = []

# ---------- 1) CSS: 浮动小窗 + 对话 + 画线 样式（插入到盯盘弹出模式之前） ----------
css_new = (
'\n/* === AI 交易员 · 独立浮动小窗 + 对话 + 画线 === */\n'
'.aiT-panel{display:none;position:fixed;top:84px;right:18px;width:384px;height:580px;min-width:320px;min-height:380px;background:#14110d;border:1px solid var(--gold);border-radius:14px;box-shadow:-10px 14px 44px rgba(0,0,0,.6);z-index:90;flex-direction:column;resize:both;overflow:hidden}\n'
'.aiT-panel.open{display:flex}\n'
'.aiT-panel .aiT-head{cursor:move;user-select:none}\n'
'.aiT-panel .aiT-head h3{font-size:13.5px}\n'
'.aiT-panel .aiT-tabs{margin-left:auto;margin-right:30px}\n'
'.aiT-panel .aiT-body{padding:0;display:flex;flex-direction:column;overflow:hidden}\n'
'.aiT-chat{flex:1;overflow-y:auto;padding:12px 13px;display:flex;flex-direction:column;gap:10px}\n'
'.aiT-msg{font-size:12.5px;line-height:1.7;border-radius:10px;padding:9px 11px;border:1px solid #2a2520}\n'
'.aiT-msg.ai{background:#0f0d0a;border-color:#2a2520;color:#ece5d3}\n'
'.aiT-msg.me{background:#3a2c10;border-color:#5a4318;color:var(--gold2);align-self:flex-end;max-width:88%}\n'
'.aiT-msg .who{font-size:10.5px;color:#8a7d63;margin-bottom:3px;font-weight:700;letter-spacing:.5px}\n'
'.aiT-msg .aiT-plan{font-size:12px;margin:5px 0}\n'
'.aiT-msg .blk{margin-bottom:9px}\n'
'.aiT-msg .blk h4{font-size:12px;color:var(--gold);margin-bottom:5px;border-left:3px solid var(--gold);padding-left:7px}\n'
'.aiT-msg .row{display:flex;justify-content:space-between;font-size:11.5px;padding:2px 0;border-bottom:1px dashed #241f17}\n'
'.aiT-msg .row b{color:#ece5d3}\n'
'.aiT-msg .sup{color:#7fd87a}.aiT-msg .res{color:#ff7a6e}\n'
'.aiT-msg .bias{font-size:12px;padding:8px 10px;border-radius:8px;margin:5px 0;line-height:1.7}\n'
'.aiT-msg .bias.up{background:#13261a;color:#9ad89a;border:1px solid #294d33}\n'
'.aiT-msg .bias.dn{background:#2a1410;color:#ff9a8e;border:1px solid #5a2f28}\n'
'.aiT-msg .bias.mid{background:#2a2410;color:#e8c66a;border:1px solid #4d431f}\n'
'.aiT-msg .warn{font-size:11px;color:#9a8f76;background:#13110d;border:1px solid #2a2520;border-radius:8px;padding:7px 9px;margin-top:7px;line-height:1.65}\n'
'.aiT-msg .bt-tab{width:100%;border-collapse:collapse;font-size:11.5px}\n'
'.aiT-msg .bt-tab td{padding:3px 6px;border-bottom:1px solid #241f17}\n'
'.aiT-msg .bt-good{color:#7fd87a}.aiT-msg .bt-bad{color:#ff7a6e}\n'
'.aiT-input{display:flex;gap:7px;padding:9px 10px;border-top:1px solid #2a2520;background:#1b160f}\n'
'.aiT-input input{flex:1;background:#0f0d0a;border:1px solid #3a3328;border-radius:8px;color:#ece5d3;padding:8px 10px;font-size:12.5px;outline:none}\n'
'.aiT-input input:focus{border-color:var(--gold)}\n'
'.aiT-input button{background:#3a2c10;border:1px solid var(--gold);color:var(--gold2);border-radius:8px;padding:0 14px;cursor:pointer;font-size:12px;font-weight:700}\n'
'.aiT-input button:hover{background:#4a3813}\n'
'.aiT-chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 10px 9px;background:#1b160f}\n'
'.aiT-chip{background:#241e16;border:1px solid #3a3328;color:#b9ab8a;border-radius:20px;padding:4px 10px;font-size:11px;cursor:pointer}\n'
'.aiT-chip:hover{border-color:var(--gold);color:var(--gold2)}\n'
'.aiT-ol-fib{stroke:#9b7bff;stroke-width:1.1;stroke-dasharray:4 3}\n'
'.aiT-ol-gann{stroke:#5fd0c8;stroke-width:1.1}\n'
)
reps.append(("/* 盯盘弹出模式 */", css_new + "/* 盯盘弹出模式 */"))

# ---------- 2) HTML: 面板改为对话结构 ----------
html_old = (
'<!-- AI 分析面板（集成在 MT5 工作区内） -->\n'
'<div class="aiT-panel" id="aiTPanel">\n'
'  <div class="aiT-head">\n'
'    <span class="dot-ai"></span>\n'
'    <h3>🤖 AI 职业黄金交易员</h3>\n'
'    <div class="aiT-tabs" id="aiTTabs">\n'
'      <button class="aiT-tab on" onclick="selectAiTf(\'day\',this)">日线</button>\n'
'      <button class="aiT-tab" onclick="selectAiTf(\'hour\',this)">小时线</button>\n'
'      <button class="aiT-tab" onclick="selectAiTf(\'week\',this)">周线</button>\n'
'    </div>\n'
'    <span class="x" onclick="toggleAiPanel()" title="关闭">×</span>\n'
'  </div>\n'
'  <div class="aiT-body">\n'
'    <div class="aiT-status" id="aiTStatus">点上方<b>日线 / 小时线 / 周线</b>拉取真实历史K线并回测。AI 会实时根据现价更新买卖信号。</div>\n'
'    <div id="aiTOut" class="aiT-out">\n'
'      <div class="warn">点上方<b>日线 / 小时线 / 周线</b>切换分析周期。系统读取实时价与对应周期区间，给出支撑/阻力、多空研判与操作建议。点<b>🎯 投射到走势图</b>可把关键位标到走势图上。</div>\n'
'    </div>\n'
'  </div>\n'
'</div>\n'
)
html_new = (
'<!-- AI 交易员 · 独立浮动小窗（可拖动 / 可缩放 / 可对话下指令） -->\n'
'<div class="aiT-panel" id="aiTPanel">\n'
'  <div class="aiT-head" id="aiTHead">\n'
'    <span class="dot-ai"></span>\n'
'    <h3>🤖 AI 职业黄金交易员</h3>\n'
'    <div class="aiT-tabs" id="aiTTabs">\n'
'      <button class="aiT-tab on" onclick="selectAiTf(\'day\',this)">日线</button>\n'
'      <button class="aiT-tab" onclick="selectAiTf(\'hour\',this)">小时线</button>\n'
'      <button class="aiT-tab" onclick="selectAiTf(\'week\',this)">周线</button>\n'
'    </div>\n'
'    <span class="x" onclick="toggleAiPanel()" title="收起（再点工具栏 🤖 AI分析 打开）">×</span>\n'
'  </div>\n'
'  <div class="aiT-body">\n'
'    <div class="aiT-status" id="aiTStatus">👋 我是你的 AI 黄金交易员，已学习<b>斐波那契</b>、<b>江恩</b>画线法与<b>风险管理</b>体系。点上方周期，或直接在下面对我下指令：<b>画斐波那契线</b> / <b>画江恩线</b> / <b>分析当前走势</b> / <b>给我交易建议</b> / <b>怎么做风险管理</b> / <b>把关键位投射到走势图</b>。</div>\n'
'    <div class="aiT-chat" id="aiTChat"></div>\n'
'    <div class="aiT-chips">\n'
'      <span class="aiT-chip" onclick="aiQuick(\'画斐波那契线\')">📐 画斐波那契</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'画江恩线\')">📏 画江恩线</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'分析当前走势\')">📊 分析走势</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'给我交易建议\')">💡 交易建议</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'怎么做风险管理 止损 仓位\')">🛡️ 风险管理</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'把关键位投射到走势图\')">🎯 投射关键位</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'斐波那契怎么用\')">📚 斐波那契知识</span>\n'
'      <span class="aiT-chip" onclick="aiQuick(\'清除AI画线\')">🧹 清AI画线</span>\n'
'    </div>\n'
'    <div class="aiT-input">\n'
'      <input id="aiTCmd" type="text" placeholder="对 AI 交易员下指令，例如：画斐波那契线并分析支撑…" onkeydown="if(event.key===\'Enter\')aiSendCmd()" />\n'
'      <button onclick="aiSendCmd()">发送</button>\n'
'    </div>\n'
'  </div>\n'
'</div>\n'
)
reps.append((html_old, html_new))

# ---------- 3) toggleAiPanel：加拖动初始化 + 欢迎语 ----------
old3 = (
'function toggleAiPanel(){\n'
'  var p=document.getElementById("aiTPanel");\n'
'  if(!p) return;\n'
'  AI_STATE.open=!AI_STATE.open;\n'
'  if(AI_STATE.open){\n'
'    p.classList.add("open");\n'
'    if(!AI_STATE.data) runAiAnalyze(AI_STATE.tf);\n'
'    if(AI_LIVE_TIMER) clearInterval(AI_LIVE_TIMER);\n'
'    AI_LIVE_TIMER=setInterval(aiLiveTick,15000);\n'
'  } else {\n'
'    p.classList.remove("open");\n'
'    if(AI_LIVE_TIMER){ clearInterval(AI_LIVE_TIMER); AI_LIVE_TIMER=null; }\n'
'  }\n'
'}\n'
)
new3 = (
'function toggleAiPanel(){\n'
'  var p=document.getElementById("aiTPanel");\n'
'  if(!p) return;\n'
'  AI_STATE.open=!AI_STATE.open;\n'
'  if(AI_STATE.open){\n'
'    p.classList.add("open");\n'
'    initAiDrag();\n'
'    if(!AI_STATE.everOpen){ AI_STATE.everOpen=true; aiChat(\'👋 你好，我是你的 AI 黄金交易员。我已学习黄金期货的<b>斐波那契</b>、<b>江恩</b>画线法与<b>风险管理</b>体系，能实时读盘、画线、给建议并帮你控风险。点上方周期，或直接在下面对我下指令（说「帮助」看全部指令）。\',\'ai\'); }\n'
'    if(!AI_STATE.data) runAiAnalyze(AI_STATE.tf);\n'
'    if(AI_LIVE_TIMER) clearInterval(AI_LIVE_TIMER);\n'
'    AI_LIVE_TIMER=setInterval(aiLiveTick,15000);\n'
'  } else {\n'
'    p.classList.remove("open");\n'
'    if(AI_LIVE_TIMER){ clearInterval(AI_LIVE_TIMER); AI_LIVE_TIMER=null; }\n'
'  }\n'
'}\n'
)
reps.append((old3, new3))

# ---------- 4) AI_STATE 增加字段 ----------
old4 = 'var AI_STATE={tf:"day",data:null,open:false,levels:null,trend:null,bt:null,candles:null};'
new4 = 'var AI_STATE={tf:"day",data:null,open:false,levels:null,trend:null,bt:null,candles:null,everOpen:false,signalHostId:null};'
reps.append((old4, new4))

# ---------- 5) renderAi 末尾改为追加聊天 ----------
old5 = (
"  html+='<div class=\"aiT-bar\">'\n"
"    +'<button onclick=\"projectAiToChart()\">🎯 投射到走势图</button>'\n"
"    +'<button class=\"ghost\" onclick=\"runAiAnalyze(\\''+tf+'\\',true)\">🔄 重新拉取K线</button>'\n"
"    +'<button class=\"ghost\" onclick=\"aiTraderDeep()\">🧠 大模型解读</button>'\n"
"    +'</div>';\n"
"  out.innerHTML=html;\n"
"}\n"
)
new5 = (
"  html+='<div class=\"aiT-bar\">'\n"
"    +'<button onclick=\"projectAiToChart()\">🎯 投射到走势图</button>'\n"
"    +'<button class=\"ghost\" onclick=\"runAiAnalyze(\\''+tf+'\\',true)\">🔄 重新拉取K线</button>'\n"
"    +'<button class=\"ghost\" onclick=\"aiTraderDeep()\">🧠 大模型解读</button>'\n"
"    +'</div>';\n"
"  var _mid=aiChat(html,'ai'); if(_mid){ AI_STATE.signalHostId=_mid; }\n"
"}\n"
)
reps.append((old5, new5))

# ---------- 6) renderAiFallback 早返回 + 末尾 ----------
old6a = '  if(!d){ out.innerHTML=\'<div class="warn">计算失败，请确认实时价已获取后重试。</div>\'; return; }'
new6a = '  if(!d){ aiChat(\'<div class="warn">计算失败，请确认实时价已获取后重试。</div>\',\'ai\'); return; }'
reps.append((old6a, new6a))
old6b = (
"  html+='<div class=\"aiT-bar\"><button onclick=\"projectAiToChart()\">🎯 投射到走势图</button>'\n"
"    +'<button class=\"ghost\" onclick=\"runAiAnalyze(\\''+tf+'\\',true)\">🔄 重新拉取K线</button></div>';\n"
"  out.innerHTML=html;\n"
"}\n"
)
new6b = (
"  html+='<div class=\"aiT-bar\"><button onclick=\"projectAiToChart()\">🎯 投射到走势图</button>'\n"
"    +'<button class=\"ghost\" onclick=\"runAiAnalyze(\\''+tf+'\\',true)\">🔄 重新拉取K线</button></div>';\n"
"  var _mid=aiChat(html,'ai'); if(_mid){ AI_STATE.signalHostId=_mid; }\n"
"}\n"
)
reps.append((old6b, new6b))

# ---------- 7) runAiAnalyze 加载提示改为聊天 ----------
old7 = "  if(!force) out.innerHTML='<div class=\"warn\">🔄 正在拉取 '+tfName(tf)+' 真实历史K线并回测…（免费接口，约 1-3 秒）</div>';"
new7 = "  if(!force) aiChat('<div class=\"warn\">🔄 正在拉取 '+tfName(tf)+' 真实历史K线并回测…（免费接口，约 1-3 秒）</div>','ai');"
reps.append((old7, new7))

# ---------- 8) aiLiveTick 改为按 host 更新 ----------
old8 = (
'function aiLiveTick(){\n'
'  if(!AI_STATE.open || !AI_STATE.levels) return;\n'
'  var el=document.getElementById("aiTSignal");\n'
'  if(el) el.innerHTML=aiSignalHtml(MT5.lastPrice, AI_STATE.levels, AI_STATE.trend);\n'
'}\n'
)
new8 = (
'function aiLiveTick(){\n'
'  if(!AI_STATE.open || !AI_STATE.levels) return;\n'
'  var host=AI_STATE.signalHostId&&document.getElementById(AI_STATE.signalHostId);\n'
'  if(!host) return;\n'
'  var el=host.querySelector(".aiT-sig");\n'
'  if(el) el.outerHTML=aiSignalHtml(MT5.lastPrice, AI_STATE.levels, AI_STATE.trend);\n'
'}\n'
)
reps.append((old8, new8))

# ---------- 9) aiTraderDeep 的 out 改为聊天 setter ----------
old9 = (
'function aiTraderDeep(){\n'
'  var out=document.getElementById("aiTOut");\n'
'  if(!STATE.aiKey||!STATE.aiBase){\n'
)
new9 = (
'function aiTraderDeep(){\n'
'  var out={ set innerHTML(v){ aiChat(v,\'ai\'); } };\n'
'  if(!STATE.aiKey||!STATE.aiBase){\n'
)
reps.append((old9, new9))

# ---------- 10) renderDrawings 增加斐波/江恩图层 ----------
old10 = (
'  // 1) AI 投射线（底层，最多 5 条，避免画面乱）\n'
'  if(AI_PROJECTION){\n'
'    var data=AI_PROJECTION;\n'
'    data.lines.forEach(function(L){\n'
'      var y=priceToY(L.p, H);\n'
'      html+=\'<line class="mt5-ol-line" x1="0" y1="\'+y+\'" x2="\'+W+\'" y2="\'+y+\'" stroke="\'+L.col+\'" stroke-width="\'+L.width+\'" stroke-dasharray="\'+L.dash+\'"/>\';\n'
'      html+=\'<text class="mt5-ol-text" x="6" y="\'+(y-5)+\'" fill="\'+L.col+\'" font-weight="bold">\'+L.label+\' \'+fmtPrice(L.p)+\'</text>\';\n'
'    });\n'
'  }\n'
)
new10 = (
'  // 1) AI 投射线（底层）\n'
'  if(AI_PROJECTION){\n'
'    var data=AI_PROJECTION;\n'
'    data.lines.forEach(function(L){\n'
'      var y=priceToY(L.p, H);\n'
'      html+=\'<line class="mt5-ol-line" x1="0" y1="\'+y+\'" x2="\'+W+\'" y2="\'+y+\'" stroke="\'+L.col+\'" stroke-width="\'+L.width+\'" stroke-dasharray="\'+L.dash+\'"/>\';\n'
'      html+=\'<text class="mt5-ol-text" x="6" y="\'+(y-5)+\'" fill="\'+L.col+\'" font-weight="bold">\'+L.label+\' \'+fmtPrice(L.p)+\'</text>\';\n'
'    });\n'
'  }\n'
'  // 1.5) AI 斐波那契线（紫色，区间摆动高低点）\n'
'  if(AI_FIB){\n'
'    var fmin=AI_FIB.min, fmax=AI_FIB.max;\n'
'    AI_FIB.lines.forEach(function(L){\n'
'      var y=H-((L.p-fmin)/(fmax-fmin))*H;\n'
'      if(y<0||y>H) return;\n'
'      html+=\'<line class="aiT-ol-fib" x1="0" y1="\'+y+\'" x2="\'+W+\'" y2="\'+y+\'"/>\';\n'
'      html+=\'<text class="mt5-ol-text" x="6" y="\'+(y-4)+\'" fill="#9b7bff" font-weight="bold">Fib \'+(L.r*100).toFixed(1)+\'% \'+fmtPrice(L.p)+\'</text>\';\n'
'    });\n'
'    html+=\'<text class="mt5-ol-text" x="\'+(W-150)+\'" y="14" fill="#9b7bff" font-size="11">📐 斐波那契(示意)</text>\';\n'
'  }\n'
'  // 1.6) AI 江恩扇形（青色，枢轴点按标准角度）\n'
'  if(AI_GANN){\n'
'    var gmin=AI_GANN.min, gmax=AI_GANN.max;\n'
'    var gpx=W*AI_GANN.px, gpy=H-((AI_GANN.pivotPrice-gmin)/(gmax-gmin))*H;\n'
'    AI_GANN.angles.forEach(function(a){\n'
'      var rad=a*Math.PI/180, dx=W, dy=dx*Math.tan(rad);\n'
'      html+=\'<line class="aiT-ol-gann" x1="\'+gpx+\'" y1="\'+gpy+\'" x2="\'+(gpx+dx)+\'" y2="\'+(gpy+dy)+\'"/>\';\n'
'      html+=\'<line class="aiT-ol-gann" x1="\'+gpx+\'" y1="\'+gpy+\'" x2="\'+(gpx-dx)+\'" y2="\'+(gpy+dy)+\'"/>\';\n'
'      html+=\'<line class="aiT-ol-gann" x1="\'+gpx+\'" y1="\'+gpy+\'" x2="\'+(gpx+dx)+\'" y2="\'+(gpy-dy)+\'"/>\';\n'
'      html+=\'<line class="aiT-ol-gann" x1="\'+gpx+\'" y1="\'+gpy+\'" x2="\'+(gpx-dx)+\'" y2="\'+(gpy-dy)+\'"/>\';\n'
'    });\n'
'    html+=\'<circle cx="\'+gpx+\'" cy="\'+gpy+\'" r="3" fill="#5fd0c8"/>\';\n'
'    html+=\'<text class="mt5-ol-text" x="6" y="\'+(gpy-6)+\'" fill="#5fd0c8" font-size="11">江恩枢轴 \'+fmtPrice(AI_GANN.pivotPrice)+\'</text>\';\n'
'  }\n'
)
reps.append((old10, new10))

# ---------- 11) clearDrawings 也清 AI 画线 ----------
old11 = "function clearDrawings(){ DRAW.items=[]; DRAW.current=null; AI_PROJECTION=null; AI_PROJ_RANGE=null; renderDrawings(); var ptr=document.querySelector('#mt5Dtools .dt-btn[data-tool=\"pointer\"]'); if(ptr) selectDrawTool('pointer',ptr); }"
new11 = "function clearDrawings(){ DRAW.items=[]; DRAW.current=null; AI_PROJECTION=null; AI_PROJ_RANGE=null; AI_FIB=null; AI_GANN=null; renderDrawings(); var ptr=document.querySelector('#mt5Dtools .dt-btn[data-tool=\"pointer\"]'); if(ptr) selectDrawTool('pointer',ptr); }"
reps.append((old11, new11))

# ---------- 12) 插入新功能块（新闻雷达之前） ----------
anchor12 = "/* ===== 新闻雷达 · 智能语义引擎 v2 ===== */"
js_block = (
'\n'
'/* ===== AI 交易员 · 对话指令 / 画线 / 风险管理 / 知识库 ===== */\n'
'var AI_FIB=null, AI_GANN=null;\n'
'/* 内置黄金期货知识库（整理自公开资料：斐波那契、江恩、风险管理） */\n'
'var GOLD_KB={\n'
'  fib:\'<div class="blk"><h4>📐 斐波那契回调（Fibonacci Retracement）</h4>\'\n'
'    +\'<p class="aiT-plan">原理：趋势回撤常在 <b>23.6% / 38.2% / 50% / 61.8% / 78.6%</b> 这几条黄金比例位获得支撑或受阻。做法：取一段行情的<b>摆动低点→摆动高点</b>拉出区间，价格回踩到这些比例位且出现反转K线（锤子线、看涨吞噬）时，视为顺势入场点。</p>\'\n'
'    +\'<p class="aiT-plan">用法：① 上涨趋势中，从低点到高点画；② 价格回踩 38.2%~61.8% 不破，配合确认K线做多；③ 跌破 61.8% 则原趋势大概率失效。我已把当前周期区间的斐波那契线画到走势图上（紫色），可直接对照。</p></div>\',\n'
'  gann:\'<div class="blk"><h4>📏 江恩理论（Gann）</h4>\'\n'
'    +\'<p class="aiT-plan">核心：<b>时间=价格</b>。江恩认为当价格与时间达成平方（1×1 即 45° 线）时市场最平衡。关键角度：1×1(45°)、2×1(63.4°)、1×2(26.6°)、3×1、1×3、4×1、1×4 等，从重要顶部/底部（枢轴点）向外发散成「江恩扇形」。</p>\'\n'
'    +\'<p class="aiT-plan">用法：枢轴点上方扇形线为阻力、下方为支撑；价格沿 1×1 线运行代表趋势健康，跌破 1×1 转弱、跌破 1×2 则趋势可能反转。我已从区间高点作枢轴，画出标准角度扇形（青色，示意）供你学习对照。</p></div>\',\n'
'  risk:\'<div class="blk"><h4>🛡️ 风险管理要点</h4>\'\n'
'    +\'<p class="aiT-plan">① <b>单笔风险 ≤ 本金 1%~2%</b>：你 400U、风险 1.5% → 单笔最多亏 6U。② <b>先定止损再定仓位</b>：仓位 = 单笔风险 ÷（每手每点价值 × 止损距离）。XAUUSD 0.01 手每波动 1 美元 = 风险 1 美元。③ <b>止损放技术位外</b>：做多放支撑下方、做空放阻力上方，不扛单。④ <b>盈亏比 ≥ 2:1</b> 才出手。⑤ 总敞口同时不超过 2~3 笔。</p></div>\',\n'
'  general:\'<div class="blk"><h4>📚 黄金交易核心驱动</h4>\'\n'
'    +\'<p class="aiT-plan">黄金由 <b>美元</b>（美元弱→金强）、<b>实际利率</b>（利率降/通胀升→金强）、<b>避险情绪</b>（地缘、危机→金强）、<b>ETF与央行购金</b>流向共同驱动。看盘重点：美盘时段（北京时间 20:30 后）波动最大；关注美国 CPI、非农、美联储讲话。技术面配合支撑阻力与斐波/江恩，胜率更高。</p></div>\'\n'
'};\n'
'function aiChat(html, who){\n'
'  var box=document.getElementById("aiTChat"); if(!box) return null;\n'
'  var mid="aiMsg_"+Date.now()+"_"+Math.floor(Math.random()*1000);\n'
'  var div=document.createElement("div");\n'
'  div.className="aiT-msg "+(who==="me"?"me":"ai");\n'
'  div.id=mid;\n'
'  div.innerHTML=\'<div class="who">\'+(who==="me"?"你":"🤖 AI 交易员")+\'</div>\'+html;\n'
'  box.appendChild(div);\n'
'  box.scrollTop=box.scrollHeight;\n'
'  return mid;\n'
'}\n'
'function aiQuick(t){ var i=document.getElementById("aiTCmd"); if(i) i.value=t; aiChat(escHtml(t),"me"); aiCommand(t); }\n'
'function aiSendCmd(){\n'
'  var i=document.getElementById("aiTCmd"); if(!i) return;\n'
'  var v=i.value.trim(); if(!v) return; i.value="";\n'
'  aiChat(escHtml(v),"me"); aiCommand(v);\n'
'}\n'
'function aiKb(topic){ aiChat(GOLD_KB[topic]||GOLD_KB.general,"ai"); }\n'
'function aiHelp(){\n'
'  aiChat(\'<div class="blk"><h4>💬 我可以帮你做这些（直接打字下指令）</h4>\'\n'
'    +\'<p class="aiT-plan">· 画斐波那契线 / 画江恩线 —— 我在走势图上画线</p>\'\n'
'    +\'<p class="aiT-plan">· 分析当前走势 / 全盘研判 —— 拉真实K线给支撑阻力+趋势+回测</p>\'\n'
'    +\'<p class="aiT-plan">· 给我交易建议 —— 给入场/止损/目标计划</p>\'\n'
'    +\'<p class="aiT-plan">· 怎么做风险管理 / 设止损 / 控仓 —— 算止损位与仓位</p>\'\n'
'    +\'<p class="aiT-plan">· 把关键位投射到走势图 —— 标支撑阻力</p>\'\n'
'    +\'<p class="aiT-plan">· 斐波那契怎么用 / 江恩怎么用 / 黄金知识 —— 讲原理</p>\'\n'
'    +\'<p class="aiT-plan">· 清除AI画线 / 帮助</p></div>\',\'ai\');\n'
'}\n'
'function aiPlanToChat(){\n'
'  var price=MT5.lastPrice, lv=AI_STATE.levels, tr=AI_STATE.trend;\n'
'  if(!lv){ aiChat(\'<div class="warn">请先点上方周期运行分析，或说「分析当前走势」。</div>\',\'ai\'); return; }\n'
'  var riskAmt=(STATE.equity||400)*((STATE.riskPct||1.5)/100);\n'
'  aiChat(aiPlanHtml(AI_STATE.tf, price, lv, tr, riskAmt),\'ai\');\n'
'}\n'
'function aiGiveAdvice(){\n'
'  if(!AI_STATE.levels){ aiChat(\'<div class="warn">先拉取K线并回测，稍等…</div>\',\'ai\'); runAiAnalyze(AI_STATE.tf); }\n'
'  else { aiPlanToChat(); aiRiskPlan(); }\n'
'}\n'
'function aiDrawFib(){\n'
'  var lv=AI_STATE.levels, price=MT5.lastPrice;\n'
'  if(!lv||price==null){ aiChat(\'<div class="warn">请先点上方周期运行分析（拉真实K线），我再画斐波那契。</div>\',\'ai\'); return; }\n'
'  var lo=lv.L, hi=lv.H;\n'
'  if(!(hi>lo)){ var d=buildTfData(AI_STATE.tf); if(d){ lo=d.lo; hi=d.hi; } }\n'
'  if(!(hi>lo)){ aiChat(\'<div class="warn">区间不足，无法画斐波那契。</div>\',\'ai\'); return; }\n'
'  var lines=fibLevels(lo,hi);\n'
'  AI_FIB={min:lo*0.999, max:hi*1.001, lines:lines};\n'
'  renderDrawings();\n'
'  var txt=\'<div class="blk"><h4>📐 斐波那契线已画到走势图（区间 \'+fmtPrice(lo)+\' ~ \'+fmtPrice(hi)+\'）</h4>\';\n'
'  lines.forEach(function(L){ txt+=\'<div class="row"><span>Fib \'+(L.r*100).toFixed(1)+\'%</span><b style="color:#9b7bff">\'+fmtPrice(L.p)+\'</b></div>\'; });\n'
'  txt+=\'<div class="warn">回踩 38.2%~61.8% 不破且出现反转K线，可顺势做多；跌破 61.8% 原趋势大概率失效。说「斐波那契怎么用」看原理。</div></div>\';\n'
'  aiChat(txt,"ai");\n'
'}\n'
'function aiDrawGann(){\n'
'  var lv=AI_STATE.levels, price=MT5.lastPrice;\n'
'  if(!lv||price==null){ aiChat(\'<div class="warn">请先点上方周期运行分析，我再画江恩线。</div>\',\'ai\'); return; }\n'
'  var lo=lv.L, hi=lv.H;\n'
'  if(!(hi>lo)){ var d=buildTfData(AI_STATE.tf); if(d){ lo=d.lo; hi=d.hi; } }\n'
'  if(!(hi>lo)){ aiChat(\'<div class="warn">区间不足，无法画江恩线。</div>\',\'ai\'); return; }\n'
'  AI_GANN={min:lo*0.999, max:hi*1.001, pivotPrice:hi, px:0.62, angles:[75,71.6,63.4,45,26.6,18.4,14]};\n'
'  renderDrawings();\n'
'  aiChat(\'<div class="blk"><h4>📏 江恩扇形已画到走势图（枢轴=\'+fmtPrice(hi)+\'）</h4>\'\n'
'    +\'<p class="aiT-plan">从区间高点作枢轴，按标准角度（1×1=45°、2×1、1×2、3×1、1×3、4×1）发散。价格沿 1×1 线运行趋势健康；跌破 1×1 转弱、跌破 1×2 警惕反转。说「江恩怎么用」看原理。</p>\'\n'
'    +\'<div class="warn">江恩扇形为示意角度，精确比例需按真实时间刻度；用于学习形态，开仓仍以支撑阻力+确认K线为主。</div></div>\',\'ai\');\n'
'}\n'
'function aiRiskPlan(){\n'
'  var price=MT5.lastPrice;\n'
'  if(price==null){ aiChat(\'<div class="warn">实时价还没取到，请稍等几秒。</div>\',\'ai\'); return; }\n'
'  var eq=(STATE.equity||400), rp=(STATE.riskPct||1.5)/100;\n'
'  var riskAmt=eq*rp;\n'
'  var html=\'<div class="blk"><h4>🛡️ 风险管理方案（本金 \'+eq+\'U · 单笔风险 \'+(rp*100).toFixed(1)+\'%）</h4>\';\n'
'  html+=\'<p class="aiT-plan">单笔最大可亏损：<b>\'+riskAmt.toFixed(2)+\'U</b>。先想亏多少，再决定仓位——这是活下来的关键。</p>\';\n'
'  var lv=AI_STATE.levels;\n'
'  if(lv){\n'
'    var S=lv.sup||lv.S1, R=lv.res||lv.R1;\n'
'    var slLong=S-Math.max(1.5,(price-S)*0.25), distLong=price-slLong;\n'
'    var slShort=R+Math.max(1.5,(R-price)*0.25), distShort=slShort-price;\n'
'    function lotInfo(dist){\n'
'      var real=Math.max(0.01, Math.round((riskAmt/(100*dist))/0.01)*0.01);\n'
'      var realRisk=0.01*100*dist;\n'
'      var ok=realRisk<=riskAmt*1.08;\n'
'      return \'建议仓位 <b>\'+real.toFixed(2)+\' 手</b>（最低 0.01）；0.01 手在此止损距离下实际风险 <b>\'+realRisk.toFixed(2)+\'U</b> \'+(ok?\':) 在预算内\':\':( 超预算，建议放弃或等更近入场\');\n'
'    }\n'
'    html+=\'<div class="row"><span>做多止损位</span><b class="sup">\'+fmtPrice(slLong)+\'</b></div>\';\n'
'    html+=\'<p class="aiT-plan">\'+lotInfo(distLong)+\'</p>\';\n'
'    html+=\'<div class="row"><span>做空止损位</span><b class="res">\'+fmtPrice(slShort)+\'</b></div>\';\n'
'    html+=\'<p class="aiT-plan">\'+lotInfo(distShort)+\'</p>\';\n'
'    html+=\'<p class="aiT-plan">目标：做多看 \'+fmtPrice(R)+\'（距 \'+(R-price).toFixed(2)+\'）、做空看 \'+fmtPrice(S)+\'（距 \'+(price-S).toFixed(2)+\'）。开仓前确认盈亏比 ≥ 2:1。</p>\';\n'
'  } else {\n'
'    html+=\'<p class="aiT-plan">先运行分析，我才能结合支撑/阻力算具体止损与仓位。通用：止损距离 = 单笔风险 ÷（100 × 手数）；0.01 手每波动 1 美元 = 风险 1 美元。</p>\';\n'
'  }\n'
'  html+=\'<div class="warn">纪律：① 单笔风险 ≤1%~2%；② 止损必设技术位外、不扛单；③ 盈亏比 ≥2:1 才出手；④ 同时敞口 ≤2~3 笔。黄金波动大，务必轻仓。</div></div>\';\n'
'  aiChat(html,\'ai\');\n'
'}\n'
'function clearAiDrawings(){\n'
'  AI_FIB=null; AI_GANN=null; AI_PROJECTION=null; AI_PROJ_RANGE=null;\n'
'  renderDrawings();\n'
'  aiChat(\'<div class="warn">🧹 已清除 AI 画的分析线（支撑/阻力、斐波那契、江恩）。你的手绘线保留。</div>\',\'ai\');\n'
'}\n'
'function aiCommand(text){\n'
'  var t=(text||"").toLowerCase();\n'
'  function has(){ for(var i=0;i<arguments.length;i++) if(t.indexOf(arguments[i])>=0) return true; return false; }\n'
'  var know=has(\'怎么用\',\'原理\',\'知识\',\'教程\',\'是什么\',\'如何\',\'学习\');\n'
'  if(know && has(\'斐波\',\'fib\')){ aiKb(\'fib\'); return; }\n'
'  if(know && has(\'江恩\',\'gann\')){ aiKb(\'gann\'); return; }\n'
'  if(know && has(\'风险\',\'仓位\',\'控仓\',\'止损\',\'风控\')){ aiKb(\'risk\'); return; }\n'
'  if(has(\'风险\',\'止损\',\'仓位\',\'控仓\',\'风控\')){ aiRiskPlan(); return; }\n'
'  if(has(\'斐波\',\'fib\')){ aiDrawFib(); return; }\n'
'  if(has(\'江恩\',\'gann\')){ aiDrawGann(); return; }\n'
'  if(has(\'投射\',\'标到图\',\'关键位\',\'投影\')){ projectAiToChart(); return; }\n'
'  if(has(\'清\',\'删\',\'去\') && has(\'线\',\'画\')){ clearAiDrawings(); return; }\n'
'  if(has(\'分析\',\'走势\',\'盘面\',\'研判\',\'当前\',\'全盘\')){ aiChat(\'<div class="warn">🔄 正在拉取\'+tfName(AI_STATE.tf)+\'真实K线并回测…</div>\',\'ai\'); runAiAnalyze(AI_STATE.tf); return; }\n'
'  if(has(\'建议\',\'交易\',\'信号\',\'操作\',\'怎么玩\',\'买\',\'卖\')){ aiGiveAdvice(); return; }\n'
'  if(has(\'帮助\',\'help\',\'你能\',\'会做\',\'功能\')){ aiHelp(); return; }\n'
'  if(has(\'知识\',\'黄金\',\'怎么看\',\'入门\')){ aiKb(\'general\'); return; }\n'
'  aiChat(\'我还没完全理解这条指令。试试：<b>画斐波那契线</b> / <b>画江恩线</b> / <b>分析当前走势</b> / <b>给我交易建议</b> / <b>怎么做风险管理</b> / <b>把关键位投射到走势图</b> / <b>清除AI画线</b>。也可说「帮助」。\',\'ai\');\n'
'}\n'
'function initAiDrag(){\n'
'  var panel=document.getElementById("aiTPanel"), head=document.getElementById("aiTHead");\n'
'  if(!panel||!head||panel._dragReady) return; panel._dragReady=true;\n'
'  var sx=0,sy=0,ox=0,oy=0,drag=false;\n'
'  head.addEventListener("mousedown",function(e){\n'
'    if(e.target.tagName==="BUTTON"||e.target.classList.contains("x")) return;\n'
'    drag=true; sx=e.clientX; sy=e.clientY;\n'
'    var r=panel.getBoundingClientRect(); ox=r.left; oy=r.top;\n'
'    panel.style.left=ox+"px"; panel.style.top=oy+"px"; panel.style.right="auto";\n'
'    e.preventDefault();\n'
'  });\n'
'  window.addEventListener("mousemove",function(e){\n'
'    if(!drag) return;\n'
'    var nx=ox+(e.clientX-sx), ny=oy+(e.clientY-sy);\n'
'    nx=Math.max(0,Math.min(window.innerWidth-panel.offsetWidth,nx));\n'
'    ny=Math.max(0,Math.min(window.innerHeight-panel.offsetHeight,ny));\n'
'    panel.style.left=nx+"px"; panel.style.top=ny+"px";\n'
'  });\n'
'  window.addEventListener("mouseup",function(){ drag=false; });\n'
'}\n'
)
reps.append((anchor12, js_block + anchor12))

# ---------- 13) 页脚版本号 ----------
# 允许不存在（count 0 也 OK）
if "v2.8 · 更新于 2026-08-15" in s:
    reps.append(("v2.8 · 更新于 2026-08-15", "v2.9 · 更新于 2026-08-15"))

# ---------- 执行 ----------
failed = []
for i,(old,new) in enumerate(reps):
    c = s.count(old)
    if c != 1:
        failed.append((i, c))
if failed:
    print("FAILED replacements (index, count):")
    for i,c in failed:
        print("  ", i, c)
    sys.exit(1)

for old,new in reps:
    s = s.replace(old, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("OK: applied", len(reps), "replacements")
