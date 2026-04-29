# ULX Installer - Windows
# Versão: 3.0

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULX - Instalador v3.0 (Windows)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se é admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[✗] Execute como Administrador!" -ForegroundColor Red
    Write-Host "Clique direito > Executar como administrador"
    exit 1
}

Write-Host "[*] Verificando dependências..." -ForegroundColor Yellow

# Verifica Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[✗] Python 3 não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3 de: https://www.python.org/downloads/"
    exit 1
}

Write-Host "[✓] Python: $(python --version)" -ForegroundColor Green

# Verifica GCC (MinGW)
$gcc = Get-Command gcc -ErrorAction SilentlyContinue
if (-not $gcc) {
    Write-Host "[!] GCC não encontrado. Algumas funcionalidades podem não funcionar." -ForegroundColor Yellow
    Write-Host "Instale MinGW de: https://sourceforge.net/projects/mingw/"
}

# Diretório do script
$scriptDir = $PSScriptRoot

Write-Host ""
Write-Host "[1/4] Instalando ULX..." -ForegroundColor Yellow

# Copia scripts
Copy-Item "$scriptDir\compiler\clx_compiler.py" "$env:LOCALAPPDATA\Programs\ULX\" -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "$env:LOCALAPPDATA\Programs\ULX" -Force | Out-Null
Copy-Item "$scriptDir\compiler\clx_compiler.py" "$env:LOCALAPPDATA\Programs\ULX\ulx-compile.py" -Force
Copy-Item "$scriptDir\runtime\ulx_runner.py" "$env:LOCALAPPDATA\Programs\ULX\ulx-run.py" -Force
Copy-Item "$scriptDir\runtime\ulx_packager.py" "$env:LOCALAPPDATA\Programs\ULX\ulx-pack.py" -Force
Copy-Item "$scriptDir\runtime\ulx_init.py" "$env:LOCALAPPDATA\Programs\ULX\ulx-init.py" -Force

Write-Host "[✓] Scripts instalados em $env:LOCALAPPDATA\Programs\ULX\" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Criando atalhos..." -ForegroundColor Yellow

# Adiciona ao PATH (usuário)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$ulxPath = "$env:LOCALAPPDATA\Programs\ULX"
if ($userPath -notlike "*$ulxPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$ulxPath", "User")
    Write-Host "[✓] PATH atualizado" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/4] Registrando extensão .ulx..." -ForegroundColor Yellow

# Registra extensão
$ulxFile = "$env:LOCALAPPDATA\Programs\ULX\ulx-run.py"
$progId = "ULXFile"
$extension = ".ulx"

# Cria registro
Set-ItemProperty -Path "HKCU:\Software\Classes\$extension" -Name "(Default)" -Value $progId
New-Item -Path "HKCU:\Software\Classes\$progId" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Classes\$progId" -Name "(Default)" -Value "Aplicativo ULX"
New-Item -Path "HKCU:\Software\Classes\$progId\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Classes\$progId\shell\open\command" -Name "(Default)" -Value "python `"$ulxFile`" `"%1`""

Write-Host "[✓] Extensão .ulx registrada" -ForegroundColor Green

Write-Host ""
Write-Host "[4/4] Finalizando..." -ForegroundColor Yellow

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULX instalado com sucesso!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos disponíveis:"
Write-Host "  ulx-compile.py <arquivo.ulx>  - Compila para binário"
Write-Host "  ulx-run.py <app.ulx>          - Executa aplicativo"
Write-Host "  ulx-pack.py pack <bin>         - Empacota aplicativo"
Write-Host "  ulx-init.py <nome>             - Cria novo projeto"
Write-Host ""
Write-Host "Reinicie o terminal para usar os comandos."
Write-Host ""
