<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Requests in three API formats converge on one gateway and fan out to four providers." src="assets/banner-light.svg" width="100%">
</picture>

## Hi, I'm LeenHawk

I write Rust, mostly the plumbing that sits between apps and LLM APIs. [gproxy](https://github.com/LeenHawk/gproxy) is the big one: one gateway that speaks OpenAI, Claude and Gemini and translates between them.

Lately I've also been porting Tauri to OpenHarmony, which means a lot of time inside WebView init scripts and half-working build toolchains. If something annoys me twice, I usually end up writing a tool for it.

平时写 Rust，主要做 LLM API 网关；最近在把 Tauri 搬到鸿蒙上。欢迎提 issue，中英文都行。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img alt="GitHub stats: stars earned, commits, pull requests, merged upstream PRs, contribution streak and top languages." src="assets/stats-light.svg" width="100%">
</picture>

### What I'm working on

- Keeping gproxy current as providers ship new APIs and auth flows
- Getting the Tauri OpenHarmony patches through review upstream
- Making the Tauri-for-HarmonyOS toolchain build the same way every day ([tauri-harmony](https://github.com/LeenHawk/tauri-harmony))

### Things I made

- **[gproxy](https://github.com/LeenHawk/gproxy)** ![stars](https://img.shields.io/github/stars/LeenHawk/gproxy?style=flat&label=%E2%98%85&color=0b6e69)  
  The LLM gateway. Multi-provider routing, per-key quotas and rate limits, credential failover, usage auditing and an admin console. Runs as a binary, in Docker, or on the edge as WASM. Windows users can grab it from my [Scoop bucket](https://github.com/LeenHawk/scoop-bucket).
- **[sgproxy](https://github.com/LeenHawk/sgproxy)** ![stars](https://img.shields.io/github/stars/LeenHawk/sgproxy?style=flat&label=%E2%98%85&color=0b6e69)  
  gproxy cut down to one job: Claude Code credentials on Cloudflare Workers.
- **[gproxy-protocol](https://github.com/LeenHawk/gproxy-protocol)**  
  The wire formats and cross-protocol transforms from gproxy, as their own crate.
- **[pi-gproxy](https://github.com/LeenHawk/pi-gproxy)** and **[st-compress-cache](https://github.com/LeenHawk/st-compress-cache)**  
  gproxy clients: login and model discovery for the Pi coding agent, and context compression with prompt-cache breakpoints for SillyTavern.

### Code I've sent upstream

Tauri on OpenHarmony, one layer at a time:

- [tauri](https://github.com/tauri-apps/tauri/pull/16171), [wry](https://github.com/tauri-apps/wry/pull/1873), [tao](https://github.com/tauri-apps/tao/pull/1360), [cargo-mobile2](https://github.com/tauri-apps/cargo-mobile2/pull/529) and [plugins-workspace](https://github.com/tauri-apps/plugins-workspace/pull/3657): native plugin bridge, platform config, WebView init scripts and six mobile plugin backends (in review)
- [openharmony-ability](https://github.com/harmony-contrib/openharmony-ability/pull/85) and [ohos-native-bindings](https://github.com/ohos-rs/ohos-native-bindings/pull/167): WebView script ordering and async body buffers (merged)
- [TauriTavern](https://github.com/Darkatse/TauriTavern/pull/300): experimental OpenHarmony HAP support (merged)

And elsewhere:

- [UPX](https://github.com/upx/upx/pull/18965): x86_64 Android `so_fold` and an arm64 escape-hatch page (merged), plus [two](https://github.com/upx/upx/pull/18968) [more](https://github.com/upx/upx/pull/18970) in review
- [clewdr](https://github.com/Xerxes-2/clewdr/pulls?q=is%3Apr+author%3ALeenHawk+is%3Amerged): twelve merged PRs, including proxy hot reload and Claude beta-header passthrough
- [SeaORM](https://github.com/SeaQL/sea-orm/pull/3231): table-level index declarations on entities (in review)

### Ask me about

Async Rust services (Axum, Tokio, SeaORM), LLM API protocols and prompt caching, Cloudflare Workers, getting Rust apps to build for HarmonyOS NEXT, and compilers.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/LeenHawk/LeenHawk/output/snake-dark.svg">
  <img alt="A snake eating the contribution graph." src="https://raw.githubusercontent.com/LeenHawk/LeenHawk/output/snake-light.svg" width="100%">
</picture>
