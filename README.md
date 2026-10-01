<h1 align="center">🚀 Tech Master AI — Termux AI Agent (3D Edition)</h1>

<p align="center">
  <b>Neon terminal • 3D ASCII animations • Deep AI powered • Single-file</b><br/>
  Developer: <a href="https://t.me/tech_master_a2z">Tech Master</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.6%2B-blue?style=for-the-badge&logo=python">
  <img alt="Platform" src="https://img.shields.io/badge/platform-termux%20%7C%20linux%20%7C%20macos-black?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-orange?style=for-the-badge">
</p>

---

## ✨ Features

- 🎨 **Truecolor neon UI** — gradient banner, rounded boxes, colored prompt
- 🍩 **4 fullscreen 3D animations** — Donut, Cube, Matrix Rain, Plasma
- 💬 **Interactive AI chat** — session history, animated spinner, latency display
- ⚡ **Deep AI API** — `deep-ai-api-by-tech-master.vercel.app`
- 🐍 **Zero external dependencies** — pure Python standard library
- 📱 **Termux-optimized** — runs on Android without root
- 🖥️ **Also works on Linux / macOS / WSL**
- 🧩 **Command system** — `/help`, `/anim`, `/clear`, `/history`, `/save`, `/about`, `/api`
- 💾 **Session save** — export chat history to file
- 🌏 **Unicode-aware** — Bengali / emoji / box chars align properly

---

## 📸 Preview

```
 ████████╗███████╗ ██████╗██╗  ██╗    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗
 ╚══██╔══╝██╔════╝██╔════╝██║  ██║    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║   █████╗  ██║     ███████║    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║   ██╔══╝  ██║     ██╔══██║    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║   ███████╗╚██████╗██║  ██║    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

           Termux AI Agent  •  3D Edition  •  Deep AI Powered
        Developer: Tech Master  •  t.me/tech_master_a2z
════════════════════════════════════════════════════════════════════════════════
  Type /help for commands  •  Ctrl+C to exit
════════════════════════════════════════════════════════════════════════════════

❯ You › hello AI

  ⏱  1.42s
╭─ AI  •  Tech Master ────────────────────────────────────────────────────────╮
│ Hey — great to see you. I can answer questions, help write or edit text,   │
│ brainstorm ideas, plan something, debug code, or just chat. What would     │
│ you like to do today?                                                      │
╰────────────────────────────────────────────────────────────────────────────╯
```

---

## 📦 Installation

### 🔹 Option 1 — Termux (Android)

```bash
pkg update -y && pkg install -y python
git clone https://github.com/YOUR_USERNAME/techmaster-ai.git
cd techmaster-ai
python main.py
```

### 🔹 Option 2 — Linux / macOS / WSL

```bash
git clone https://github.com/YOUR_USERNAME/techmaster-ai.git
cd techmaster-ai
python3 main.py
```

> Python 3.6+ required. No external packages needed.

---

## 🎮 Usage

### Interactive mode

```bash
python main.py
```

### One-shot question

```bash
python main.py -q "explain quantum computing in simple words"
```

### Play a 3D animation directly

```bash
python main.py --anim donut
python main.py --anim cube
python main.py --anim matrix
python main.py --anim plasma
python main.py --anim all
```

### Skip splash / disable animations

```bash
python main.py --no-splash
python main.py --no-anim
```

### Custom API endpoint

```bash
python main.py --api "https://your-endpoint.example/api"
```

---

## 🎛️ Slash Commands (inside the app)

| Command | কাজ |
|---------|------|
| `/help` | সব কমান্ড দেখাবে |
| `/anim donut` | 🍩 Donut 3D animation |
| `/anim cube` | 🧊 Rotating 3D cube |
| `/anim matrix` | 🟢 Matrix rain |
| `/anim plasma` | 🌈 Plasma field |
| `/anim all` | সব animation একসাথে |
| `/clear` | স্ক্রিন clear করবে |
| `/banner` | Banner আবার দেখাবে |
| `/about` | Tool সম্পর্কে তথ্য |
| `/api` | API endpoint দেখাবে |
| `/history` | Session history |
| `/save chat.txt` | History file-এ save |
| `/quit` `/exit` | App থেকে exit |

---

## 🔌 API Info

```
GET https://deep-ai-api-by-tech-master.vercel.app/api/deep-ai?query=your+question+here
```

Response:

```json
{
  "status": true,
  "creator": "Tech Master",
  "results": "Your AI answer here..."
}
```

---

## 🐙 GitHub-এ আপলোড করার নিয়ম

### 1️⃣ GitHub repo তৈরি করো

1. https://github.com/new এ যাও
2. **Repository name**: `techmaster-ai`
3. **Public** সিলেক্ট করো
4. **Create repository** চাপো (README টিক দিও না)

### 2️⃣ Termux / Linux-এ Git সেটআপ

```bash
pkg install -y git            # Termux
git config --global user.name "Tech Master"
git config --global user.email "you@example.com"
```

### 3️⃣ Project ফাইল বানাও

```
techmaster-ai/
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── CHANGELOG.md
```

### 4️⃣ Test করো

```bash
python main.py --no-splash
python main.py --anim donut
python main.py -q "hello"
```

### 5️⃣ Git initialize + commit

```bash
cd techmaster-ai
git init
git branch -M main
git add .
git commit -m "🚀 Initial release: Tech Master AI v1.0.0"
```

### 6️⃣ GitHub-এ push করো

```bash
git remote add origin https://github.com/YOUR_USERNAME/techmaster-ai.git
git push -u origin main
```

### 7️⃣ Personal Access Token

GitHub এখন password accept করে না। এভাবে token বানাও:

1. GitHub → Settings → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)** → scope: `repo`
4. Token copy করে password হিসেবে paste করো

### 8️⃣ পরের বার update

```bash
git add .
git commit -m "✨ new feature"
git push
```

---

## 🛠️ Troubleshooting

| সমস্যা | সমাধান |
|--------|--------|
| `Permission denied` | `chmod +x main.py` |
| Unicode error / box ভাঙা | Termux-এ `pkg install termux-styling` দিয়ে Nerd Font সেট করো |
| Colors দেখা যাচ্ছে না | Termux → `settings` → `Colors` → `Default` |
| API timeout | `python main.py -q "hi"` দিয়ে নেট চেক করো |
| Animation slow | `--no-anim` flag দাও |
| `python: command not found` | `pkg install python` দাও |

---

## 🎨 Customization

- **API URL** → `main.py` এর `API_URL` variable
- **Colors** → `NEON_PALETTE` list
- **Animation duration** → `play_animation()` এর ভেতরে
- **নতুন animation** → `anim_*` ফাংশন লেখো, `play_animation`-এ case add করো

---

## 📜 License

MIT — দেখো [LICENSE](LICENSE)

---

## 💚 Credits

- **Developer:** [Tech Master](https://t.me/tech_master_a2z)
- **API:** Deep AI by Tech Master
- **Inspired by:** `donut.c` by Andy Sloane

<p align="center"><b>⭐ যদি ভালো লাগে, GitHub-এ star দিও!</b></p>
