# 📜 Changelog

All notable changes to **Tech Master AI** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2025-01-15

### 🎉 Initial Release

#### Added
- ✨ Neon truecolor gradient banner
- ✨ Rounded AI answer boxes
- ✨ 4 fullscreen 3D ASCII animations:
  - 🍩 Donut (spinning torus with lighting)
  - 🧊 Rotating 3D Cube
  - 🟢 Matrix Digital Rain
  - 🌈 Plasma Field
- ✨ Interactive AI chat with session history
- ✨ Animated spinner with latency display
- ✨ Splash loader with progress bar
- ✨ Slash command system:
  - `/help`, `/anim`, `/clear`, `/banner`
  - `/about`, `/api`, `/history`, `/save`
  - `/quit`, `/exit`
- ✨ One-shot mode (`-q "question"`)
- ✨ Animation-only mode (`--anim donut|cube|matrix|plasma|all`)
- ✨ API error handling (network / JSON / status)
- ✨ Terminal size auto-detect
- ✨ East-Asian width aware text wrapping
- ✨ Zero external dependencies (pure stdlib)
- ✨ Custom API endpoint support (`--api URL`)

#### Platform Support
- ✅ Termux (Android)
- ✅ Linux
- ✅ macOS
- ✅ WSL (Windows Subsystem for Linux)

---

## 🔮 Planned

- [ ] Voice input via `termux-speech-to-text`
- [ ] Multi-line input mode
- [ ] Theme switching (`--theme neon|cyberpunk|retro`)
- [ ] Plugin system
- [ ] Config file (`~/.techmaster-ai.json`)
- [ ] Conversation context memory
- [ ] File attachment support
- [ ] OpenAI / Gemini / Claude backend adapters
