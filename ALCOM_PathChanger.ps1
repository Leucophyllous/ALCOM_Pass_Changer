# ALCOM / VCC Project Path Changer (Windows fallback, no Python required)
# Edits userProjects in %LOCALAPPDATA%\VRChatCreatorCompanion\settings.json via a GUI.
# UI language: Japanese on Japanese systems, English otherwise.

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

# ---------- Language ----------
$ja = (Get-UICulture).TwoLetterISOLanguageName -eq 'ja'
if ($ja) {
    $L = @{
        Title           = 'プロジェクトの場所 変更ツール (ALCOM / VCC)'
        Guide           = "使い方:  ① 下の一覧からプロジェクトを選ぶ → ② [場所を変更] で新しいフォルダを選ぶ → ③ [保存] を押す`n「❌ 見つかりません」の行は、フォルダが移動または削除されています。"
        ColName         = 'プロジェクト名'
        ColStatus       = '状態'
        ColPath         = 'フォルダの場所'
        Ok              = '✅ OK'
        Missing         = '❌ 見つかりません'
        BtnChange       = '📁 場所を変更'
        BtnAdd          = '＋ 追加'
        BtnRemove       = '－ 一覧から外す'
        BtnSave         = '💾 保存'
        StatusDirty     = '⚠ 変更があります。[保存] を押すまで反映されません。'
        StatusClean     = '変更はありません。'
        Info            = 'お知らせ'
        Confirm         = '確認'
        Warn            = '注意'
        Error           = 'エラー'
        Done            = '完了'
        PickTitle       = 'プロジェクトのフォルダ(中に Assets があるフォルダ)を選んでください'
        SelectFirst     = '先に一覧からプロジェクトをクリックして選んでください。'
        NoAssets        = "選んだフォルダの中に「Assets」フォルダがありません。`nUnityのプロジェクトフォルダではないかもしれません。`n`n選んだ場所: {0}`n`nこのまま設定しますか?"
        AlreadyListed   = 'そのフォルダは既に一覧にあります。'
        RemoveConfirm   = "この項目を一覧から外しますか?`n(フォルダやデータは削除されません。ALCOM / VCC に表示されなくなるだけです)`n`n{0}"
        Saved           = "保存しました! ✅`n`nALCOM / VCC を起動すると、新しい場所で表示されます。`n(元の設定はバックアップとして残してあります)"
        SaveFailed      = "保存できませんでした:`n{0}"
        Unsaved         = "まだ保存していない変更があります。`n保存せずに閉じると変更は消えます。`n`n閉じる前に保存しますか?"
        NoSettings      = "設定ファイルが見つかりませんでした。`nALCOM または VCC を一度起動したことがあるパソコンで使ってください。`n`n探した場所:`n{0}"
        VccRunning      = "ALCOM / VCC が起動中のようです。`n起動したまま保存すると、変更が消されることがあります。`n`n先に ALCOM / VCC を閉じることをおすすめします。`nこのまま続けますか?"
    }
} else {
    $L = @{
        Title           = 'Project Path Changer (ALCOM / VCC)'
        Guide           = "How to use:  1) Select a project below  →  2) Click [Change location] and pick the new folder  →  3) Click [Save]`nRows marked `"❌ Not found`" point to folders that were moved or deleted."
        ColName         = 'Project'
        ColStatus       = 'Status'
        ColPath         = 'Folder location'
        Ok              = '✅ OK'
        Missing         = '❌ Not found'
        BtnChange       = '📁 Change location'
        BtnAdd          = '＋ Add'
        BtnRemove       = '－ Remove from list'
        BtnSave         = '💾 Save'
        StatusDirty     = '⚠ You have unsaved changes. Click [Save] to apply them.'
        StatusClean     = 'No changes.'
        Info            = 'Info'
        Confirm         = 'Confirm'
        Warn            = 'Warning'
        Error           = 'Error'
        Done            = 'Done'
        PickTitle       = 'Select the project folder (the one containing an Assets folder)'
        SelectFirst     = 'Please click a project in the list first.'
        NoAssets        = "The selected folder does not contain an `"Assets`" folder,`nso it may not be a Unity project.`n`nSelected: {0}`n`nUse it anyway?"
        AlreadyListed   = 'That folder is already in the list.'
        RemoveConfirm   = "Remove this entry from the list?`n(The folder and its data are NOT deleted - it just disappears from ALCOM / VCC.)`n`n{0}"
        Saved           = "Saved! ✅`n`nLaunch ALCOM / VCC to see the projects at their new locations.`n(A backup of the previous settings was created.)"
        SaveFailed      = "Could not save:`n{0}"
        Unsaved         = "You have unsaved changes.`nClosing without saving will discard them.`n`nSave before closing?"
        NoSettings      = "The settings file was not found.`nUse this tool on a computer where ALCOM or VCC has been launched at least once.`n`nLooked in:`n{0}"
        VccRunning      = "ALCOM / VCC appears to be running.`nIf you save while it is running, your changes may be overwritten.`n`nWe recommend closing ALCOM / VCC first.`nContinue anyway?"
    }
}

