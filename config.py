from pathlib import Path

from maibot_sdk import Field, PluginConfigBase


class PluginSettings(PluginConfigBase):
    __ui_label__ = "基础设置"
    enabled: bool = Field(default=True, description="启用或停用 API 聚合插件", json_schema_extra={"label": "启用插件"})
    config_version: str = Field(default="1.0.0", description="配置格式版本，由插件维护", json_schema_extra={"label": "配置版本", "disabled": True})


class TriggerSettings(PluginConfigBase):
    __ui_label__ = "触发与权限"
    need_prefix: bool = Field(default=True, description="开启后需以 / 开头或 @机器人才能触发；关闭后直接用关键词触发", json_schema_extra={"label": "需要前缀或提及机器人"})
    admin_users: list[str] = Field(default_factory=list, description="填写插件管理员 QQ 号；接口使用范围设为 admin 时，仅允许这些用户调用", json_schema_extra={"label": "插件管理员"})
    consume_message: bool = Field(default=True, description="触发 API 后停止麦麦的普通聊天处理，避免重复回复", json_schema_extra={"label": "触发后停止普通聊天"})
    cooldown_seconds: float = Field(default=2, ge=0, le=300, description="同一用户在同一聊天两次触发之间的最短间隔，填 0 可关闭冷却", json_schema_extra={"label": "触发冷却时间（秒）"})
    max_concurrent: int = Field(default=4, ge=1, le=16, description="允许同时执行的 API 请求数量，范围为 1 至 16", json_schema_extra={"label": "最大并发请求数"})


class DataSettings(PluginConfigBase):
    __ui_label__ = "数据与缓存"
    save_data: bool = Field(default=True, description="保留新的请求结果作为本地缓存，关闭后仍保留已有缓存", json_schema_extra={"label": "保存响应数据"})
    use_local: bool = Field(default=True, description="API 请求失败时，从该接口已有缓存中随机取一条结果", json_schema_extra={"label": "失败时使用本地缓存"})
    max_media_mb: int = Field(default=8, ge=1, le=11, description="单个 API 响应及待发送媒体的大小上限，范围为 1 至 11 MiB", json_schema_extra={"label": "响应与媒体大小上限（MiB）"})


class ApisConfig(PluginConfigBase):
    plugin: PluginSettings = Field(default_factory=PluginSettings)
    trigger: TriggerSettings = Field(default_factory=TriggerSettings)
    data: DataSettings = Field(default_factory=DataSettings)


class PluginConfig:
    """Framework-neutral paths and settings consumed by the upstream core."""

    def __init__(self, config: ApisConfig, paths):
        self.plugin_dir = Path(__file__).resolve().parent
        self.data_dir = Path(paths.data_dir)
        self.runtime_dir = Path(paths.runtime_dir)
        self.local_dir = self.data_dir / "local"
        self.pool_files_dir = self.data_dir / "pool_files"
        self.presets_dir = self.plugin_dir / "presets"
        self.site_pool_file = self.presets_dir / "site_pool_default.json"
        self.api_pool_file = self.presets_dir / "api_pool_default.json"
        self.dashboard_dir = self.plugin_dir / "pages/dashboard"
        self.dashboard_assets_dir = self.dashboard_dir / "assets"
        self.logo_path = self.dashboard_assets_dir / "images/logo.png"
        self.save_data = config.data.save_data
        self.use_local = config.data.use_local
        self.max_response_bytes = config.data.max_media_mb * 1024 * 1024
        for path in (self.data_dir, self.runtime_dir, self.local_dir, self.pool_files_dir):
            path.mkdir(parents=True, exist_ok=True)
