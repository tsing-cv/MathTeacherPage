# 第九轮 · 配色设计大师评审报告（2026-09-24）

对象：index.html（行号指当前版本）。六大 agent 之一，主诉：布局之外的一切色彩问题。

## ① 现状诊断（按严重度）

### S1 对比度失败（WCAG 实测）
- gold-deep #8C6F3A / paper #F4F7FA = 4.39:1 → AA 正文不通过；/ paper2 = 4.12:1 不通过；/ white = 4.72 勉强过
- gd #8FA0BC / navy = 6.05 过；/ card = 4.92 过（余量薄）
- gd opacity:.6 / navy = 3.05 失败（copyright、chat-time）；opacity:.75 / navy = 4.01 失败（.trust 合规小字）；opacity:.8 / navy = 4.39 失败（.voice-fine）；opacity:.6 / card = 2.72 失败
- 实质：gold-deep 注释写「仅≥18px或加粗」但实际大量用于 12px 眉题、12.5px 长句（.eyebrow L184、.step-stage L385、.gate-how L688 整句操作化说明、.tl-time L666、.cycle i L674）。最刺眼：合规免责声明是全页对比度最低的文字
- 附带：:focus-visible 金描边浅底仅 2.09:1（<3:1 焦点要求）

### S2 金色职能过载
- 面积占比：深蓝 40–42%、纸白 58–60%（paper≈34% + paper2≈25%）、金 <1% 却 60+ 触点、6 类职能：认证品牌/结构线/强调文字/交互可供性/装饰底纹/数据图形
- 首屏 8 个金色注意点同屏（motto+4 stat+2 按钮+曲线+网格），没有元素在退后
- gold-hi 被当深底通用 b 标签色（duo-turn、demo lead、freq-aside、deriv 年份、act 序号），强调排他性稀释
- 浅底：重点色与元信息色同色（step-stage/tl-time/cycle i/gate-no/subsec 编号/pins/价格/FAQ 展开态全 gold-deep），价格只能靠字号硬撑

### S3 受众心理
- 深蓝对三线城市家长是优解（公办/教科书/学位袍心智，回应「怕被割」）；金隐喻本身对（印章/装订线/奖状边）
- 但 #C9A961 偏亮偏饱和且密度极高 → 滑向「高端理财/精品课程包装」，恰是这类家长最警惕的信号
- 结论：不动色相，(a)金降半档明度/彩度 (b)金收缩回「结构与认证」 (c)可选：浅底冷纸→暖纸 2–3 个点（课本/试卷心智）

### S4 深浅节奏
- 40/60 暗亮配比健康、暗-亮-暗大循环清晰
- 瑕疵1：三连深底隧道 system(网格)→demo(纯navy)→lead-magnet ≈连续 3000px 暗区（全页 20%）；暗底对暗底 rule-gold 不可见；demo 段无网格无 bigsym 是全页最平一段
- 瑕疵2：paper/paper2 明度差仅 1.07:1（ΔL*≈2.5）感知不到切换；「交替疲劳」真实来源是 plan 区 2200px 连续浅底
- 深底层次 navy→card(1.23:1)→snow 填充(.05–.08)→网格 梯子成立，但 card 与 navy 面差低于感知阈限，全靠金描边撑边界——金色被迫过载的结构性原因
- demo-card--bad 用 snow 填充 vs good 用 card+金边是聪明用法，保留

### S5 功能色缺位
- Toast 成败同皮肤（toastOk/toastFail 同 navy+金边）→ 失败态被渲染成成功态
- 照片红笔是页内唯一暖高饱和色，冷 navy+金环境中外来感明显；UI 缺一个与照片红笔同族的克制暖色呼应
- 聊天卡微信蓝 rgba(29,92,173,…) 拟真需要可接受

## ② 主推方案「冷纸·黄铜」（改动最小收益最大）
原则：navy/card/snow/ink/gd/gl 六色不动，只做三件事：修对比度、降金明度、补一个功能色。

