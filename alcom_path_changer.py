#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALCOM / VCC Project Path Changer (Windows / macOS / Linux)

Edits the userProjects list in the ALCOM / VCC settings.json via a GUI.
Runs on the Python 3 standard library (tkinter) only — no extra installs.

ALCOM / VCC の settings.json 内の userProjects を GUI で編集します。
Python 3 標準ライブラリ (tkinter) のみで動作し、追加インストールは不要です。
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# ---------- 言語 / Language ----------
def detect_lang() -> str:
    """Return 'ja' on Japanese systems, otherwise 'en'."""
    env = os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
    if env.lower().startswith("ja"):
        return "ja"
    try:
        import locale
        loc = (locale.getlocale()[0] or "").lower()
        if "ja" in loc or "japan" in loc:
            return "ja"
    except Exception:
        pass
    if platform.system() == "Windows":
        try:
            import ctypes
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0xFF == 0x11:
                return "ja"
        except Exception:
            pass
    return "en"


STRINGS = {
    "ja": {
        "title": "プロジェクトの場所 変更ツール (ALCOM / VCC)",
        "guide": (
            "使い方:  ① 下の一覧からプロジェクトを選ぶ → ② [場所を変更] で新しいフォルダを選ぶ → ③ [保存] を押す\n"
            "「❌ 見つかりません」の行は、フォルダが移動または削除されています。"
        ),
        "col_name": "プロジェクト名",
        "col_status": "状態",
        "col_path": "フォルダの場所",
        "ok": "✅ OK",
        "missing": "❌ 見つかりません",
        "btn_change": "📁 場所を変更",
        "btn_add": "＋ 追加",
        "btn_remove": "－ 一覧から外す",
        "btn_save": "💾 保存",
        "status_dirty": "⚠ 変更があります。[保存] を押すまで反映されません。",
        "status_clean": "変更はありません。",
        "info": "お知らせ",
        "confirm": "確認",
        "warn": "注意",
        "error": "エラー",
        "done": "完了",
        "pick_title": "プロジェクトのフォルダ(中に Assets があるフォルダ)を選んでください",
        "select_first_change": "先に一覧から変更したいプロジェクトをクリックして選んでください。",
        "select_first_remove": "先に一覧から外したいプロジェクトをクリックして選んでください。",
        "no_assets": (
            "選んだフォルダの中に「Assets」フォルダがありません。\n"
            "Unityのプロジェクトフォルダではないかもしれません。\n\n"
            "選んだ場所: {path}\n\nこのまま設定しますか?"
        ),
        "already_listed": "そのフォルダは既に一覧にあります。",
        "remove_confirm": (
            "この項目を一覧から外しますか?\n"
            "(フォルダやデータは削除されません。ALCOM / VCC に表示されなくなるだけです)\n\n{path}"
        ),
        "saved": (
            "保存しました! ✅\n\nALCOM / VCC を起動すると、新しい場所で表示されます。\n"
            "(元の設定はバックアップとして残してあります)"
        ),
        "save_failed": "保存できませんでした:\n{err}",
        "unsaved": (
            "まだ保存していない変更があります。\n保存せずに閉じると変更は消えます。\n\n閉じる前に保存しますか?"
        ),
        "no_settings": (
            "設定ファイルが見つかりませんでした。\n"
            "ALCOM または VCC を一度起動したことがあるパソコンで使ってください。\n\n"
            "探した場所:\n{path}"
        ),
        "vcc_running": (
            "ALCOM / VCC が起動中のようです。\n"
            "起動したまま保存すると、変更が消されることがあります。\n\n"
            "先に ALCOM / VCC を閉じることをおすすめします。\nこのまま続けますか?"
        ),
    },
    "en": {
        "title": "Project Path Changer (ALCOM / VCC)",
        "guide": (
            "How to use:  1) Select a project below  →  2) Click [Change location] and pick the new folder  →  3) Click [Save]\n"
            "Rows marked \"❌ Not found\" point to folders that were moved or deleted."
        ),
        "col_name": "Project",
        "col_status": "Status",
        "col_path": "Folder location",
        "ok": "✅ OK",
        "missing": "❌ Not found",
        "btn_change": "📁 Change location",
        "btn_add": "＋ Add",
        "btn_remove": "－ Remove from list",
        "btn_save": "💾 Save",
        "status_dirty": "⚠ You have unsaved changes. Click [Save] to apply them.",
        "status_clean": "No changes.",
        "info": "Info",
        "confirm": "Confirm",
        "warn": "Warning",
        "error": "Error",
        "done": "Done",
        "pick_title": "Select the project folder (the one containing an Assets folder)",
        "select_first_change": "Please click a project in the list first.",
        "select_first_remove": "Please click a project in the list first.",
        "no_assets": (
            "The selected folder does not contain an \"Assets\" folder,\n"
            "so it may not be a Unity project.\n\n"
            "Selected: {path}\n\nUse it anyway?"
        ),
        "already_listed": "That folder is already in the list.",
        "remove_confirm": (
            "Remove this entry from the list?\n"
            "(The folder and its data are NOT deleted — it just disappears from ALCOM / VCC.)\n\n{path}"
        ),
        "saved": (
            "Saved! ✅\n\nLaunch ALCOM / VCC to see the projects at their new locations.\n"
            "(A backup of the previous settings was created.)"
        ),
        "save_failed": "Could not save:\n{err}",
        "unsaved": (
            "You have unsaved changes.\nClosing without saving will discard them.\n\nSave before closing?"
        ),
        "no_settings": (
            "The settings file was not found.\n"
            "Use this tool on a computer where ALCOM or VCC has been launched at least once.\n\n"
            "Looked in:\n{path}"
        ),
        "vcc_running": (
            "ALCOM / VCC appears to be running.\n"
            "If you save while it is running, your changes may be overwritten.\n\n"
            "We recommend closing ALCOM / VCC first.\nContinue anyway?"
        ),
    },
}

