Write-Host "Go to root folder of the repository..."
$root = git rev-parse --show-toplevel
cd $root

Write-Host "Check that the repo is clean..."
$status = git status --porcelain
if ($status) {
    Write-Host "This repository has uncommitted or untracked files."
    exit 1
}

Write-Host "Checkout addonTemplate branch..."
git checkout --quiet addonTemplate
git pull --quiet --ff-only

Write-Host "Remove all items except folders .git et tools..."
Get-ChildItem -Path $root -Exclude "tools",".git" | Remove-Item -Recurse -Force

Write-Host "Clone add-on template repo in tmp subfolder..."
git clone --quiet --depth 1 -b master https://github.com/nvdaaddons/AddonTemplate.git $root\tmp
$hash = git -C tmp rev-parse HEAD
$logEntry = git -C tmp log

Write-Host "Remove .git folder from add-on template repo..."
$tmpDir = Join-Path $root "tmp"
$dotGitDir = Join-Path $tmpDir ".git"
Remove-Item $dotGitDir -Recurse -Force

Write-Host "Copy files and folders from tmp to root folder..."
Get-ChildItem -Path $tmpDir | Move-Item -Destination $root

Write-Host "Remove tmp folder..."
# Check if tmp is empty
if ((Get-ChildItem $tmpDir).Count -ne 0) {
    Write-Host "tmp subfolder is not empty."
    exit 1
}
Remove-Item $tmpDir -Recurse -Force

Write-Host "Current folder updated to $hash."
Write-Host "=========="
Write-Output $logEntry
Write-Host "=========="
