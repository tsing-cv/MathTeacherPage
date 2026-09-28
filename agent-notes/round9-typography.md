# 第九轮 · 排版设计大师评审报告（2026-09-24）

总评：衬线/无衬线分工成立不要动；Georgia 老式数字账本气质正确。系统病三处：间距手工拍出来非倍率体系（38/40/44/46/56 五档近似、卡片内边距七档）、桌面字号中部塌陷、两处硬性节奏破损。

## 12 条优化（影响力降序）

1. **【P0】lead-magnet 双重留白洞+底部 0px 贴金线**：L1153 内联 padding 叠 #demo 的 --sp-sec（上 208px/128px），下缘紧贴 rule-gold 间距 0。改：删内联 style 回 `<div class="wrap">`；.lead-magnet { margin: 0 0 56px; }
2. **【P0】组件间距无倍率体系且不随断点缩放**：五近似值 38/40/44/46/48–56；桌面区块留白翻倍组件不动；.subsec/.interlude 恒 84px 手机失衡；三 gap 脱队（shots 28、cycle 18、stats 18）。改：:root 增 --sp-block:40/--sp-block-lg:56/--sp-sub:56，≥768 改 56/72/88；映射全部组件；shots 28→20、cycle 对齐 16/20
3. **【P1】桌面字号中部塌陷**：梯度 54/32/20/17/13，h3→正文仅 1.18；.subsec 恒 22px 手机与 h2 仅差 2px。改：≥768 --fs-h3: 22px；.subsec 20px（手机让位 h2）/≥768 26px。改后桌面链 54/32/26/22/17 逐级 1.2–1.3
4. **【P1】卡片内边距七档并存**（14/18/20/22/24/26/30，轴向颠倒如 .demo-q 24 26）。改：三档 token --pad-chip:16 14/--pad-card:24 22/--pad-banner:30 26，≥768 放大 20 18/28 26/40 32；八类卡片一律 --pad-card
5. **【P1】768–1023 区间 .steps 四列过窄**：每列文本宽约 146px，15px 正文仅 9 字/行。改：768–1023 两列（column-gap 48/row-gap 40），≥1024 才四列
6. **【P1】装订线只铺一半**：现 4 处金线含 1 处同色交界（system→demo 无意义），而 mentor→system、plan→interlude、interlude→classes、evidence→voices、faq→footer 五处深浅变色无线。规矩：**凡深浅变色处必有 1px 金线，同色交界不设线**——补五删一
7. **【P2】.letter/.deriv 居中轴与标题组左轴打架**（金线装订左缘悬空约 100px）。改：margin 44px 0 0 / 40px 0 0 左对齐（.demo-q/.demo-video 居中保留——对称展柜语义不同）
8. **【P2】tabular-nums 在 Georgia 上空承诺**（系统 Georgia 无 OpenType 特性，静默失效渲染老式数字）。三缺陷：a)「3–5 人」底线锯齿→.stat--txt b 宋体；b) .tier-price「100–150 元/课时·90 分钟」≥768 折行→span display:block 栈式两行；c) .deriv li b ≤520 被切回 sans 跨断点换字形→删覆盖。数字规则：口号数字随标题宋体，数据数字 Georgia 老式
9. **【P2】衬线正文两规则打架**：.voice p 手机 17 桌面反缩 16、.letter p 反向。规则：信件 17/2.05，引语 16/1.9 两端统一。.deriv li span 13px 桌面提 14（证据权重）；.gate-how 12.5→13
10. **【P2】letter 文字墙+plan 巨区**：letter 375 下约 1200px 连续文字墙。改：真书信排版——text-indent:2em+margin:0 0 .35em 紧段距；.sign text-indent:0。plan 呼吸交 --sp-sub
11. **【P3】FAQ 右缘 4px 错位**（summary 34 vs p 30）+行高松。改：p padding 0 34px 22px 0；summary line-height 1.55；≥768 summary 18px
12. **【P3】字距十档散落**。收敛三档 --ls-h:.02/--ls-m:.06/--ls-l:.18，映射：h2/h3/subsec→h；中层标签→m；眉题层保持 .18

## 三档间距倍率表（4px 基准）

| Token | 375 | ≥768 | 用途 | 吸收现值 |
|---|---|---|---|---|
| --sp-1 | 4 | 4 | 基线补差 | — |
| --sp-2 | 8 | 8 | 列表行距 | 6、10 |
| --sp-3 | 12 | 12 | 标题组内部 | 14 |
| --sp-4 | 16 | 20 | 卡片网格 gap | 16→20、28、18 |
| --sp-5 | 24 | 32 | 卡片内子元素距 | 22/26/28/30 |
| --sp-6 | 40 | 56 | 标题组→组件 | 38/40/44/46 |
| --sp-7 | 56 | 72 | 大组件、subsec 上沿 | 48/56/84 |
| --sp-8 | 64 | 104 | 区块留白（现状） | — |

1024 与 768 共享（960 定宽后无需增长），唯一例外 .steps 四列从 1024 起。落地顺序：1→2+4→3+6→其余。