L = STRINGS[detect_lang()]


def settings_path() -> Path:
    """Per-OS location of settings.json (shared by VCC / ALCOM / vrc-get)."""
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux and others
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "VRChatCreatorCompanion" / "settings.json"


def vcc_running() -> bool:
    """Best-effort check whether ALCOM / VCC is running (False on failure)."""
    names = ("ALCOM", "alcom", "CreatorCompanion", "vrc-get-gui")
    try:
        if platform.system() == "Windows":
            out = subprocess.run(
                ["tasklist"], capture_output=True, text=True, timeout=5
            ).stdout
        else:
            out = subprocess.run(
                ["ps", "-A", "-o", "comm"], capture_output=True, text=True, timeout=5
            ).stdout
        return any(n in out for n in names)
    except Exception:
        return False


class App:
    def __init__(self, root: tk.Tk, path: Path):
        self.root = root
        self.path = path
        self.dirty = False

        with open(path, encoding="utf-8") as f:
            self.settings = json.load(f)
        self.projects: list[str] = [str(p) for p in self.settings.get("userProjects", [])]

        self.build_ui()
        self.refresh()

    # ---------- UI ----------
    def build_ui(self):
        self.root.title(L["title"])
        self.root.geometry("900x600")
        self.root.minsize(700, 450)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        default_font = ("", 12)

        guide = tk.Label(self.root, justify="left", anchor="w",
                         font=default_font, text=L["guide"])
        guide.pack(fill="x", padx=12, pady=(10, 6))

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=12)

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=default_font)
        style.configure("Treeview.Heading", font=default_font)

        self.tree = ttk.Treeview(
            frame, columns=("status", "path"), show="tree headings", selectmode="browse"
        )
        self.tree.heading("#0", text=L["col_name"])
        self.tree.heading("status", text=L["col_status"])
        self.tree.heading("path", text=L["col_path"])
        self.tree.column("#0", width=220, anchor="w")
        self.tree.column("status", width=150, anchor="w")
        self.tree.column("path", width=460, anchor="w")
        self.tree.tag_configure("ok", foreground="#006e00")
        self.tree.tag_configure("missing", foreground="#c80000")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self.change_selected())

        btns = tk.Frame(self.root)
        btns.pack(fill="x", padx=12, pady=8)

        tk.Button(btns, text=L["btn_change"], font=default_font, height=2, width=18,
                  command=self.change_selected).pack(side="left", padx=(0, 10))
        tk.Button(btns, text=L["btn_add"], font=default_font, height=2, width=10,
                  command=self.add_project).pack(side="left", padx=(0, 10))
        tk.Button(btns, text=L["btn_remove"], font=default_font, height=2, width=18,
                  command=self.remove_selected).pack(side="left")
        tk.Button(btns, text=L["btn_save"], font=(default_font[0], 12, "bold"),
                  height=2, width=16, bg="#d2ebd2",
                  command=self.save).pack(side="right")

        self.status = tk.Label(self.root, anchor="w", font=default_font)
        self.status.pack(fill="x", padx=12, pady=(0, 10))

    # ---------- Refresh ----------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for i, p in enumerate(self.projects):
            name = Path(p).name or p
            if Path(p).is_dir():
                status, tag = L["ok"], "ok"
            else:
                status, tag = L["missing"], "missing"
            self.tree.insert("", "end", iid=str(i), text=name,
                             values=(status, p), tags=(tag,))
        if self.dirty:
            self.status.config(text=L["status_dirty"], fg="#b45a00")
        else:
            self.status.config(text=L["status_clean"], fg="gray")

    def selected_index(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    # ---------- Actions ----------
    def pick_folder(self, initial: str | None) -> str | None:
        initdir = initial if initial and Path(initial).is_dir() else str(Path.home())
        chosen = filedialog.askdirectory(
            parent=self.root, initialdir=initdir, title=L["pick_title"],
        )
        return os.path.normpath(chosen) if chosen else None

    def change_selected(self):
        i = self.selected_index()
        if i is None:
            messagebox.showinfo(L["info"], L["select_first_change"], parent=self.root)
            return
        new_path = self.pick_folder(self.projects[i])
        if not new_path:
            return
        if not (Path(new_path) / "Assets").is_dir():
            if not messagebox.askyesno(
                L["confirm"], L["no_assets"].format(path=new_path),
                icon="warning", parent=self.root,
            ):
                return
        self.projects[i] = new_path
        self.dirty = True
        self.refresh()
        self.tree.selection_set(str(i))

    def add_project(self):
        new_path = self.pick_folder(None)
        if not new_path:
            return
        if new_path in self.projects:
            messagebox.showinfo(L["info"], L["already_listed"], parent=self.root)
            return
        self.projects.append(new_path)
        self.dirty = True
        self.refresh()

    def remove_selected(self):
        i = self.selected_index()
        if i is None:
            messagebox.showinfo(L["info"], L["select_first_remove"], parent=self.root)
            return
        if messagebox.askyesno(
            L["confirm"], L["remove_confirm"].format(path=self.projects[i]),
            parent=self.root,
        ):
            del self.projects[i]
            self.dirty = True
            self.refresh()

    def save(self):
        try:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(self.path, self.path.with_name(f"{self.path.name}.{stamp}.bak"))

            self.settings["userProjects"] = self.projects
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)

            self.dirty = False
            self.refresh()
            messagebox.showinfo(L["done"], L["saved"], parent=self.root)
        except Exception as e:
            messagebox.showerror(L["error"], L["save_failed"].format(err=e), parent=self.root)

    def on_close(self):
        if self.dirty:
            r = messagebox.askyesnocancel(
                L["confirm"], L["unsaved"], icon="warning", parent=self.root,
            )
            if r is None:
                return
            if r:
                self.save()
                if self.dirty:  # do not close if saving failed
                    return
        self.root.destroy()


def main():
    path = settings_path()

    root = tk.Tk()
    root.withdraw()  # hide the main window while dialogs are shown

    if not path.is_file():
        messagebox.showerror(L["error"], L["no_settings"].format(path=path))
        sys.exit(1)

    if vcc_running():
        if not messagebox.askyesno(L["warn"], L["vcc_running"], icon="warning"):
            sys.exit(0)

    App(root, path)
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