变量级（:root L84–95）：
- --c-gold: #C9A961 → **#C2A05F**（明度-3 彩度-8，色相不动；按钮对比 6.48:1）
- --c-gold-deep: #8C6F3A → **#7A5E2F**（paper 上 5.63 / paper2 上 5.28 / white 上 6.05 全过 AA，12px 眉题合法化）
- --c-gold-hi 不变（9.84:1）
- 新增 --c-gd-dim: **#8296B4**（gd 合规降档色；navy 上 5.32:1，替代所有 opacity 层级）
- 新增 --c-cinnabar: **#B5543B**（朱砂/砖红唯一功能色；paper 上 4.55 过 AA；与照片红笔同族）

硬编码替换：rgba(201,169,97, → rgba(194,160,95,（约 26 处）；rgba(140,111,58, → rgba(122,94,47,（约 12 处）；favicon/brand SVG 与 canvas 曲线色（JS L1721）同步 #C2A05F/#DCC38A；og-cover 重新导出。

规则级（6 处）：
1. 消灭 opacity 层级：L359/423/435/459/503/507/621/644/775 共 9 处 gd+opacity:.6~.85 小字改 var(--c-gd-dim) 删 opacity
2. 焦点可见性：L146 后补 `.sec--paper :focus-visible, .sec--paper2 :focus-visible { outline-color: var(--c-gold-deep); }`（2.09→5.63）
3. FAQ 展开态降金：L478 整标题 gold-deep 改 color:var(--c-ink)（状态变化不占品牌强调色）
4. 元信息降档：.cycle i(L674) 与 .subsec::before(L654) gold-deep → var(--c-gl)；.step-stage/.tl-time/.gate-no 保留 gold-deep（新值合规，构成浅底批注墨系统）
5. Toast 失败态：补 .toast--fail { border-color: rgba(181,84,59,.55); }，JS 失败分支加类；.fit-card--no li::before 的×(L719) 与 .demo-card--bad .who(L618) 改 var(--c-cinnabar)——全页朱砂≤4处、面积<0.1%
6. demo 段解平：demo section 加 grid-deep 类；删 L1084 暗底对暗底 rule-gold（rule-gold 纪律=仅深→浅交界）

预期：两组 AA 失败清零、金触感镀金→黄铜、失败态可辨识、首屏金色注意点 8→5。改动量：2 变量值+3 新变量+约 50 处机械替换+6 处规则微调。

## ③ 备选方案「宣纸·茶金」（书卷气方向）
- --c-paper: #F4F7FA → #F6F3EB（暖象牙纸）；.sec--paper2 L392 #EBF0F6 → #EFEAE0（建议升变量 --c-paper2）
- --c-gold → #BA9A5C（茶金）；--c-gold-hi → #D9BE82；--c-gold-deep → #7A5E2F（同主推）
- --c-gl: #5A6B85 → #5E6572（去蓝调中性灰，暖纸上 5.29；原蓝灰暖纸上显脏）
- 白卡 5 处（cycle/tier/pins/social/fit-yes）→ #FBFAF5；.qr-card 必须 keep 纯白（二维码识别依赖）
- rgba(201,169,97, → rgba(186,154,92,
- 暖纸已验证 gl 4.89、新 gold-deep 5.46 全合规。心理收益最大（课本/试卷心智），代价替换面广。**不建议两案折中——冷暖纸混用最易显脏，二选一**

## ④ 金色使用纪律清单
合法席位四类：
1. 结构与装订（rule-gold、卡片 1px 描边、letter 左金线、金角标、印章边框；透明度维持 .18–.45）
2. 数字与价格（stat、tier-price、vs-to、bar-val、pins——数据即金）
3. 主 CTA（btn--gold、fab；同屏实底金按钮 ≤1）
4. 正文关键短语（duo-turn b、demo lead b；同屏 ≤2 处）

降级为灰蓝/墨色的场景：栏目元信息（subsec 编号、cycle i、chat-time、freq-note、voice footer）；状态反馈（FAQ 开合态、toast 用墨蓝或朱砂）；否定/警示语义一律朱砂禁止用金；装饰底纹只铺深底透明度不得高于现值；任何同屏第 3 个金色实底块砍掉。

一句话纪律：**金=结构+数字+唯一CTA；文字强调每屏≤2；状态用墨蓝/朱砂；其余归灰蓝。**当前差距=60+ 触点中约 15 处需降级，主推方案已圈出。
