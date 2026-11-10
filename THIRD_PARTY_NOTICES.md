# 来源与许可证

本插件派生自 Zhalslar 及原项目贡献者的 https://github.com/Zhalslar/astrbot_plugin_apis 。

- 上游版本：3.1.2。
- 用户提供的原始归档：`astrbot_plugin_apis-3.1.2-dedb3df60a93.zip`。
- 归档根目录所标识的提交：`dedb3df60a93ed23df45ac1849a49251e8d664c4`。这是归档中的标识，未与当前 GitHub 状态核验。
- 原始归档 SHA-256：`2e96d343b61e99ba2473509918d8d10e589d69d1fede3ac505a3e169d38691a6`。
- 上游包含 GNU AFFERO GENERAL PUBLIC LICENSE Version 3 全文。本移植版保留该 LICENSE，清单声明为 `AGPL-3.0-only`。

保留的上游内容包括：API 请求/解析与缓存核心、SQLite 存储、站点和 API 管理、默认 API/站点池、面板 HTML/CSS/JavaScript、图标及其原有署名。

MaiBot 移植维护者：sora-maru。2026-11-10 的迁移工作包括：独立 SDK 入口与配置、消息 Hook、权限与会话路由、媒体内容传输、页面通信网关、分块导入/预览、可取消的测试任务、自包含 HTML、测试和文档。另修复空选择误测试全部 API、关闭保存时误删缓存的风险，并收紧本地数据及导出路径边界。

1.0.2 增加站点批量健康测试和确认后的关联删除、站点地址迁移及事务保存，修复数据库内存引用和持久化、嵌入式页面及弹窗布局、测试取消清理，并统一文字响应与缓存显示的换行处理。

1.0.3 的接口及站点默认数据重新依据冷雨枫林、枫雨二代、糖豆子、问情、星之阁和倾梦的公开目录与参数文档整理；收录不代表拥有其业务数据或媒体版权。接口描述、来源链接、采集范围及排除原因列于 DEFAULT_DATA_SOURCES.md。本包不分发站点私密密钥及 Cookie，不对来源的运行情况和第三方媒体权利作保证。

仓库源码和本安装包中的可编辑前端资源是本版对应源码；`tools/build_webui.py` 可重建页面。分发与修改请遵守随附 AGPL v3，包括适用时向通过网络交互的用户提供修改版对应源码。

Python 第三方依赖通过运行环境安装，不在包内复制其源码：aiohttp、beautifulsoup4，以及 MaiBot Plugin SDK。默认 API 所返回的第三方文字和媒体不随本包分发，其来源和使用条件由各站点决定。
