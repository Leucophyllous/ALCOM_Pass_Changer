# ALCOM / VCC Project Path Changer

[English](#english) | [日本語](#日本語)

A small GUI tool to **easily fix the project folder paths** registered in ALCOM / VRChat Creator Companion (VCC). The UI automatically switches between English and Japanese based on your system language.

ALCOM / VCC に登録された**プロジェクトのフォルダパスをGUIで簡単に変更できる**ツールです。UIはシステム言語に合わせて日本語/英語が自動で切り替わります。

---

## English

When you move a project folder to another drive or rename it, ALCOM / VCC can no longer open the project from its list. This tool lets you fix the paths just by picking the new folder — no manual editing of `settings.json` required.

**Works on Windows / macOS / Linux. Runs on the Python 3 standard library only — nothing extra to install.**

### Features

- 📋 Lists all registered projects (name / status / folder location)
- ❌ Projects whose folders are missing are highlighted in red
- 📁 Fix a path by selecting the project and picking its new folder (double-click works too)
- ➕ Add projects / ➖ remove entries from the list (folders themselves are never deleted)
- 💾 Automatically backs up `settings.json` (`.bak`) on every save
- ⚠ Warns before closing with unsaved changes
- 🔍 Warns if ALCOM / VCC is running (saving while it runs may get overwritten)
- 🧪 Sanity check: warns when the chosen folder has no `Assets` folder

### Requirements

| OS | Requirements |
|---|---|
| Windows | Python 3.10+ (without Python, the bundled PowerShell version is used automatically) |
| macOS | Python 3.10+ (the standard `python3` is fine) |
| Linux | Python 3.10+ and tkinter (e.g. `sudo apt install python3-tk`) |

### How to launch

| OS | How |
|---|---|
| Windows | Double-click `launch_windows.bat` |
| macOS | Double-click `launch_macos.command` (you may need `chmod +x launch_macos.command` once) |
| Linux | `./launch_linux.sh` or `python3 alcom_path_changer.py` |

### Usage (3 steps)

1. Click the project you want to fix in the list
2. Click **[📁 Change location]** and pick the folder where the project now lives
3. Click **[💾 Save]** — launch ALCOM / VCC and the project opens from its new location

> [!IMPORTANT]
> Close ALCOM / VCC before saving. If it is running, it may overwrite your changes when it exits (the tool also warns you about this on startup).

### What file does it edit?

Auto-detected per OS. ALCOM and VCC share the same settings file.

| OS | Path |
|---|---|
| Windows | `%LOCALAPPDATA%\VRChatCreatorCompanion\settings.json` |
| macOS | `~/Library/Application Support/VRChatCreatorCompanion/settings.json` |
| Linux | `~/.local/share/VRChatCreatorCompanion/settings.json` |

Only the `userProjects` list is modified. A timestamped backup is created next to the file on every save — if anything goes wrong, rename the `.bak` file back to `settings.json`.

### Files

```
alcom_path_changer.py   # Main tool (Python 3 / tkinter)
ALCOM_PathChanger.ps1   # Windows fallback (PowerShell / WinForms)
launch_windows.bat      # Windows launcher
launch_macos.command    # macOS launcher
launch_linux.sh         # Linux launcher
```

### Disclaimer

Unofficial tool. Not affiliated with VRChat Inc. or the ALCOM developers. Use at your own risk (automatic backups are created).

---

## 日本語

プロジェクトフォルダを別ドライブに移動したりフォルダ名を変えたりすると、ALCOM / VCC の一覧上でプロジェクトが開けなくなります。このツールを使えば、`settings.json` を手で編集しなくても、移動先のフォルダを選ぶだけでパスを直せます。

**Windows / macOS / Linux 対応。Python 3 標準ライブラリのみで動作し、追加インストールは不要です。**

### 機能

- 📋 登録済みプロジェクトの一覧表示(プロジェクト名 / 状態 / フォルダの場所)
- ❌ フォルダが見つからないプロジェクトを赤字で表示
- 📁 一覧から選んでフォルダを選び直すだけでパスを変更(行のダブルクリックでもOK)
- ➕ プロジェクトの追加 / ➖ 一覧からの登録解除(フォルダ自体は削除されません)
- 💾 保存時に `settings.json` のバックアップ(`.bak`)を自動作成
- ⚠ 未保存のまま閉じようとすると確認ダイアログを表示
- 🔍 ALCOM / VCC が起動中の場合は起動時に警告(起動中に保存すると変更が上書きされるため)
- 🧪 Assets フォルダが無い場所を選んだ場合は警告(Unityプロジェクトかどうかの簡易チェック)

### 動作環境

| OS | 必要なもの |
|---|---|
| Windows | Python 3.10+(無い場合は同梱のPowerShell版が自動で使われます) |
| macOS | Python 3.10+(標準の python3 でOK) |
| Linux | Python 3.10+ と tkinter(例: `sudo apt install python3-tk`) |

### 起動方法

| OS | 方法 |
|---|---|
| Windows | `launch_windows.bat` をダブルクリック |
| macOS | `launch_macos.command` をダブルクリック(初回は `chmod +x launch_macos.command` が必要な場合があります) |
| Linux | `./launch_linux.sh` または `python3 alcom_path_changer.py` |

### 使い方(3ステップ)

1. 一覧から変更したいプロジェクトをクリックして選ぶ
2. **[📁 場所を変更]** を押して、移動先のフォルダを選ぶ
3. **[💾 保存]** を押す → ALCOM / VCC を起動すると新しい場所で表示されます

> [!IMPORTANT]
> 保存する前に ALCOM / VCC を閉じてください。起動したまま保存すると、ALCOM / VCC の終了時に変更が上書きされることがあります(ツール起動時にも警告が出ます)。

### 編集対象のファイル

OSごとに自動判別します。ALCOM と VCC は同じ設定ファイルを使用しています。

| OS | パス |
|---|---|
| Windows | `%LOCALAPPDATA%\VRChatCreatorCompanion\settings.json` |
| macOS | `~/Library/Application Support/VRChatCreatorCompanion/settings.json` |
| Linux | `~/.local/share/VRChatCreatorCompanion/settings.json` |

このファイル内の `userProjects`(プロジェクト一覧)だけを書き換えます。保存のたびにタイムスタンプ付きバックアップが同じフォルダに作られるので、問題があれば `.bak` ファイルを `settings.json` に戻せば元どおりです。

### 免責

非公式ツールです。VRChat 及び ALCOM の開発元とは関係ありません。設定ファイルの書き換えは自己責任でお願いします(自動バックアップは作成されます)。

## License

[MIT License](LICENSE)
