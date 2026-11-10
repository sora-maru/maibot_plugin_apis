# 默认 API 数据来源与更新说明

采集日期：2026-11-10（北京时间）。插件：`github.sora-maru.apis` 1.0.4。

本次以各站公开目录及接口文档为依据，生成 **621 条配置、6 个站点**。其中 395 条默认启用，226 条因密钥、维护、异步流程或参数问题默认停用。

“网页可访问”和“文档已采集”不表示全部业务 API 已实测成功。本次请求了来源主页、公开目录与文档，没有批量执行账号登录、上传、消息发送等业务操作。

## 来源连通检查

| 原来源 | 本次结果 | 新默认数据处理 |
|---|---|---|
| [枫林旧站](https://api.yuafeng.cn) | HTTP 200，页面明确提示迁移到 v.yuafeng.cn | 用冷雨枫林新站替换旧站 |
| [枫林二代](https://api-v2.yuafeng.cn) | HTTP 200，可读公开目录及文档 | 保留，重新采集 60 条 |
| 稳定 API（api.xingchenfu.xyz） | HTTPS 握手失败，HTTP 返回空响应 | 从当前默认来源移除，不能据此断言永久关闭 |
| [倾梦旧域名](https://api.317ak.cn) | HTTP 200，canonical 指向 api.317ak.com；旧域公开目录来源校验失败 | 改用 [api.317ak.com](https://api.317ak.com) 的公开目录，159 条 |
| 桑帛云 / FAPI（api.lolimi.cn） | 当前执行环境 DNS 无法解析 | 从当前默认来源移除 |
| [糖豆子](https://api.tangdouz.com) | HTTP 200，200 个文档条目 | 收录 189 个同站 API，其余 11 个为外部门户/文件/群链接等 |
| Pear（api.pearktrue.cn） | 当前执行环境 DNS 无法解析 | 从当前默认来源移除 |
| [问情](https://free.wqwlkj.cn) | HTTP 200，135 个目录条目；3 份单独文档超时 | 135 条，超时文档从首页公开参数表补充 |
| 龙珠（sdkapi.hhlqilongzhu.cn） | HTTPS 证书过期；HTTP 虽返回 200，正文为 502 Bad Gateway | 从当前默认来源移除 |
| [星之阁](https://api.xingzhige.com) | HTTP 200，58 个目录条目；9 个文档只显示维护页 | 49 条带真实请求地址的接口 |
| [冷雨枫林](https://v.yuafeng.cn) | HTTP 200，29 个公开接口文档全部下载 | 全部 29 条；登录接口维护中，保留为停用配置 |

## 新默认数据分布

| 来源 | 配置数 | 默认启用 | 默认停用 |
|---|---:|---:|---:|
| 冷雨枫林 | 29 | 25 | 4 |
| 枫雨二代 | 60 | 26 | 34 |
| 糖豆子 | 189 | 177 | 12 |
| 问情 | 135 | 122 | 13 |
| 星之阁 | 49 | 45 | 4 |
| 倾梦 | 159 | 0 | 159 |

## 更新现有实例

1. 保留 MaiBot 的插件配置和数据目录，替换为 1.0.4 源码，重载插件，然后点击管理页的“重载页面”。
2. 停止测试，等待正在执行的 API 请求结束。
3. 打开 **站点池 → 右上角导入/导出下拉菜单 → 替换为最新内置默认数据**。
4. 阅读覆盖数量后点击 **备份并覆盖两个池**。它会先完整备份当前站点池/API 池，再用一个数据库事务替换两者。
5. 备份位于插件数据目录的 `pool_files/`，文件名为 `site_pool_backup_日期_标识.json` 和 `api_pool_backup_日期_标识.json`。完成信息显示实际路径。

替换会移除你自行添加或修改的接口，使用本版预设重新建立两个池。插件配置及本地缓存保留。同地址或同主机唯一匹配站点的已有密钥/请求头会合并保留；更换域名（例如倾梦 .cn → .com）的账号和密钥不能假定兼容，需要按新站说明重新填写。

仅替换插件文件不会覆盖已有数据库；普通 JSON 导入跳过同名项目，适合补充而不是完整更新。自动备份包含你原有的私密配置，请保存在自己的实例，不要公开分享。

如果暂时不升级插件，也可使用本目录两个 `*_latest_2026-11-10.json` 文件：先导出备份，清空旧 API 和站点，再先导入站点池、后导入 API 池。推荐使用新版替换按钮，以免手工顺序错误。

## 使用与转换规则

- 接口名称保留来源前缀，触发关键词不带来源名，均为 1–6 个字符；同类接口使用数字后缀区分。例如 `/翻译 你好 en`。完整关键词可通过 `/查看api` 或面板查看。
- 所有当前可映射的公开目录项均收录，但仅支持 GET 的单次调用；POST 专用、登录、异步任务等条目默认停用。停用不代表失效，可在完成配置后手动启用。
- 文档中的密钥、Cookie、token 示例不写入预设。站点级 key/apikey 使用空值，填写自己的凭据；非标准认证参数按对应文档单独设置。
- 必填业务参数留空，供聊天参数填充；格式开关采用文档中明确的 JSON、图片或音频模式；没有足够证据时保留文字结果，不猜测媒体路径。
- 冷雨枫林的 b站搜索/解析，地址栏与示例存在 blilibli/bilibili 拼写差异，按地址栏记录并默认停用，等待实测。
- 冷雨枫林的解析接口采用文档样例中的单视频路径；图集、音乐等不同分享类型需要单独配置，不代表已实现一个触发词发送全部分支。
- `params` 按输入顺序填写；含空格的长文本推荐使用引用消息补参数，避免被拆成多个参数。
- 收录文件小于插件 3 MiB 浏览器导入上限，并经过真实配置模型和本地数据库导入校验。

## 未收录条目

| 来源 | 名称 | 原因 |
|---|---|---|
| 糖豆子 | [离线版网页版日历](https://api.tangdouz.com/api/%E7%A6%BB%E7%BA%BF%E7%89%88%E7%BD%91%E9%A1%B5%E7%89%88%E6%97%A5%E5%8E%86.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [临时文件互传](https://api.tangdouz.com/api/%E4%B8%B4%E6%97%B6%E6%96%87%E4%BB%B6%E4%BA%92%E4%BC%A0.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [糖豆子QQ小程序](https://api.tangdouz.com/api/%E7%B3%96%E8%B1%86%E5%AD%90QQ%E5%B0%8F%E7%A8%8B%E5%BA%8F.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [可以成为你的恋人吗](https://api.tangdouz.com/api/%E5%8F%AF%E4%BB%A5%E6%88%90%E4%B8%BA%E4%BD%A0%E7%9A%84%E6%81%8B%E4%BA%BA%E5%90%97.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [文档系统](https://api.tangdouz.com/api/%E6%96%87%E6%A1%A3%E7%B3%BB%E7%BB%9F.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [QQ群机器人](https://api.tangdouz.com/api/QQ%E7%BE%A4%E6%9C%BA%E5%99%A8%E4%BA%BA.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [ciallo](https://api.tangdouz.com/api/ciallo.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [帮你百度](https://api.tangdouz.com/api/%E5%B8%AE%E4%BD%A0%E7%99%BE%E5%BA%A6.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [volumeshader_bm](https://api.tangdouz.com/api/volumeshader_bm.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [节气横屏图片](https://api.tangdouz.com/api/%E8%8A%82%E6%B0%94%E6%A8%AA%E5%B1%8F%E5%9B%BE%E7%89%87.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| 糖豆子 | [云端文档](https://api.tangdouz.com/api/%E4%BA%91%E7%AB%AF%E6%96%87%E6%A1%A3.html) | 文档指向外部文件、交流群或独立门户，未作为当前站点的可调用 API 内置 |
| xing | [酷狗音乐搜索 v](https://api.xingzhige.com/doc/47) | 文档显示维护页，未提供可识别请求地址 |
| xing | [冰淇淋](https://api.xingzhige.com/doc/42) | 文档显示维护页，未提供可识别请求地址 |
| xing | [QQ音乐点歌v](https://api.xingzhige.com/doc/41) | 文档显示维护页，未提供可识别请求地址 |
| xing | [检讨书生成器](https://api.xingzhige.com/doc/33) | 文档显示维护页，未提供可识别请求地址 |
| xing | [网易云音乐搜索](https://api.xingzhige.com/doc/30) | 文档显示维护页，未提供可识别请求地址 |
| xing | [b站短链生成与还原](https://api.xingzhige.com/doc/28) | 文档显示维护页，未提供可识别请求地址 |
| xing | [QQ音乐搜索](https://api.xingzhige.com/doc/27) | 文档显示维护页，未提供可识别请求地址 |
| xing | [二维码解析](https://api.xingzhige.com/doc/13) | 文档显示维护页，未提供可识别请求地址 |
| xing | [群成员信息](https://api.xingzhige.com/doc/7) | 文档显示维护页，未提供可识别请求地址 |

## 全部接口及配置注意事项

| 接口名称 / 文档 | 返回类型 | 默认状态 | 输入参数顺序 | 注意事项 |
|---|---|---|---|---|
| [冷雨枫林·b站搜索](https://v.yuafeng.cn/index.php?doc-blilibli.html) | text | 停用 | msg → b | 接口地址与调用示例拼写不一致，按接口地址栏收录，待实测确认 |
| [冷雨枫林·b站解析](https://v.yuafeng.cn/index.php?doc-blilibli_jx.html) | video | 停用 | url | 接口地址与调用示例拼写不一致，按接口地址栏收录，待实测确认 |
| [冷雨枫林·DNS多节点拨测](https://v.yuafeng.cn/index.php?doc-boce_dns_api.html) | text | 启用 | domain → node | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·HTTP多节点拨测](https://v.yuafeng.cn/index.php?doc-boce_http_api.html) | text | 启用 | domain → node | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·ping多节点拨测](https://v.yuafeng.cn/index.php?doc-boce_ping_api.html) | text | 启用 | domain → node | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·域名查询](https://v.yuafeng.cn/index.php?doc-domainquery.html) | text | 启用 | domain | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·豆包解析](https://v.yuafeng.cn/index.php?doc-doubao.html) | video | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·豆英解析](https://v.yuafeng.cn/index.php?doc-douyin.html) | video | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·GitHub加速](https://v.yuafeng.cn/index.php?doc-ghproxy.html) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·即梦解析](https://v.yuafeng.cn/index.php?doc-jimeng.html) | video | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·扣扣音乐登录2](https://v.yuafeng.cn/index.php?doc-login_music.html) | text | 停用 | select | 网站目录或文档标记为维护、停用或状态未知；涉及登录、上传或多步骤操作，需额外配置/流程 |
| [冷雨枫林·猫眼实时票房](https://v.yuafeng.cn/index.php?doc-maoyanbox.html) | text | 启用 | mod | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·MD5加密](https://v.yuafeng.cn/index.php?doc-md5encrypt.html) | text | 启用 | text → format | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·迷你世界查主页](https://v.yuafeng.cn/index.php?doc-mini.html) | text | 启用 | uin | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·迷你世界s7加解密](https://v.yuafeng.cn/index.php?doc-mini_s7.html) | text | 启用 | text → select | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·墨迹天气查询](https://v.yuafeng.cn/index.php?doc-mojiweather.html) | text | 启用 | city → n → type | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·QQ音乐用户收藏](https://v.yuafeng.cn/index.php?doc-qqmusicuser.html) | text | 停用 | uin → select | 参数 Cookie 涉及账号/凭据，请按站点文档单独配置；站点说明需要 QQ 音乐 Cookie 或站点预置 Cookie，默认停用 |
| [冷雨枫林·QQ头像获取](https://v.yuafeng.cn/index.php?doc-qqtx.html) | image | 启用 | qq → t | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·QQ域名安全检测](https://v.yuafeng.cn/index.php?doc-qqurlcheck.html) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·二维码生成](https://v.yuafeng.cn/index.php?doc-qrcode.html) | image | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·视频大全](https://v.yuafeng.cn/index.php?doc-spxl.html) | video | 启用 | type → urltype | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·SSL证书查询](https://v.yuafeng.cn/index.php?doc-sslquery.html) | text | 启用 | domain | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·表情包搜索](https://v.yuafeng.cn/index.php?doc-stickersSearch.html) | image | 启用 | msg → page → num | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·多语言翻译](https://v.yuafeng.cn/index.php?doc-translate.html) | text | 启用 | content → to | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·文字转语音](https://v.yuafeng.cn/index.php?doc-tts.html) | audio | 启用 | msg → format → rate → volume | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·台风数据](https://v.yuafeng.cn/index.php?doc-typhoon.html) | text | 启用 | action | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·视频号解析](https://v.yuafeng.cn/index.php?doc-wxjx.html) | video | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·闲鱼作图](https://v.yuafeng.cn/index.php?doc-xianyu_img.html) | image | 启用 | qq → type | 按公开文档生成，业务有效性待实例验证 |
| [冷雨枫林·有道翻译](https://v.yuafeng.cn/index.php?doc-youdao.html) | text | 启用 | msg → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·JSON格式化校验](https://api-v2.yuafeng.cn/api_details.php?id=81) | text | 启用 | json | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·时间戳日期互换](https://api-v2.yuafeng.cn/api_details.php?id=80) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·获取本站服务器数据](https://api-v2.yuafeng.cn/api_details.php?id=74) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·恶搞语音文字转语音tts](https://api-v2.yuafeng.cn/api_details.php?id=73) | text | 启用 | content | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·实时汇率查询](https://api-v2.yuafeng.cn/api_details.php?id=72) | text | 启用 | to → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·国内各地区油价查询](https://api-v2.yuafeng.cn/api_details.php?id=71) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·表情包合成](https://api-v2.yuafeng.cn/api_details.php?id=70) | text | 启用 | slug → format | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·多倒计时提示（图片版）](https://api-v2.yuafeng.cn/api_details.php?id=69) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·12306余票和票价查询](https://api-v2.yuafeng.cn/api_details.php?id=68) | text | 启用 | date → from → to | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·实时黄金多品牌价格](https://api-v2.yuafeng.cn/api_details.php?id=67) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·UC浏览器热搜榜单](https://api-v2.yuafeng.cn/api_details.php?id=66) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·企鹅开放平台功能集接口](https://api-v2.yuafeng.cn/api_details.php?id=65) | text | 启用 | mode → quin → quid → qticket | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·龙虾创建机器人](https://api-v2.yuafeng.cn/api_details.php?id=64) | text | 停用 | qticket_lite → quid | 涉及登录、上传或多步骤操作，需额外配置/流程 |
| [枫雨二代·获取开放平台ck](https://api-v2.yuafeng.cn/api_details.php?id=63) | text | 停用 | mode → qrcode | 涉及登录、上传或多步骤操作，需额外配置/流程 |
| [枫雨二代·龙虾开放平台机器人列表查询](https://api-v2.yuafeng.cn/api_details.php?id=62) | text | 启用 | qticket_lite → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·扣扣开放平台龙虾取ck](https://api-v2.yuafeng.cn/api_details.php?id=61) | text | 停用 | mode → session_id | 涉及登录、上传或多步骤操作，需额外配置/流程 |
| [枫雨二代·deepseek-v3.2(满血记忆版)](https://api-v2.yuafeng.cn/api_details.php?id=60) | text | 停用 | msg → id → type | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [枫雨二代·名字重名查](https://api-v2.yuafeng.cn/api_details.php?id=59) | text | 停用 | name | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·ip归属地经纬度查询（并发高性能）](https://api-v2.yuafeng.cn/api_details.php?id=58) | text | 启用 | ip → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·ip归属地查询（本地）](https://api-v2.yuafeng.cn/api_details.php?id=57) | text | 启用 | ip → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·灰色头像制作（作图）](https://api-v2.yuafeng.cn/api_details.php?id=56) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·头像像素画（作图）](https://api-v2.yuafeng.cn/api_details.php?id=55) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·企鹅群头像](https://api-v2.yuafeng.cn/api_details.php?id=54) | image | 启用 | qun | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·明日方舟蓝图分享码](https://api-v2.yuafeng.cn/api_details.php?id=53) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·IP归属地查询(仅支持IPV4)](https://api-v2.yuafeng.cn/api_details.php?id=52) | text | 启用 | ip → type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·ocr图片文字提取](https://api-v2.yuafeng.cn/api_details.php?id=51) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·AI文本审核（高速）](https://api-v2.yuafeng.cn/api_details.php?id=49) | text | 停用 | text | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·tx新闻热搜](https://api-v2.yuafeng.cn/api_details.php?id=48) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·蓝奏云解析（支持密码）](https://api-v2.yuafeng.cn/api_details.php?id=47) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·最右视频解析(视频、图集）](https://api-v2.yuafeng.cn/api_details.php?id=46) | video | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·kg_mv视频](https://api-v2.yuafeng.cn/api_details.php?id=44) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·12306车站大屏信息](https://api-v2.yuafeng.cn/api_details.php?id=43) | text | 停用 | city → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·每日三角洲密码](https://api-v2.yuafeng.cn/api_details.php?id=42) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·baidu短剧搜索](https://api-v2.yuafeng.cn/api_details.php?id=41) | text | 停用 | name | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·wx客户端链接阻拦状态](https://api-v2.yuafeng.cn/api_details.php?id=40) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·成语查询](https://api-v2.yuafeng.cn/api_details.php?id=39) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·超级答题王](https://api-v2.yuafeng.cn/api_details.php?id=38) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·今日热门](https://api-v2.yuafeng.cn/api_details.php?id=36) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·回森解析](https://api-v2.yuafeng.cn/api_details.php?id=34) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·KFC文案](https://api-v2.yuafeng.cn/api_details.php?id=32) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·随机超能力](https://api-v2.yuafeng.cn/api_details.php?id=31) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·AI图片变清晰](https://api-v2.yuafeng.cn/api_details.php?id=30) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·AI抠图](https://api-v2.yuafeng.cn/api_details.php?id=29) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·ping](https://api-v2.yuafeng.cn/api_details.php?id=27) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·百度百科词条搜索](https://api-v2.yuafeng.cn/api_details.php?id=26) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·历史上的今天](https://api-v2.yuafeng.cn/api_details.php?id=25) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·应用宝软件搜索](https://api-v2.yuafeng.cn/api_details.php?id=23) | text | 停用 | name | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·图片格式转换②](https://api-v2.yuafeng.cn/api_details.php?id=22) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·图片格式转换①](https://api-v2.yuafeng.cn/api_details.php?id=21) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·IP经纬度查询（支持ipv6）](https://api-v2.yuafeng.cn/api_details.php?id=20) | text | 停用 | ip | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·看图猜成语](https://api-v2.yuafeng.cn/api_details.php?id=18) | text | 停用 | action | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·官机获取用户头像](https://api-v2.yuafeng.cn/api_details.php?id=16) | text | 停用 | appid → openid | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·文本乱序](https://api-v2.yuafeng.cn/api_details.php?id=12) | text | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·咪小咕点歌](https://api-v2.yuafeng.cn/api_details.php?id=11) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·违禁词检测](https://api-v2.yuafeng.cn/api_details.php?id=7) | text | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [枫雨二代·大模型语音合成](https://api-v2.yuafeng.cn/api_details.php?id=6) | text | 停用 | text | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·语言合成](https://api-v2.yuafeng.cn/api_details.php?id=5) | text | 停用 | text | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·快递查询](https://api-v2.yuafeng.cn/api_details.php?id=4) | text | 停用 | id → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·影视搜索](https://api-v2.yuafeng.cn/api_details.php?id=3) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [枫雨二代·小说搜索](https://api-v2.yuafeng.cn/api_details.php?id=2) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [糖豆子·人工智能大模型](https://api.tangdouz.com/api/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%A4%A7%E6%A8%A1%E5%9E%8B.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·IP反查域名](https://api.tangdouz.com/api/IP%E5%8F%8D%E6%9F%A5%E5%9F%9F%E5%90%8D.html) | text | 启用 | ip → f → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·万象棋](https://api.tangdouz.com/api/%E4%B8%87%E8%B1%A1%E6%A3%8B.html) | text | 停用 | f → type → size → q → fields → id → sort → cat | 需要站点密钥或登录凭据，配置后手动启用 |
| [糖豆子·藏头诗](https://api.tangdouz.com/api/%E8%97%8F%E5%A4%B4%E8%AF%97.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·小黑盒即将上线游戏](https://api.tangdouz.com/api/%E5%B0%8F%E9%BB%91%E7%9B%92%E5%8D%B3%E5%B0%86%E4%B8%8A%E7%BA%BF%E6%B8%B8%E6%88%8F.html) | text | 启用 | return → date → flat → limit → platform → next | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·星座运势](https://api.tangdouz.com/api/%E6%98%9F%E5%BA%A7%E8%BF%90%E5%8A%BF.html) | text | 启用 | xz → return → type → id → list | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·最近上映电影](https://api.tangdouz.com/api/%E6%9C%80%E8%BF%91%E4%B8%8A%E6%98%A0%E7%94%B5%E5%BD%B1.html) | text | 启用 | return → limit | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·解析扫描](https://api.tangdouz.com/api/%E8%A7%A3%E6%9E%90%E6%89%AB%E6%8F%8F.html) | text | 启用 | url → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·端口扫描](https://api.tangdouz.com/api/%E7%AB%AF%E5%8F%A3%E6%89%AB%E6%8F%8F.html) | text | 启用 | host → ports | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·Ping检测](https://api.tangdouz.com/api/Ping%E6%A3%80%E6%B5%8B.html) | text | 启用 | host → count | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·动效文字GIF](https://api.tangdouz.com/api/%E5%8A%A8%E6%95%88%E6%96%87%E5%AD%97GIF.html) | image | 启用 | text → style → speed → bg → textcolor → overcolor | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·实时汇率](https://api.tangdouz.com/api/%E5%AE%9E%E6%97%B6%E6%B1%87%E7%8E%87.html) | text | 启用 | from → to → amount → list | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·IP归属地精准查询](https://api.tangdouz.com/api/IP%E5%BD%92%E5%B1%9E%E5%9C%B0%E7%B2%BE%E5%87%86%E6%9F%A5%E8%AF%A2.html) | text | 启用 | ip → return → f | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·分钟级天气预测](https://api.tangdouz.com/api/%E5%88%86%E9%92%9F%E7%BA%A7%E5%A4%A9%E6%B0%94%E9%A2%84%E6%B5%8B.html) | text | 启用 | city → hours → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机网名及头像](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E7%BD%91%E5%90%8D%E5%8F%8A%E5%A4%B4%E5%83%8F.html) | text | 启用 | xb → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·mc我的世界wiki](https://api.tangdouz.com/api/mc%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8Cwiki.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·ICP备案查询](https://api.tangdouz.com/api/ICP%E5%A4%87%E6%A1%88%E6%9F%A5%E8%AF%A2.html) | text | 启用 | type → search → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·台风实时数据](https://api.tangdouz.com/api/%E5%8F%B0%E9%A3%8E%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE.html) | text | 启用 | id → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·肥鱼说](https://api.tangdouz.com/api/%E8%82%A5%E9%B1%BC%E8%AF%B4.html) | image | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·B站番剧时间表](https://api.tangdouz.com/api/B%E7%AB%99%E7%95%AA%E5%89%A7%E6%97%B6%E9%97%B4%E8%A1%A8.html) | text | 启用 | name → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·每日日报](https://api.tangdouz.com/api/%E6%AF%8F%E6%97%A5%E6%97%A5%E6%8A%A5.html) | text | 启用 | url → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·小黑盒帖子解析](https://api.tangdouz.com/api/%E5%B0%8F%E9%BB%91%E7%9B%92%E5%B8%96%E5%AD%90%E8%A7%A3%E6%9E%90.html) | text | 启用 | url → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·阴阳师模拟抽卡](https://api.tangdouz.com/api/%E9%98%B4%E9%98%B3%E5%B8%88%E6%A8%A1%E6%8B%9F%E6%8A%BD%E5%8D%A1.html) | text | 启用 | n | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·markdown与html互转](https://api.tangdouz.com/api/markdown%E4%B8%8Ehtml%E4%BA%92%E8%BD%AC.html) | text | 启用 | md → html → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·每日日历](https://api.tangdouz.com/api/%E6%AF%8F%E6%97%A5%E6%97%A5%E5%8E%86.html) | text | 启用 | content → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·文字转拼音](https://api.tangdouz.com/api/%E6%96%87%E5%AD%97%E8%BD%AC%E6%8B%BC%E9%9F%B3.html) | text | 启用 | msg → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·唱歌](https://api.tangdouz.com/api/%E5%94%B1%E6%AD%8C.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·piv每日随机图片](https://api.tangdouz.com/api/piv%E6%AF%8F%E6%97%A5%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·域名ssl证书查询](https://api.tangdouz.com/api/%E5%9F%9F%E5%90%8Dssl%E8%AF%81%E4%B9%A6%E6%9F%A5%E8%AF%A2.html) | text | 启用 | url → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·多设备共享文本](https://api.tangdouz.com/api/%E5%A4%9A%E8%AE%BE%E5%A4%87%E5%85%B1%E4%BA%AB%E6%96%87%E6%9C%AC.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·浙商积存金实时金价api](https://api.tangdouz.com/api/%E6%B5%99%E5%95%86%E7%A7%AF%E5%AD%98%E9%87%91%E5%AE%9E%E6%97%B6%E9%87%91%E4%BB%B7api.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机哈基米音乐](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E5%93%88%E5%9F%BA%E7%B1%B3%E9%9F%B3%E4%B9%90.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·拟人语音合成](https://api.tangdouz.com/api/%E6%8B%9F%E4%BA%BA%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·古风小生标签图片](https://api.tangdouz.com/api/%E5%8F%A4%E9%A3%8E%E5%B0%8F%E7%94%9F%E6%A0%87%E7%AD%BE%E5%9B%BE%E7%89%87.html) | image | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·饥荒wiki](https://api.tangdouz.com/api/%E9%A5%A5%E8%8D%92wiki.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·whois查询](https://api.tangdouz.com/api/whois%E6%9F%A5%E8%AF%A2.html) | text | 启用 | url → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·360随机风景壁纸](https://api.tangdouz.com/api/360%E9%9A%8F%E6%9C%BA%E9%A3%8E%E6%99%AF%E5%A3%81%E7%BA%B8.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·喜加一](https://api.tangdouz.com/api/%E5%96%9C%E5%8A%A0%E4%B8%80.html) | text | 启用 | name → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·语音转文字](https://api.tangdouz.com/api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E6%96%87%E5%AD%97.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·随机谜语](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E8%B0%9C%E8%AF%AD.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·脑筋急转弯](https://api.tangdouz.com/api/%E8%84%91%E7%AD%8B%E6%80%A5%E8%BD%AC%E5%BC%AF.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·显卡排行榜](https://api.tangdouz.com/api/%E6%98%BE%E5%8D%A1%E6%8E%92%E8%A1%8C%E6%A6%9C.html) | text | 启用 | f → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·死亡结果计算器](https://api.tangdouz.com/api/%E6%AD%BB%E4%BA%A1%E7%BB%93%E6%9E%9C%E8%AE%A1%E7%AE%97%E5%99%A8.html) | text | 启用 | return → nian → yue → ri → xingbie → shengao → tizhong → xintai → xiyan | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·垃圾分类](https://api.tangdouz.com/api/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·古诗名句](https://api.tangdouz.com/api/%E5%8F%A4%E8%AF%97%E5%90%8D%E5%8F%A5.html) | text | 启用 | name → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·节日倒计时](https://api.tangdouz.com/api/%E8%8A%82%E6%97%A5%E5%80%92%E8%AE%A1%E6%97%B6.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·MC基岩版最新版本号](https://api.tangdouz.com/api/MC%E5%9F%BA%E5%B2%A9%E7%89%88%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC%E5%8F%B7.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·网页截图](https://api.tangdouz.com/api/%E7%BD%91%E9%A1%B5%E6%88%AA%E5%9B%BE.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·文字找茬](https://api.tangdouz.com/api/%E6%96%87%E5%AD%97%E6%89%BE%E8%8C%AC.html) | text | 启用 | x → y | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·每日一句](https://api.tangdouz.com/api/%E6%AF%8F%E6%97%A5%E4%B8%80%E5%8F%A5.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·音频转silk](https://api.tangdouz.com/api/%E9%9F%B3%E9%A2%91%E8%BD%ACsilk.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·哔哩哔哩热榜](https://api.tangdouz.com/api/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E7%83%AD%E6%A6%9C.html) | text | 启用 | keyword → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·科技资讯](https://api.tangdouz.com/api/%E7%A7%91%E6%8A%80%E8%B5%84%E8%AE%AF.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·古诗](https://api.tangdouz.com/api/%E5%8F%A4%E8%AF%97.html) | text | 启用 | name → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·抽签](https://api.tangdouz.com/api/%E6%8A%BD%E7%AD%BE.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·🐧，音乐点歌](https://api.tangdouz.com/api/%F0%9F%90%A7%EF%BC%8C%E9%9F%B3%E4%B9%90%E7%82%B9%E6%AD%8C.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·金铲铲公告](https://api.tangdouz.com/api/%E9%87%91%E9%93%B2%E9%93%B2%E5%85%AC%E5%91%8A.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·5v5公告](https://api.tangdouz.com/api/5v5%E5%85%AC%E5%91%8A.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·元梦之星公告](https://api.tangdouz.com/api/%E5%85%83%E6%A2%A6%E4%B9%8B%E6%98%9F%E5%85%AC%E5%91%8A.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·原神公告](https://api.tangdouz.com/api/%E5%8E%9F%E7%A5%9E%E5%85%AC%E5%91%8A.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·阴阳师公告](https://api.tangdouz.com/api/%E9%98%B4%E9%98%B3%E5%B8%88%E5%85%AC%E5%91%8A.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·tea动态加解密](https://api.tangdouz.com/api/tea%E5%8A%A8%E6%80%81%E5%8A%A0%E8%A7%A3%E5%AF%86.html) | text | 停用 | f → nr | 需要站点密钥或登录凭据，配置后手动启用 |
| [糖豆子·urldecode](https://api.tangdouz.com/api/urldecode.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·24点巧算](https://api.tangdouz.com/api/24%E7%82%B9%E5%B7%A7%E7%AE%97.html) | text | 启用 | num1 → num2 → num3 → num4 → ms → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·一言1](https://api.tangdouz.com/api/%E4%B8%80%E8%A8%801.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·360随机动漫壁纸](https://api.tangdouz.com/api/360%E9%9A%8F%E6%9C%BA%E5%8A%A8%E6%BC%AB%E5%A3%81%E7%BA%B8.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·透明头像1](https://api.tangdouz.com/api/%E9%80%8F%E6%98%8E%E5%A4%B4%E5%83%8F1.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·表情包搜索](https://api.tangdouz.com/api/%E8%A1%A8%E6%83%85%E5%8C%85%E6%90%9C%E7%B4%A2.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·ai-网页体验版](https://api.tangdouz.com/api/ai-%E7%BD%91%E9%A1%B5%E4%BD%93%E9%AA%8C%E7%89%88.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [糖豆子·跑路表情包](https://api.tangdouz.com/api/%E8%B7%91%E8%B7%AF%E8%A1%A8%E6%83%85%E5%8C%85.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·幻兽帕鲁孵蛋计算器](https://api.tangdouz.com/api/%E5%B9%BB%E5%85%BD%E5%B8%95%E9%B2%81%E5%AD%B5%E8%9B%8B%E8%AE%A1%E7%AE%97%E5%99%A8.html) | text | 启用 | palu1 → palu2 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·今日运势](https://api.tangdouz.com/api/%E4%BB%8A%E6%97%A5%E8%BF%90%E5%8A%BF.html) | image | 启用 | theme → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·日历](https://api.tangdouz.com/api/%E6%97%A5%E5%8E%86.html) | image | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·朋友圈一言](https://api.tangdouz.com/api/%E6%9C%8B%E5%8F%8B%E5%9C%88%E4%B8%80%E8%A8%80.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·骚扰电话查询](https://api.tangdouz.com/api/%E9%AA%9A%E6%89%B0%E7%94%B5%E8%AF%9D%E6%9F%A5%E8%AF%A2.html) | text | 启用 | phone | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·诗句摘录](https://api.tangdouz.com/api/%E8%AF%97%E5%8F%A5%E6%91%98%E5%BD%95.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·菜谱](https://api.tangdouz.com/api/%E8%8F%9C%E8%B0%B1.html) | text | 启用 | f → nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·cosplay集图，每天更新](https://api.tangdouz.com/api/cosplay%E9%9B%86%E5%9B%BE%EF%BC%8C%E6%AF%8F%E5%A4%A9%E6%9B%B4%E6%96%B0.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·心灵鸡汤](https://api.tangdouz.com/api/%E5%BF%83%E7%81%B5%E9%B8%A1%E6%B1%A4.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·浅草寺抽签](https://api.tangdouz.com/api/%E6%B5%85%E8%8D%89%E5%AF%BA%E6%8A%BD%E7%AD%BE.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·特殊名称](https://api.tangdouz.com/api/%E7%89%B9%E6%AE%8A%E5%90%8D%E7%A7%B0.html) | text | 启用 | name → wb → f | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·统计信息](https://api.tangdouz.com/api/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF.html) | text | 启用 | nr → name → sl → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·文案合集](https://api.tangdouz.com/api/%E6%96%87%E6%A1%88%E5%90%88%E9%9B%86.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·日出日落](https://api.tangdouz.com/api/%E6%97%A5%E5%87%BA%E6%97%A5%E8%90%BD.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·情书](https://api.tangdouz.com/api/%E6%83%85%E4%B9%A6.html) | text | 启用 | gon → shou | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·中草药](https://api.tangdouz.com/api/%E4%B8%AD%E8%8D%89%E8%8D%AF.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·你们看到她了吗](https://api.tangdouz.com/api/%E4%BD%A0%E4%BB%AC%E7%9C%8B%E5%88%B0%E5%A5%B9%E4%BA%86%E5%90%97.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·喜报](https://api.tangdouz.com/api/%E5%96%9C%E6%8A%A5.html) | image | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·透明头像](https://api.tangdouz.com/api/%E9%80%8F%E6%98%8E%E5%A4%B4%E5%83%8F.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·你怎么和··一样](https://api.tangdouz.com/api/%E4%BD%A0%E6%80%8E%E4%B9%88%E5%92%8C%2A%2A%E4%B8%80%E6%A0%B7.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·答题](https://api.tangdouz.com/api/%E7%AD%94%E9%A2%98.html) | text | 启用 | f | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机key](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BAkey.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·图片验证码](https://api.tangdouz.com/api/%E5%9B%BE%E7%89%87%E9%AA%8C%E8%AF%81%E7%A0%81.html) | image | 启用 | num | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机坤坤表情包](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E5%9D%A4%E5%9D%A4%E8%A1%A8%E6%83%85%E5%8C%85.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·中文域名](https://api.tangdouz.com/api/%E4%B8%AD%E6%96%87%E5%9F%9F%E5%90%8D.html) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·cp](https://api.tangdouz.com/api/cp.html) | text | 启用 | gon → shou | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·文章](https://api.tangdouz.com/api/%E6%96%87%E7%AB%A0.html) | text | 启用 | return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·绕口令](https://api.tangdouz.com/api/%E7%BB%95%E5%8F%A3%E4%BB%A4.html) | text | 启用 | msg → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·发病](https://api.tangdouz.com/api/%E5%8F%91%E7%97%85.html) | text | 启用 | name | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·中文检测](https://api.tangdouz.com/api/%E4%B8%AD%E6%96%87%E6%A3%80%E6%B5%8B.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·土味情话](https://api.tangdouz.com/api/%E5%9C%9F%E5%91%B3%E6%83%85%E8%AF%9D.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·撕](https://api.tangdouz.com/api/%E6%92%95.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·我朋友说](https://api.tangdouz.com/api/%E6%88%91%E6%9C%8B%E5%8F%8B%E8%AF%B4.html) | image | 启用 | q → nr → name | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·对对联](https://api.tangdouz.com/api/%E5%AF%B9%E5%AF%B9%E8%81%94.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·抖.音解析](https://api.tangdouz.com/api/%E6%8A%96.%E9%9F%B3%E8%A7%A3%E6%9E%90.html) | text | 启用 | lj | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·时间戳转时间](https://api.tangdouz.com/api/%E6%97%B6%E9%97%B4%E6%88%B3%E8%BD%AC%E6%97%B6%E9%97%B4.html) | text | 启用 | time | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·想](https://api.tangdouz.com/api/%E6%83%B3.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·我老婆](https://api.tangdouz.com/api/%E6%88%91%E8%80%81%E5%A9%86.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·吃](https://api.tangdouz.com/api/%E5%90%83.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·塔罗牌](https://api.tangdouz.com/api/%E5%A1%94%E7%BD%97%E7%89%8C.html) | text | 启用 | img → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·图文合成②号接口](https://api.tangdouz.com/api/%E5%9B%BE%E6%96%87%E5%90%88%E6%88%90%E2%91%A1%E5%8F%B7%E6%8E%A5%E5%8F%A3.html) | image | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·答案之书](https://api.tangdouz.com/api/%E7%AD%94%E6%A1%88%E4%B9%8B%E4%B9%A6.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·天气](https://api.tangdouz.com/api/%E5%A4%A9%E6%B0%94.html) | text | 启用 | dz → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·爬](https://api.tangdouz.com/api/%E7%88%AC.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·解字节型加密](https://api.tangdouz.com/api/%E8%A7%A3%E5%AD%97%E8%8A%82%E5%9E%8B%E5%8A%A0%E5%AF%86.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·王者英雄语音](https://api.tangdouz.com/api/%E7%8E%8B%E8%80%85%E8%8B%B1%E9%9B%84%E8%AF%AD%E9%9F%B3.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·图文合成接口](https://api.tangdouz.com/api/%E5%9B%BE%E6%96%87%E5%90%88%E6%88%90%E6%8E%A5%E5%8F%A3.html) | image | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·群友说](https://api.tangdouz.com/api/%E7%BE%A4%E5%8F%8B%E8%AF%B4.html) | image | 启用 | qq → nr → sf → name | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·相思](https://api.tangdouz.com/api/%E7%9B%B8%E6%80%9D.html) | image | 启用 | q → nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·拽](https://api.tangdouz.com/api/%E6%8B%BD.html) | image | 启用 | q → nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·报时、整点报时②](https://api.tangdouz.com/api/%E6%8A%A5%E6%97%B6%E3%80%81%E6%95%B4%E7%82%B9%E6%8A%A5%E6%97%B6%E2%91%A1.html) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·标签图片](https://api.tangdouz.com/api/%E6%A0%87%E7%AD%BE%E5%9B%BE%E7%89%87.html) | image | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·打开QQ群](https://api.tangdouz.com/api/%E6%89%93%E5%BC%80QQ%E7%BE%A4.html) | text | 启用 | qh | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·打开QQ名片](https://api.tangdouz.com/api/%E6%89%93%E5%BC%80QQ%E5%90%8D%E7%89%87.html) | text | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机动漫壁纸](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E5%8A%A8%E6%BC%AB%E5%A3%81%E7%BA%B8.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·签到图](https://api.tangdouz.com/api/%E7%AD%BE%E5%88%B0%E5%9B%BE.html) | image | 启用 | qq → bt → nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·来份兽耳](https://api.tangdouz.com/api/%E6%9D%A5%E4%BB%BD%E5%85%BD%E8%80%B3.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·刑法](https://api.tangdouz.com/api/%E5%88%91%E6%B3%95.html) | text | 启用 | nr → xz | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·捅](https://api.tangdouz.com/api/%E6%8D%85.html) | image | 启用 | q → qq | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·多随机数](https://api.tangdouz.com/api/%E5%A4%9A%E9%9A%8F%E6%9C%BA%E6%95%B0.html) | text | 启用 | min → max → num | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机数](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E6%95%B0.html) | text | 启用 | min → max | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·农历](https://api.tangdouz.com/api/%E5%86%9C%E5%8E%86.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机鲲](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E9%B2%B2.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·看电视](https://api.tangdouz.com/api/%E7%9C%8B%E7%94%B5%E8%A7%86.html) | image | 启用 | q | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·公告](https://api.tangdouz.com/api/%E5%85%AC%E5%91%8A.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·猜字谜](https://api.tangdouz.com/api/%E7%8C%9C%E5%AD%97%E8%B0%9C.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·颜色转图片](https://api.tangdouz.com/api/%E9%A2%9C%E8%89%B2%E8%BD%AC%E5%9B%BE%E7%89%87.html) | image | 启用 | color | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口⑥](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A5.html) | text | 启用 | num → a → b | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机名字](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E5%90%8D%E5%AD%97.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·排行榜](https://api.tangdouz.com/api/%E6%8E%92%E8%A1%8C%E6%A6%9C.html) | text | 停用 | 无 | 此条可能是网页工具入口，需确认后启用 |
| [糖豆子·接口搜索-右上角列表展开](https://api.tangdouz.com/api/%E6%8E%A5%E5%8F%A3%E6%90%9C%E7%B4%A2-%E5%8F%B3%E4%B8%8A%E8%A7%92%E5%88%97%E8%A1%A8%E5%B1%95%E5%BC%80.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·一中一英一言](https://api.tangdouz.com/api/%E4%B8%80%E4%B8%AD%E4%B8%80%E8%8B%B1%E4%B8%80%E8%A8%80.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口⑤](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A4.html) | text | 启用 | nr → nr1 → f | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·百度百科](https://api.tangdouz.com/api/%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·二十四节气](https://api.tangdouz.com/api/%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口④](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A3.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口③](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A2.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口②](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A1.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·奇怪的接口①](https://api.tangdouz.com/api/%E5%A5%87%E6%80%AA%E7%9A%84%E6%8E%A5%E5%8F%A3%E2%91%A0.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·哔哩哔哩搜索](https://api.tangdouz.com/api/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E6%90%9C%E7%B4%A2.html) | text | 启用 | nr → a | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·报时，图片版](https://api.tangdouz.com/api/%E6%8A%A5%E6%97%B6%EF%BC%8C%E5%9B%BE%E7%89%87%E7%89%88.html) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·葫芦侠应用or游戏搜索](https://api.tangdouz.com/api/%E8%91%AB%E8%8A%A6%E4%BE%A0%E5%BA%94%E7%94%A8or%E6%B8%B8%E6%88%8F%E6%90%9C%E7%B4%A2.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·我的世界pe服务器查询](https://api.tangdouz.com/api/%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8Cpe%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%9F%A5%E8%AF%A2.html) | text | 启用 | ip → dk → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·翻译](https://api.tangdouz.com/api/%E7%BF%BB%E8%AF%91.html) | text | 启用 | nr → return | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·电池电量](https://api.tangdouz.com/api/%E7%94%B5%E6%B1%A0%E7%94%B5%E9%87%8F.html) | image | 启用 | dl | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·毒鸡汤](https://api.tangdouz.com/api/%E6%AF%92%E9%B8%A1%E6%B1%A4.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·爱情公寓一言](https://api.tangdouz.com/api/%E7%88%B1%E6%83%85%E5%85%AC%E5%AF%93%E4%B8%80%E8%A8%80.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·牵](https://api.tangdouz.com/api/%E7%89%B5.html) | image | 启用 | q → qq → qname → qqname | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·买家秀](https://api.tangdouz.com/api/%E4%B9%B0%E5%AE%B6%E7%A7%80.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·笑话](https://api.tangdouz.com/api/%E7%AC%91%E8%AF%9D.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·vivo主题下载](https://api.tangdouz.com/api/vivo%E4%B8%BB%E9%A2%98%E4%B8%8B%E8%BD%BD.html) | text | 启用 | lj | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·堆糖搜索](https://api.tangdouz.com/api/%E5%A0%86%E7%B3%96%E6%90%9C%E7%B4%A2.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·手机短信验证码接口](https://api.tangdouz.com/api/%E6%89%8B%E6%9C%BA%E7%9F%AD%E4%BF%A1%E9%AA%8C%E8%AF%81%E7%A0%81%E6%8E%A5%E5%8F%A3.html) | text | 停用 | 无 | 此条可能是网页工具入口，需确认后启用 |
| [糖豆子·你画我猜词条](https://api.tangdouz.com/api/%E4%BD%A0%E7%94%BB%E6%88%91%E7%8C%9C%E8%AF%8D%E6%9D%A1.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·乘法](https://api.tangdouz.com/api/%E4%B9%98%E6%B3%95.html) | text | 启用 | nu → num → numm | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·除法](https://api.tangdouz.com/api/%E9%99%A4%E6%B3%95.html) | text | 启用 | nu → num → numm | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·加法](https://api.tangdouz.com/api/%E5%8A%A0%E6%B3%95.html) | text | 启用 | nu → num → numm | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·减法](https://api.tangdouz.com/api/%E5%87%8F%E6%B3%95.html) | text | 启用 | nu → num | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·图片鉴黄](https://api.tangdouz.com/api/%E5%9B%BE%E7%89%87%E9%89%B4%E9%BB%84.html) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用；此条可能是网页工具入口，需确认后启用 |
| [糖豆子·随机高清动漫图片](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E9%AB%98%E6%B8%85%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·bing每日美图](https://api.tangdouz.com/api/bing%E6%AF%8F%E6%97%A5%E7%BE%8E%E5%9B%BE.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·冷知识](https://api.tangdouz.com/api/%E5%86%B7%E7%9F%A5%E8%AF%86.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·json编码转换，unicode](https://api.tangdouz.com/api/json%E7%BC%96%E7%A0%81%E8%BD%AC%E6%8D%A2%EF%BC%8Cunicode.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·历史上的今天](https://api.tangdouz.com/api/%E5%8E%86%E5%8F%B2%E4%B8%8A%E7%9A%84%E4%BB%8A%E5%A4%A9.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·美腿](https://api.tangdouz.com/api/%E7%BE%8E%E8%85%BF.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·高清视频壁纸，每日更新](https://api.tangdouz.com/api/%E9%AB%98%E6%B8%85%E8%A7%86%E9%A2%91%E5%A3%81%E7%BA%B8%EF%BC%8C%E6%AF%8F%E6%97%A5%E6%9B%B4%E6%96%B0.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·高清壁纸，每日更新](https://api.tangdouz.com/api/%E9%AB%98%E6%B8%85%E5%A3%81%E7%BA%B8%EF%BC%8C%E6%AF%8F%E6%97%A5%E6%9B%B4%E6%96%B0.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·搜图](https://api.tangdouz.com/api/%E6%90%9C%E5%9B%BE.html) | text | 启用 | nr → sl | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·情侣名字](https://api.tangdouz.com/api/%E6%83%85%E4%BE%A3%E5%90%8D%E5%AD%97.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·文字数量](https://api.tangdouz.com/api/%E6%96%87%E5%AD%97%E6%95%B0%E9%87%8F.html) | text | 启用 | lt | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·微博热搜](https://api.tangdouz.com/api/%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C.html) | text | 启用 | list | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·抽奖概率](https://api.tangdouz.com/api/%E6%8A%BD%E5%A5%96%E6%A6%82%E7%8E%87.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·百度搜索](https://api.tangdouz.com/api/%E7%99%BE%E5%BA%A6%E6%90%9C%E7%B4%A2.html) | text | 启用 | nr | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·美女api](https://api.tangdouz.com/api/%E7%BE%8E%E5%A5%B3api.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机颜色代码](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E9%A2%9C%E8%89%B2%E4%BB%A3%E7%A0%81.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·ip地理位置及网络查询](https://api.tangdouz.com/api/ip%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E5%8F%8A%E7%BD%91%E7%BB%9C%E6%9F%A5%E8%AF%A2.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·时间接口](https://api.tangdouz.com/api/%E6%97%B6%E9%97%B4%E6%8E%A5%E5%8F%A3.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·随机一言接口](https://api.tangdouz.com/api/%E9%9A%8F%E6%9C%BA%E4%B8%80%E8%A8%80%E6%8E%A5%E5%8F%A3.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [糖豆子·舔狗日记](https://api.tangdouz.com/api/%E8%88%94%E7%8B%97%E6%97%A5%E8%AE%B0.html) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·抖音点歌](https://free.wqwlkj.cn/?action=interface&id=128) | text | 启用 | name → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·爱奇艺热搜风云榜](https://free.wqwlkj.cn/?action=interface&id=127) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·360热搜榜](https://free.wqwlkj.cn/?action=interface&id=126) | text | 启用 | n → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·一笔签名设计](https://free.wqwlkj.cn/?action=interface&id=105) | text | 启用 | id → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·支付宝到账语音生成](https://free.wqwlkj.cn/?action=interface&id=103) | audio | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·个性头像](https://free.wqwlkj.cn/?action=interface&id=101) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·网易云热歌榜随机音乐](https://free.wqwlkj.cn/?action=interface&id=36) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·金价查询](https://free.wqwlkj.cn/?action=interface&id=138) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ音乐（免vip_ogg文件）](https://free.wqwlkj.cn/?action=interface&id=137) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·身份证解析api](https://free.wqwlkj.cn/?action=interface&id=42) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·文字找茬](https://free.wqwlkj.cn/?action=interface&id=136) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·图片直链转base64图片](https://free.wqwlkj.cn/?action=interface&id=135) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·星座运势查询](https://free.wqwlkj.cn/?action=interface&id=134) | text | 启用 | name | 按公开文档生成，业务有效性待实例验证 |
| [问情·猜成语接口](https://free.wqwlkj.cn/?action=interface&id=133) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·笑话API](https://free.wqwlkj.cn/?action=interface&id=132) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·百度云ocr精准位置版](https://free.wqwlkj.cn/?action=interface&id=131) | text | 停用 | url | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·铃声多多接口_按榜单](https://free.wqwlkj.cn/?action=interface&id=130) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·铃声多多接口_按名字](https://free.wqwlkj.cn/?action=interface&id=129) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·酷我音乐（不支持付费音乐）](https://free.wqwlkj.cn/?action=interface&id=100) | text | 启用 | n | 按公开文档生成，业务有效性待实例验证 |
| [问情·随机唱鸭音频](https://free.wqwlkj.cn/?action=interface&id=67) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·抖音视频无水印解析](https://free.wqwlkj.cn/?action=interface&id=125) | text | 停用 | video | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·base64图片转换](https://free.wqwlkj.cn/?action=interface&id=124) | text | 停用 | img | 文档未声明支持 GET，当前请求引擎需另适配 |
| [问情·QQ头框生成](https://free.wqwlkj.cn/?action=interface&id=3) | image | 启用 | qq → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·域名whois查询](https://free.wqwlkj.cn/?action=interface&id=123) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ注册时间，q龄查询](https://free.wqwlkj.cn/?action=interface&id=122) | text | 停用 | qq → type | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·QQ昵称获取（无需ck）](https://free.wqwlkj.cn/?action=interface&id=121) | text | 停用 | qq → type | 网站目录或文档标记为维护、停用或状态未知；涉及登录、上传或多步骤操作，需额外配置/流程 |
| [问情·ai绘画](https://free.wqwlkj.cn/?action=interface&id=120) | text | 停用 | msg | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·[游戏接口]ai成语接龙](https://free.wqwlkj.cn/?action=interface&id=119) | text | 启用 | select → user → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·抖音视频搜索](https://free.wqwlkj.cn/?action=interface&id=118) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·摸鱼人日历](https://free.wqwlkj.cn/?action=interface&id=117) | image | 停用 | type | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·QQ名片制作1](https://free.wqwlkj.cn/?action=interface&id=116) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·[游戏接口]五子棋](https://free.wqwlkj.cn/?action=interface&id=115) | text | 启用 | type → group → qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·斗鱼直播查询](https://free.wqwlkj.cn/?action=interface&id=114) | text | 启用 | name | 按公开文档生成，业务有效性待实例验证 |
| [问情·百度百科接口](https://free.wqwlkj.cn/?action=interface&id=113) | text | 启用 | msg → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·中文单字笔画查询](https://free.wqwlkj.cn/?action=interface&id=107) | text | 启用 | word → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·知乎每日60s](https://free.wqwlkj.cn/?action=interface&id=112) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·舔狗日记（图片版）](https://free.wqwlkj.cn/?action=interface&id=111) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·王者荣耀英雄图集](https://free.wqwlkj.cn/?action=interface&id=110) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·仿手写自动换行图文接口](https://free.wqwlkj.cn/?action=interface&id=109) | image | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [问情·电影今日票房](https://free.wqwlkj.cn/?action=interface&id=108) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·中文转拼音](https://free.wqwlkj.cn/?action=interface&id=106) | text | 启用 | word → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·骚扰电话查询](https://free.wqwlkj.cn/?action=interface&id=27) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·表情包搜索](https://free.wqwlkj.cn/?action=interface&id=102) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·qr授权查询](https://free.wqwlkj.cn/?action=interface&id=99) | text | 启用 | qq → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·油价查询](https://free.wqwlkj.cn/?action=interface&id=98) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·chatgpt接口](https://free.wqwlkj.cn/?action=interface&id=87) | text | 停用 | msg | 网站目录或文档标记为维护、停用或状态未知；参数 key 涉及账号/凭据，请按站点文档单独配置 |
| [问情·QQ音乐（VIP版）](https://free.wqwlkj.cn/?action=interface&id=92) | text | 停用 | msg → type | 参数 Cookie 涉及账号/凭据，请按站点文档单独配置 |
| [问情·抽签](https://free.wqwlkj.cn/?action=interface&id=97) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·emoji表情合成](https://free.wqwlkj.cn/?action=interface&id=96) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ音乐（不支持VIP，付费歌曲）](https://free.wqwlkj.cn/?action=interface&id=95) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·识别二维码](https://free.wqwlkj.cn/?action=interface&id=94) | text | 启用 | url → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·咪咕音乐](https://free.wqwlkj.cn/?action=interface&id=93) | text | 启用 | msg → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·快手热门短视频](https://free.wqwlkj.cn/?action=interface&id=91) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·天气查询](https://free.wqwlkj.cn/?action=interface&id=90) | text | 启用 | city → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·快递100查询](https://free.wqwlkj.cn/?action=interface&id=89) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·自适应图文接口](https://free.wqwlkj.cn/?action=interface&id=46) | image | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·帅哥腹肌](https://free.wqwlkj.cn/?action=interface&id=88) | image | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·网易云热评](https://free.wqwlkj.cn/?action=interface&id=86) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·获取请求用户的ip（图片版）](https://free.wqwlkj.cn/?action=interface&id=84) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·食物卡路里查询](https://free.wqwlkj.cn/?action=interface&id=83) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·网站权重查询](https://free.wqwlkj.cn/?action=interface&id=82) | text | 启用 | url → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·ikun鸡歌](https://free.wqwlkj.cn/?action=interface&id=81) | audio | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·腾讯视频热搜](https://free.wqwlkj.cn/?action=interface&id=80) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·漂流瓶](https://free.wqwlkj.cn/?action=interface&id=79) | text | 启用 | content → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·今日头条热搜榜](https://free.wqwlkj.cn/?action=interface&id=78) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·网站快照](https://free.wqwlkj.cn/?action=interface&id=77) | image | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·手机号归属地查询](https://free.wqwlkj.cn/?action=interface&id=76) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·挑战古诗词](https://free.wqwlkj.cn/?action=interface&id=75) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·最新检测域名是否能在微信正常打开](https://free.wqwlkj.cn/?action=interface&id=74) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·图片报时](https://free.wqwlkj.cn/?action=interface&id=73) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·ikun有关图片](https://free.wqwlkj.cn/?action=interface&id=72) | image | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·个性网名](https://free.wqwlkj.cn/?action=interface&id=71) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·酷狗音乐点歌](https://free.wqwlkj.cn/?action=interface&id=70) | text | 启用 | msg → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·车牌号归属地查询](https://free.wqwlkj.cn/?action=interface&id=69) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [问情·域名注册查询](https://free.wqwlkj.cn/?action=interface&id=68) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·免费QQ名片赞](https://free.wqwlkj.cn/?action=interface&id=66) | text | 停用 | qq | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·域名备案查询](https://free.wqwlkj.cn/?action=interface&id=65) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·蓝奏云直链解析](https://free.wqwlkj.cn/?action=interface&id=64) | text | 启用 | url → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·买吧，不贵（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=63) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·快了，已经在做了（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=62) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·教我写代码（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=61) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·方方方面面给我安排好（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=60) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我还是萌新一个（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=59) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·差评（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=58) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·好评（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=57) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·没马内很难帮你办事（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=56) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·抱着哭（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=55) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我tm教你做事（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=54) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我好羡慕啊（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=53) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我为坤举旗（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=52) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我拍死你个憨批（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=51) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·无所谓看蛋了（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=50) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·我想要money（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=49) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·黑白si举牌（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=48) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·se表情包（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=47) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·爬表情包生成（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=45) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·中国地图头像表情包（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=44) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·ping域名接口](https://free.wqwlkj.cn/?action=interface&id=43) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·搜索字词，成功，诗词](https://free.wqwlkj.cn/?action=interface&id=41) | text | 启用 | keyword | 按公开文档生成，业务有效性待实例验证 |
| [问情·qq估价](https://free.wqwlkj.cn/?action=interface&id=40) | text | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ名片制作](https://free.wqwlkj.cn/?action=interface&id=39) | image | 启用 | uin | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ说说id和内容获取](https://free.wqwlkj.cn/?action=interface&id=38) | text | 停用 | qq | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·二维码生成](https://free.wqwlkj.cn/?action=interface&id=37) | image | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [问情·跳转QQ名片](https://free.wqwlkj.cn/?action=interface&id=35) | text | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·获取请求用户的ip](https://free.wqwlkj.cn/?action=interface&id=34) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·cos小姐姐图片](https://free.wqwlkj.cn/?action=interface&id=33) | image | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·摸一摸（QQ头像）](https://free.wqwlkj.cn/?action=interface&id=32) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [问情·b站番剧更新列表](https://free.wqwlkj.cn/?action=interface&id=31) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·短视频无水印解析](https://free.wqwlkj.cn/?action=interface&id=30) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·快手小姐姐图片](https://free.wqwlkj.cn/?action=interface&id=29) | image | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·垃圾分类查询](https://free.wqwlkj.cn/?action=interface&id=28) | text | 启用 | msg → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·全国重名查询](https://free.wqwlkj.cn/?action=interface&id=26) | text | 启用 | name → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·快手二次元图片](https://free.wqwlkj.cn/?action=interface&id=25) | image | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ域名拦截检测](https://free.wqwlkj.cn/?action=interface&id=24) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [问情·全国降水量预报](https://free.wqwlkj.cn/?action=interface&id=23) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·百度热搜排行榜](https://free.wqwlkj.cn/?action=interface&id=22) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·网易云音乐歌曲搜索](https://free.wqwlkj.cn/?action=interface&id=21) | text | 启用 | name → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·抖音热搜排行榜](https://free.wqwlkj.cn/?action=interface&id=20) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·b站排行榜](https://free.wqwlkj.cn/?action=interface&id=19) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·百度收录查询](https://free.wqwlkj.cn/?action=interface&id=18) | text | 启用 | domain → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·知乎热搜排行榜](https://free.wqwlkj.cn/?action=interface&id=17) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·图形验证码生成](https://free.wqwlkj.cn/?action=interface&id=16) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·有道翻译](https://free.wqwlkj.cn/?action=interface&id=15) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·舔狗日记](https://free.wqwlkj.cn/?action=interface&id=14) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·QQ访客查询](https://free.wqwlkj.cn/?action=interface&id=13) | text | 启用 | qq → type | 按公开文档生成，业务有效性待实例验证 |
| [问情·全国疫情查询](https://free.wqwlkj.cn/?action=interface&id=12) | text | 停用 | type | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·实时微博热搜排行榜](https://free.wqwlkj.cn/?action=interface&id=10) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·实时快手热搜排行榜](https://free.wqwlkj.cn/?action=interface&id=9) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·历史上的今天](https://free.wqwlkj.cn/?action=interface&id=8) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·每日一句（中文,英文）](https://free.wqwlkj.cn/?action=interface&id=7) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·获取b站up主信息](https://free.wqwlkj.cn/?action=interface&id=6) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·王者荣耀英雄个性语音包](https://free.wqwlkj.cn/?action=interface&id=5) | text | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [问情·bing每日一图](https://free.wqwlkj.cn/?action=interface&id=4) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [问情·快递查询](https://free.wqwlkj.cn/?action=interface&id=2) | text | 停用 | 无 | 网站目录或文档标记为维护、停用或状态未知 |
| [问情·小米壁纸接口](https://free.wqwlkj.cn/?action=interface&id=1) | text | 启用 | type | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·Ai风格转变](https://api.xingzhige.com/doc/59) | text | 启用 | url → model | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·Ai绘图](https://api.xingzhige.com/doc/58) | text | 启用 | prompt → model | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·ai说话](https://api.xingzhige.com/doc/57) | text | 停用 | module → text → voice → task_id | 文档包含异步或多步骤任务流程，单次调用不能完成全部功能 |
| [星之阁·短剧搜索](https://api.xingzhige.com/doc/56) | text | 启用 | keyword | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·酷狗·QQ歌词获取](https://api.xingzhige.com/doc/55) | text | 启用 | id → mid | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·看看小世界](https://api.xingzhige.com/doc/54) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·看看西瓜](https://api.xingzhige.com/doc/53) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·看看快手](https://api.xingzhige.com/doc/52) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·看看动漫](https://api.xingzhige.com/doc/51) | text | 启用 | msg | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·看看抖音](https://api.xingzhige.com/doc/50) | text | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·搜索漫画](https://api.xingzhige.com/doc/49) | text | 启用 | keyword | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·波点音乐搜索v](https://api.xingzhige.com/doc/48) | text | 启用 | name | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·网易音乐搜索v](https://api.xingzhige.com/doc/46) | text | 启用 | name | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·素描](https://api.xingzhige.com/doc/45) | image | 启用 | url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·可莉吃](https://api.xingzhige.com/doc/44) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·爬！](https://api.xingzhige.com/doc/43) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·b站解析](https://api.xingzhige.com/doc/40) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；参数 access_key 涉及账号/凭据，请按站点文档单独配置 |
| [星之阁·b站番剧解析](https://api.xingzhige.com/doc/39) | text | 停用 | ss_id → ep_id | 参数 access_key 涉及账号/凭据，请按站点文档单独配置 |
| [星之阁·哔哩哔哩发私信](https://api.xingzhige.com/doc/38) | text | 启用 | mid → msg → sessdata → csrf | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·b站用户信息](https://api.xingzhige.com/doc/37) | text | 启用 | mid | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·cp宇宙触发器](https://api.xingzhige.com/doc/36) | text | 启用 | name1 → name2 | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·Minecraft皮肤渲染](https://api.xingzhige.com/doc/35) | text | 启用 | type → name → uuid → skinurl | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·原神黄历](https://api.xingzhige.com/doc/34) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·姓名缘分测试](https://api.xingzhige.com/doc/32) | text | 启用 | name1 → name2 | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·cp短打生成器](https://api.xingzhige.com/doc/31) | text | 启用 | g → s | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·获取QQ头像](https://api.xingzhige.com/doc/29) | text | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-打年糕](https://api.xingzhige.com/doc/26) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-舞鸡腿](https://api.xingzhige.com/doc/25) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-招财喵](https://api.xingzhige.com/doc/24) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-一起笑](https://api.xingzhige.com/doc/23) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·签到日历](https://api.xingzhige.com/doc/22) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·生成表情-抱肉肉](https://api.xingzhige.com/doc/21) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·b站扫码登录-tv](https://api.xingzhige.com/doc/20) | text | 停用 | auth_code | 涉及登录、上传或多步骤操作，需额外配置/流程 |
| [星之阁·生成表情-看这个](https://api.xingzhige.com/doc/18) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-咬](https://api.xingzhige.com/doc/17) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-顶球](https://api.xingzhige.com/doc/16) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-拍瓜](https://api.xingzhige.com/doc/15) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·表情生成-抓](https://api.xingzhige.com/doc/14) | image | 启用 | qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·修改群头像](https://api.xingzhige.com/doc/12) | text | 启用 | uin → skey → group → img_url | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·修改QQ昵称](https://api.xingzhige.com/doc/11) | text | 启用 | uin → skey → pskey | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·b站搜索](https://api.xingzhige.com/doc/10) | text | 启用 | msg → n | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·b站视频解析](https://api.xingzhige.com/doc/9) | text | 启用 | bvid → aid | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·QQ等级查询](https://api.xingzhige.com/doc/8) | text | 启用 | uin → skey → pskey → qq | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·钱包余额](https://api.xingzhige.com/doc/6) | text | 启用 | uin → skey → pskey | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·业务查询](https://api.xingzhige.com/doc/5) | text | 启用 | qq → uin → skey → pskey | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·网易云音乐随机热评](https://api.xingzhige.com/doc/4) | text | 启用 | id | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·二维码生成](https://api.xingzhige.com/doc/3) | image | 启用 | text | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·Bing每日一图](https://api.xingzhige.com/doc/2) | image | 启用 | 无 | 按公开文档生成，业务有效性待实例验证 |
| [星之阁·群活跃排行](https://api.xingzhige.com/doc/1) | text | 启用 | qq → skey → pskey → group | 按公开文档生成，业务有效性待实例验证 |
| [倾梦·大鹅音乐](https://api.317ak.com/detail/1) | text | 停用 | msg → type → qq | 需要站点密钥或登录凭据，配置后手动启用；参数 ck 涉及账号/凭据，请按站点文档单独配置 |
| [倾梦·黄盒音乐](https://api.317ak.com/detail/2) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·云村点歌](https://api.317ak.com/detail/3) | text | 停用 | msg → type → qq | 需要站点密钥或登录凭据，配置后手动启用；参数 ck 涉及账号/凭据，请按站点文档单独配置 |
| [倾梦·蓝狗音乐](https://api.317ak.com/detail/4) | text | 停用 | msg → type → qq | 需要站点密钥或登录凭据，配置后手动启用；参数 ck 涉及账号/凭据，请按站点文档单独配置 |
| [倾梦·蓝狗音乐概念版](https://api.317ak.com/detail/5) | text | 停用 | msg → type → qq | 需要站点密钥或登录凭据，配置后手动启用；参数 ck 涉及账号/凭据，请按站点文档单独配置 |
| [倾梦·蓝狗MV](https://api.317ak.com/detail/6) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·网易聚合榜](https://api.317ak.com/detail/7) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·百度聚合榜](https://api.317ak.com/detail/8) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·360聚合榜](https://api.317ak.com/detail/9) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·今日黄历](https://api.317ak.com/detail/10) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·王者战力查询](https://api.317ak.com/detail/11) | text | 停用 | hero → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·星座运势配对](https://api.317ak.com/detail/12) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·姓氏头像](https://api.317ak.com/detail/13) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·情侣头像](https://api.317ak.com/detail/14) | text | 停用 | xl → msg1 → msg2 → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·艺术壁纸](https://api.317ak.com/detail/15) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·艺术签名](https://api.317ak.com/detail/16) | text | 停用 | msg → id1 → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·脱口秀](https://api.317ak.com/detail/17) | text | 停用 | lx → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·油价查询](https://api.317ak.com/detail/20) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·历史上的今天(图片版)](https://api.317ak.com/detail/21) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·星座运势(图片版)](https://api.317ak.com/detail/22) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·星座运势(文字版)](https://api.317ak.com/detail/23) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ估价（文字版）](https://api.317ak.com/detail/24) | text | 停用 | qq → hh | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ估价（图片版）](https://api.317ak.com/detail/25) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·抽签算卦](https://api.317ak.com/detail/26) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·凤凰生活资讯早报](https://api.317ak.com/detail/27) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·二维码生成](https://api.317ak.com/detail/28) | text | 停用 | text → size | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·企鹅翻译](https://api.317ak.com/detail/29) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·小人举牌](https://api.317ak.com/detail/30) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·人品鉴定](https://api.317ak.com/detail/31) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·搜索听书](https://api.317ak.com/detail/32) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·兽语加密](https://api.317ak.com/detail/33) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·60秒读世界](https://api.317ak.com/detail/34) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·心知天气信息查询](https://api.317ak.com/detail/35) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·语音合成](https://api.317ak.com/detail/36) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·腾讯新闻头条](https://api.317ak.com/detail/37) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·哔哩哔哩视频搜索](https://api.317ak.com/detail/38) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·快手热门视频](https://api.317ak.com/detail/39) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·关爱你的女友](https://api.317ak.com/detail/40) | text | 停用 | msd → acl → mdays → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·超能力](https://api.317ak.com/detail/41) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·企鹅说说评论](https://api.317ak.com/detail/63) | text | 停用 | uin → skey → pskey → tid → qq → msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·企鹅分享卡片](https://api.317ak.com/detail/64) | text | 停用 | url → song → singer → cover → jump | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·查询QQ详细信息](https://api.317ak.com/detail/65) | text | 停用 | qq → uin → skey → pskey → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ个人信息](https://api.317ak.com/detail/66) | text | 停用 | qq → skey → pskey → qq2 → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ获取QID](https://api.317ak.com/detail/67) | text | 停用 | qq → skey → pskey → qq2 → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ群换头像](https://api.317ak.com/detail/68) | text | 停用 | qq → skey → url → group → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ聊天气泡切换](https://api.317ak.com/detail/69) | text | 停用 | qq → skey → pskey → id | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·获取企鹅群头像](https://api.317ak.com/detail/71) | text | 停用 | qun | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·获取企鹅头像](https://api.317ak.com/detail/72) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ一起听歌2.0](https://api.317ak.com/detail/73) | text | 停用 | uin → qh → skey → pskey → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·网页快照](https://api.317ak.com/detail/18) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·网站备案](https://api.317ak.com/detail/19) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·Punycode](https://api.317ak.com/detail/74) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·短网址生成](https://api.317ak.com/detail/75) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·主体查询备案](https://api.317ak.com/detail/76) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·IP地址查询2.0](https://api.317ak.com/detail/77) | text | 停用 | ip → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·IP详细地址](https://api.317ak.com/detail/78) | text | 停用 | ip → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·检测链接异常](https://api.317ak.com/detail/79) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·IP检测](https://api.317ak.com/detail/80) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·SSL证书信息](https://api.317ak.com/detail/81) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·聚合ping](https://api.317ak.com/detail/82) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·DNS域名污染检测](https://api.317ak.com/detail/83) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·域名whois查询](https://api.317ak.com/detail/84) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·网站信息](https://api.317ak.com/detail/85) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·网站备案2.0](https://api.317ak.com/detail/86) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·域名拦截查询](https://api.317ak.com/detail/87) | text | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·嘲讽语录](https://api.317ak.com/detail/42) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·晚安心语](https://api.317ak.com/detail/43) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·早安心语](https://api.317ak.com/detail/44) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·神回复语录](https://api.317ak.com/detail/45) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·绕口令语录](https://api.317ak.com/detail/46) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·脑筋急转弯](https://api.317ak.com/detail/47) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·顺口溜语录](https://api.317ak.com/detail/48) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·随机求签](https://api.317ak.com/detail/49) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·耽美小说](https://api.317ak.com/detail/50) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·巨人语录](https://api.317ak.com/detail/51) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·历史文案](https://api.317ak.com/detail/52) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·霸总语录](https://api.317ak.com/detail/53) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·社会语录](https://api.317ak.com/detail/54) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·诗词语录](https://api.317ak.com/detail/55) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·聚合语录](https://api.317ak.com/detail/56) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·舔狗日记语录](https://api.317ak.com/detail/57) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·毒鸡汤语录](https://api.317ak.com/detail/58) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·安慰语录](https://api.317ak.com/detail/59) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ签名语录](https://api.317ak.com/detail/60) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·KFC语录](https://api.317ak.com/detail/61) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·胡乱描述语录](https://api.317ak.com/detail/62) | text | 停用 | name | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·QQ图文](https://api.317ak.com/detail/70) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·堆糖搜图](https://api.317ak.com/detail/88) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·龙图](https://api.317ak.com/detail/89) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·坤坤图片](https://api.317ak.com/detail/90) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·壁纸搜索](https://api.317ak.com/detail/91) | text | 停用 | msg → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·4K壁纸专区(高质量)](https://api.317ak.com/detail/92) | text | 停用 | id → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·随机壁纸](https://api.317ak.com/detail/93) | text | 停用 | n → type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·动漫头像](https://api.317ak.com/detail/94) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·自拍图片](https://api.317ak.com/detail/95) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·诱惑图片](https://api.317ak.com/detail/96) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·举牌图片](https://api.317ak.com/detail/97) | text | 停用 | type | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·甘城图片](https://api.317ak.com/detail/98) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·动漫横图](https://api.317ak.com/detail/99) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·腹肌图片](https://api.317ak.com/detail/100) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·布布图片](https://api.317ak.com/detail/101) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·JK图片](https://api.317ak.com/detail/102) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·白丝图片](https://api.317ak.com/detail/103) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·美女图片](https://api.317ak.com/detail/104) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·动漫图片](https://api.317ak.com/detail/105) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·黑丝图片](https://api.317ak.com/detail/106) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·原神图片](https://api.317ak.com/detail/107) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·抖音主页解析](https://api.317ak.com/detail/108) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·聚合网盘解析](https://api.317ak.com/detail/109) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·最右视频解析](https://api.317ak.com/detail/110) | video | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·抖音合集解析](https://api.317ak.com/detail/111) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·微博短视频去水印](https://api.317ak.com/detail/112) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·哔哩短视频去水印](https://api.317ak.com/detail/113) | video | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·快手视频去水印](https://api.317ak.com/detail/114) | video | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·小红书去水印](https://api.317ak.com/detail/115) | text | 停用 | url | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·抖音视频去水印](https://api.317ak.com/detail/116) | video | 停用 | url → type | 需要站点密钥或登录凭据，配置后手动启用；网站目录或文档标记为维护、停用或状态未知 |
| [倾梦·坤坤语音](https://api.317ak.com/detail/117) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·原神KFC语音](https://api.317ak.com/detail/118) | text | 停用 | 无 | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·奖状生成器](https://api.317ak.com/detail/119) | text | 停用 | name | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·像话吗](https://api.317ak.com/detail/120) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·小画家](https://api.317ak.com/detail/121) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·淘汰](https://api.317ak.com/detail/122) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·炖](https://api.317ak.com/detail/123) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·嘲讽](https://api.317ak.com/detail/124) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·体温枪](https://api.317ak.com/detail/125) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·洗衣机](https://api.317ak.com/detail/126) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·为什么艾特我](https://api.317ak.com/detail/127) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·为什么要有手](https://api.317ak.com/detail/128) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·许愿失败](https://api.317ak.com/detail/129) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·致电她](https://api.317ak.com/detail/130) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·恐龙](https://api.317ak.com/detail/131) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·捂脸](https://api.317ak.com/detail/132) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·国庆头像](https://api.317ak.com/detail/133) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·天堂赦免令](https://api.317ak.com/detail/134) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·阿尼亚喜欢](https://api.317ak.com/detail/135) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·永远喜欢你](https://api.317ak.com/detail/136) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·毒瘾发作](https://api.317ak.com/detail/137) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·社会添乱](https://api.317ak.com/detail/138) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·跟我去二次元](https://api.317ak.com/detail/139) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·中国地图](https://api.317ak.com/detail/140) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·马冬梅表情](https://api.317ak.com/detail/141) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·小丑](https://api.317ak.com/detail/142) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·幽灵猎手](https://api.317ak.com/detail/143) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·随机头像框](https://api.317ak.com/detail/144) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·没这个](https://api.317ak.com/detail/145) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·抱着](https://api.317ak.com/detail/146) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·羡慕](https://api.317ak.com/detail/147) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·装高手](https://api.317ak.com/detail/148) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·想要它](https://api.317ak.com/detail/149) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·拍](https://api.317ak.com/detail/150) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·吃掉](https://api.317ak.com/detail/151) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·你可能需要它](https://api.317ak.com/detail/152) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·玩](https://api.317ak.com/detail/153) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·捣](https://api.317ak.com/detail/154) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·咬](https://api.317ak.com/detail/155) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·想看](https://api.317ak.com/detail/156) | text | 停用 | qq | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·棉花团子](https://api.317ak.com/detail/157) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·爱人爱己](https://api.317ak.com/detail/158) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
| [倾梦·超级幸福](https://api.317ak.com/detail/159) | text | 停用 | msg | 需要站点密钥或登录凭据，配置后手动启用 |
