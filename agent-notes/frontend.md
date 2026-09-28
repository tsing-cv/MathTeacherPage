# 前端架构方案 — 数学老师微信招生单页

适用背景：独立高中数学老师招生宣传单页，单文件 HTML（内联 CSS/JS），微信扫码/分享为主场景，设计基准 iPad 4:3（1024×768），同时适配手机（375-430px）无横向滚动，目标首屏渲染 <1.5s，微信 iOS/Android 表现一致。

## 零外链决策论证（向用户说明用）

1. Tailwind CDN / unpkg 在大陆多走海外回源，微信内首字节常超 2s，直接击穿 1.5s 目标；零外链让单个 HTML 请求即完成渲染。
2. Tailwind Play CDN 是 110KB 级阻塞式运行时 JS，Framer Motion 连带 React 超 100KB，二者收益在手写页面中可低成本替代。
3. 原生 CSS/rAF/IntersectionObserver 在 iOS WKWebView 与安卓 XWeb 表现一致，且不存在"CDN 加载失败→整页裸奔"的单点风险；系统字体栈零请求、无 FOIT 闪烁。

## 一、区块布局（1024px；375px 塌缩）

- **Hero**：左 6 右 4 两栏，左价值主张+CTA，右 canvas 函数曲线为视觉重心，数据信任条通栏四分压底；窄屏单列堆叠，数据条转 2×2。
- **导师介绍**：左照片 320px + 右资历，重心在照片；窄屏照片居中，资历单列。
- **教学体系**：三栏等宽思维卡片，下方考点频次条形图通栏（重心，数据即说服）；窄屏卡片单列，条形图仍通栏仅标签换行。
- **培养计划**：四步横向 stepper 通栏（重心在阶段递进）+ 直播卖点三栏；窄屏 stepper 转竖向左竖线，卖点单列。
- **教研证据/学员反馈**：三栏截图网格（重心在手写实物感）、三栏引述卡；窄屏均单列。
- **底部联系**：左二维码右微信号两栏，重心在二维码；窄屏居中单列，悬浮按钮与弹层通栏。

## 二、响应式断点策略

Mobile-first 默认单列；`min-width: 768px` 启用多栏（768 恰为 iPad 竖屏宽，覆盖平板以上）；辅以 `max-width: 480px` 微调字号与信任条 2×2。容器 `max-width: 960px` 居中防宽屏拉伸。两断点足够，避免维护碎片化。

## 三、零外链性能方案

- 导师照片 `eager` + `fetchpriority="high"`，其余图片 `loading="lazy"` + `decoding="async"` 并写死宽高防 CLS；
- 全部动画包在 `@media (prefers-reduced-motion: no-preference)` 内，reduce 时直出终态帧/终值；
- CSS 全量内联即天然首屏关键 CSS，JS 置 `</body>` 前；
- 体积预算：HTML（不含图）<100KB、首屏图 <150KB。

## 四、动画实现方案

- **Hero 函数曲线**：预采样约 200 点入数组，rAF 按 `elapsed/duration` 取进度并配 easeInOutCubic 缓动，每帧增量 `lineTo` 不清屏；播完 `cancelAnimationFrame` 并绘终点标记；标志位保证只播一次；canvas 尺寸乘 devicePixelRatio 防虚。
- **数字滚动计数器**：IntersectionObserver 进场触发，约 1.2s 内值 = 目标 × easeOut(t)，处理小数位与千分位，完成即 unobserve（只播一次）。
- **入场克制原则**：仅 Hero 曲线、数据计数、条形图宽度三处动画；导师、反馈、卖点等区块零入场动画，保滚动流畅；条形图用 CSS transition + IO 触发即可，无需逐帧 JS。

## 五、代码组织规范

- CSS 变量分区：`--c-`（色板）、`--fs-`（字号）、`--sp-`（间距档）、`--r-`（圆角），断点内只覆盖变量。
- HTML 注释分区：区块头 `<!-- ★【区块】Hero首屏 -->`，可改文案处行尾 `<!-- ★【修改】主标题 -->`，图片注释附建议尺寸；约定"搜索 ★【修改】 即得全部文案清单"。
- JS 首行 `const CONFIG = { wechatId, qrSrc, toastText }` 集中管理可变项（微信号、二维码路径、提示语）。

## 六、微信兼容注意点

- **复制微信号**：优先 execCommand（隐藏 textarea + select + copy），必须在点击手势同步调用栈内执行，navigator.clipboard 仅作增强；失败降级为引导长按选择弹层中的明文微信号。
- **底部弹层安全区**：meta 加 `viewport-fit=cover`，弹层 `padding-bottom: calc(env(safe-area-inset-bottom) + 16px)`；打开时锁 body 滚动并加 `overscroll-behavior: contain` 防滚动穿透。
- **二维码长按识别**：必须 `<img>` 位图（jpg/png），禁 background-image 与 inline SVG，且不加 lazy。

## 七、踩坑清单

1. SVG/背景图二维码长按无"识别图中二维码"菜单（iOS 微信仅认 img 位图）。
2. meta 缺 `viewport-fit=cover` 时 safe-area 恒为 0，弹层被 Home 条遮挡。
3. execCommand 放进 Promise/setTimeout 回调会静默失败，必须同步调用。
4. canvas 不乘 devicePixelRatio 高分屏发虚；rAF 动画须用时间戳驱动，防微信切后台冻结帧计数。
5. `100vw` 引发横向滚动（小数像素/滚动条），一律 `width: 100%` + `border-box`，长标签加 `word-break`。
