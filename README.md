<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Requests in three API formats converge on one gateway and fan out to four providers." src="assets/banner-light.svg" width="100%">
</picture>

## LeenHawk

I build infrastructure for LLM APIs in Rust, and I port Rust desktop apps to OpenHarmony. Most of my time goes into gproxy. I also like compilers, hardware, and toolchains that build the same way every time.

用 Rust 写 LLM API 基础设施，也在把 Tauri 生态搬到鸿蒙上。

### Projects

| | |
| --- | --- |
| **[gproxy](https://github.com/LeenHawk/gproxy)** ![stars](https://img.shields.io/github/stars/LeenHawk/gproxy?style=flat&label=%E2%98%85&color=0b6e69) | LLM API gateway. Speaks the OpenAI, Claude and Gemini protocols and translates between them, with multi-provider routing, per-key quotas and rate limits, credential failover, usage auditing and a built-in admin console. Ships as a native binary, a Docker image and a WASM/edge build. |
| **[gproxy-protocol](https://github.com/LeenHawk/gproxy-protocol)** | gproxy's wire-format types and cross-protocol transforms, as a standalone crate. |
| **[sgproxy](https://github.com/LeenHawk/sgproxy)** ![stars](https://img.shields.io/github/stars/LeenHawk/sgproxy?style=flat&label=%E2%98%85&color=0b6e69) | A single-channel gproxy for Claude Code on Cloudflare Workers and Durable Objects. |
| **[tauri-harmony](https://github.com/LeenHawk/tauri-harmony)** | Reproducible Tauri build toolchain for OpenHarmony and HarmonyOS NEXT, published daily to GHCR. |
| **[pi-gproxy](https://github.com/LeenHawk/pi-gproxy)** · **[st-compress-cache](https://github.com/LeenHawk/st-compress-cache)** | Clients for gproxy: OAuth and model discovery for Pi, and context compression with prompt-cache breakpoints for SillyTavern. |

gproxy installs from a [Scoop bucket](https://github.com/LeenHawk/scoop-bucket) on Windows; winget packages are in review.

### Upstream

Bringing Tauri to OpenHarmony, one layer at a time:

- [tauri](https://github.com/tauri-apps/tauri/pull/16171), [wry](https://github.com/tauri-apps/wry/pull/1873), [tao](https://github.com/tauri-apps/tao/pull/1360), [cargo-mobile2](https://github.com/tauri-apps/cargo-mobile2/pull/529) and [plugins-workspace](https://github.com/tauri-apps/plugins-workspace/pull/3657): native plugin bridge, platform config, WebView init scripts and six mobile plugin backends (in review)
- [openharmony-ability](https://github.com/harmony-contrib/openharmony-ability/pull/85) and [ohos-native-bindings](https://github.com/ohos-rs/ohos-native-bindings/pull/167): WebView script ordering and async body buffers (merged)
- [TauriTavern](https://github.com/Darkatse/TauriTavern/pull/300): experimental OpenHarmony HAP support (merged)

Elsewhere:

- [UPX](https://github.com/upx/upx/pull/18965): x86_64 Android `so_fold` and an arm64 escape-hatch page (merged), plus [two](https://github.com/upx/upx/pull/18968) [more](https://github.com/upx/upx/pull/18970) in review
- [clewdr](https://github.com/Xerxes-2/clewdr/pulls?q=is%3Apr+author%3ALeenHawk+is%3Amerged): twelve merged PRs, including proxy hot reload and Claude beta-header passthrough
- [SeaORM](https://github.com/SeaQL/sea-orm/pull/3231): table-level index declarations on entities (in review)

### Stack

Rust (Axum, Tokio, SeaORM) · TypeScript · Python · C++ · Cloudflare Workers · OpenHarmony