$settingsPath = Join-Path $env:LOCALAPPDATA 'VRChatCreatorCompanion\settings.json'

if (-not (Test-Path $settingsPath)) {
    [System.Windows.Forms.MessageBox]::Show(($L.NoSettings -f $settingsPath), $L.Error, 'OK', 'Error') | Out-Null
    exit 1
}

$running = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^(ALCOM|alcom|CreatorCompanion|vrc-get-gui)$' }
if ($running) {
    $r = [System.Windows.Forms.MessageBox]::Show($L.VccRunning, $L.Warn, 'YesNo', 'Warning')
    if ($r -ne 'Yes') { exit 0 }
}

$json = Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
$projects = New-Object System.Collections.ArrayList
foreach ($p in @($json.userProjects)) { [void]$projects.Add([string]$p) }

$script:dirty = $false

# ---------- Form ----------
$font     = New-Object System.Drawing.Font('Meiryo UI', 11)
$fontBold = New-Object System.Drawing.Font('Meiryo UI', 11, [System.Drawing.FontStyle]::Bold)

$form = New-Object System.Windows.Forms.Form
$form.Text = $L.Title
$form.Size = New-Object System.Drawing.Size(900, 620)
$form.MinimumSize = New-Object System.Drawing.Size(700, 450)
$form.StartPosition = 'CenterScreen'
$form.Font = $font

$lblGuide = New-Object System.Windows.Forms.Label
$lblGuide.Text = $L.Guide
$lblGuide.Location = New-Object System.Drawing.Point(14, 12)
$lblGuide.Size = New-Object System.Drawing.Size(860, 52)
$lblGuide.Anchor = 'Top,Left,Right'
$form.Controls.Add($lblGuide)

$list = New-Object System.Windows.Forms.ListView
$list.View = 'Details'
$list.FullRowSelect = $true
$list.GridLines = $true
$list.MultiSelect = $false
$list.HideSelection = $false
$list.Location = New-Object System.Drawing.Point(14, 70)
$list.Size = New-Object System.Drawing.Size(858, 380)
$list.Anchor = 'Top,Bottom,Left,Right'
[void]$list.Columns.Add($L.ColName, 220)
[void]$list.Columns.Add($L.ColStatus, 150)
[void]$list.Columns.Add($L.ColPath, 460)
$form.Controls.Add($list)

function Refresh-List {
    $list.Items.Clear()
    foreach ($p in $projects) {
        $name = Split-Path $p -Leaf
        $item = New-Object System.Windows.Forms.ListViewItem($name)
        if (Test-Path $p) {
            [void]$item.SubItems.Add($L.Ok)
            $item.ForeColor = [System.Drawing.Color]::FromArgb(0, 110, 0)
        } else {
            [void]$item.SubItems.Add($L.Missing)
            $item.ForeColor = [System.Drawing.Color]::FromArgb(200, 0, 0)
        }
        [void]$item.SubItems.Add($p)
        [void]$list.Items.Add($item)
    }
    $lblStatus.Text = if ($script:dirty) { $L.StatusDirty } else { $L.StatusClean }
    $lblStatus.ForeColor = if ($script:dirty) { [System.Drawing.Color]::FromArgb(180, 90, 0) } else { [System.Drawing.Color]::Gray }
}

function Pick-Folder([string]$initial) {
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description = $L.PickTitle
    if ($initial -and (Test-Path $initial)) { $dlg.SelectedPath = $initial }
    if ($dlg.ShowDialog($form) -eq 'OK') { return $dlg.SelectedPath }
    return $null
}

