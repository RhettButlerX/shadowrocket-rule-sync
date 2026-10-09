# Shadowrocket Top500 DIRECT Rules Sync

自动从 Johnshall 的 [Top500 白名单](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_top500_whitelist.conf) 中提取 `DIRECT` 规则，生成 Shadowrocket 可引用的独立规则文件。每天北京时间 10:17 检查更新。

该项目不覆盖 Shadowrocket 主配置，也不导入上游的代理节点策略。下载失败、解析失败或规则数异常时不覆盖上一版规则；内容有变化时才自动提交。

## 首次启动

1. 进入本仓库 **Settings → Actions → General → Workflow permissions**，确认 `GITHUB_TOKEN` 允许 **Read and write permissions**（如受组织策略限制，应调整策略）。
2. 进入 **Actions → Update Top500 DIRECT whitelist → Run workflow**。
3. 确认成功生成 `rules/top500-direct.list`。
4. 在 Shadowrocket 主配置的 `[Rule]` 下，自定义 YouTube、Claude、ChatGPT 分流规则之后，`FINAL,Remain` 之前添加：

```ini
RULE-SET,https://raw.githubusercontent.com/RhettButlerX/shadowrocket-rule-sync/main/rules/top500-direct.list,DIRECT
FINAL,Remain
```

这会保留原有专用服务分流，Top500 白名单直连，其余未匹配流量通过 `Remain` 代理。

## 广告拦截

在 Shadowrocket 中单独添加、启用 Johnshall 广告模块：

https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_ad_only.conf

不要继续使用 `shadowrocket://config/add/` 定时覆盖主配置，也不要保留指向整份 Johnshall 配置的 `update-url`。

## 注意

- 本项目只生成 Top500 的 DIRECT 规则；不会生成或应用原上游的 PROXY 规则，未命中白名单的流量由 `FINAL,Remain` 兜底。
- 更新频率取决于 GitHub Actions 实际调度，不保证精确到分钟。
- 在 iPhone 上需确认 Shadowrocket 成功刷新远程规则集缓存。
- `skip-proxy`、`bypass-tun` 以及系统服务仍可能独立绕过代理。

## 本地运行

```bash
python -m unittest discover -s tests -v
python scripts/update_rules.py
```