function Change-Selected {
    if ($list.SelectedIndices.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show($L.SelectFirst, $L.Info, 'OK', 'Information') | Out-Null
        return
    }
    $i = $list.SelectedIndices[0]
    $newPath = Pick-Folder $projects[$i]
    if (-not $newPath) { return }
    if (-not (Test-Path (Join-Path $newPath 'Assets'))) {
        $r = [System.Windows.Forms.MessageBox]::Show(($L.NoAssets -f $newPath), $L.Confirm, 'YesNo', 'Warning')
        if ($r -ne 'Yes') { return }
    }
    $projects[$i] = $newPath
    $script:dirty = $true
    Refresh-List
    $list.Items[$i].Selected = $true
}

# ---------- Buttons ----------
function New-Button([string]$text, [int]$x, [int]$width) {
    $b = New-Object System.Windows.Forms.Button
    $b.Text = $text
    $b.Location = New-Object System.Drawing.Point($x, 465)
    $b.Size = New-Object System.Drawing.Size($width, 45)
    $b.Anchor = 'Bottom,Left'
    $form.Controls.Add($b)
    return $b
}

$btnChange = New-Button $L.BtnChange 14 190
$btnAdd    = New-Button $L.BtnAdd 214 120
$btnRemove = New-Button $L.BtnRemove 344 190
$btnSave   = New-Button $L.BtnSave 640 180
$btnSave.Font = $fontBold
$btnSave.BackColor = [System.Drawing.Color]::FromArgb(210, 235, 210)
$btnSave.Anchor = 'Bottom,Right'

$lblStatus = New-Object System.Windows.Forms.Label
$lblStatus.Location = New-Object System.Drawing.Point(14, 522)
$lblStatus.Size = New-Object System.Drawing.Size(860, 30)
$lblStatus.Anchor = 'Bottom,Left,Right'
$form.Controls.Add($lblStatus)

$btnChange.Add_Click({ Change-Selected })
$list.Add_DoubleClick({ Change-Selected })

$btnAdd.Add_Click({
    $newPath = Pick-Folder $null
    if (-not $newPath) { return }
    if ($projects -contains $newPath) {
        [System.Windows.Forms.MessageBox]::Show($L.AlreadyListed, $L.Info, 'OK', 'Information') | Out-Null
        return
    }
    [void]$projects.Add($newPath)
    $script:dirty = $true
    Refresh-List
})

$btnRemove.Add_Click({
    if ($list.SelectedIndices.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show($L.SelectFirst, $L.Info, 'OK', 'Information') | Out-Null
        return
    }
    $i = $list.SelectedIndices[0]
    $r = [System.Windows.Forms.MessageBox]::Show(($L.RemoveConfirm -f $projects[$i]), $L.Confirm, 'YesNo', 'Question')
    if ($r -eq 'Yes') {
        $projects.RemoveAt($i)
        $script:dirty = $true
        Refresh-List
    }
})

$btnSave.Add_Click({
    try {
        $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
        Copy-Item $settingsPath "$settingsPath.$stamp.bak"

        $json.userProjects = [string[]]$projects.ToArray()
        $text = $json | ConvertTo-Json -Depth 20
        [System.IO.File]::WriteAllText($settingsPath, $text, (New-Object System.Text.UTF8Encoding($false)))

        $script:dirty = $false
        Refresh-List
        [System.Windows.Forms.MessageBox]::Show($L.Saved, $L.Done, 'OK', 'Information') | Out-Null
    } catch {
        [System.Windows.Forms.MessageBox]::Show(($L.SaveFailed -f $_.Exception.Message), $L.Error, 'OK', 'Error') | Out-Null
    }
})

$form.Add_FormClosing({
    param($sender, $e)
    if ($script:dirty) {
        $r = [System.Windows.Forms.MessageBox]::Show($L.Unsaved, $L.Confirm, 'YesNoCancel', 'Warning')
        if ($r -eq 'Yes') { $btnSave.PerformClick(); if ($script:dirty) { $e.Cancel = $true } }
        elseif ($r -eq 'Cancel') { $e.Cancel = $true }
    }
})

Refresh-List
[void]$form.ShowDialog()
