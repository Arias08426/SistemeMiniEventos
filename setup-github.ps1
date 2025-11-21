# Script de inicializacion de Git y GitHub
# Uso: .\setup-github.ps1 -GithubUsername "TU_USUARIO"

param(
    [Parameter(Mandatory=$true)]
    [string]$GithubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "SistemeMiniEventos",
    
    [Parameter(Mandatory=$false)]
    [string]$Branch = "main"
)

Write-Host "[+] Iniciando configuracion de Git y GitHub..." -ForegroundColor Green

# Verificar si Git esta instalado
try {
    $gitVersion = git --version
    Write-Host "[OK] Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git no esta instalado. Por favor instala Git primero." -ForegroundColor Red
    exit 1
}

# Verificar si estamos en el directorio correcto
if (!(Test-Path "app.py")) {
    Write-Host "[ERROR] Este script debe ejecutarse desde el directorio raiz del proyecto." -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Directorio actual: $(Get-Location)" -ForegroundColor Cyan

# Inicializar Git si no esta inicializado
if (!(Test-Path ".git")) {
    Write-Host "[+] Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Repositorio Git inicializado" -ForegroundColor Green
} else {
    Write-Host "[OK] Repositorio Git ya inicializado" -ForegroundColor Green
}

# Verificar si ya existe un remote
$remoteCheck = git remote 2>$null
$remoteExists = $remoteCheck -match "origin"

if (!$remoteExists) {
    Write-Host "[+] Configurando remote origin..." -ForegroundColor Yellow
    $repoUrl = "https://github.com/$GithubUsername/$RepoName.git"
    git remote add origin $repoUrl
    Write-Host "[OK] Remote configurado: $repoUrl" -ForegroundColor Green
} else {
    Write-Host "[OK] Remote origin ya existe" -ForegroundColor Green
}


# Cambiar a branch principal
Write-Host "[+] Cambiando a branch $Branch..." -ForegroundColor Yellow
git branch -M $Branch 2>$null
Write-Host "[OK] Branch configurado: $Branch" -ForegroundColor Green

# Agregar todos los archivos
Write-Host "[+] Agregando archivos al staging..." -ForegroundColor Yellow
git add .
Write-Host "[OK] Archivos agregados" -ForegroundColor Green

# Crear commit inicial si no existe
$commitCount = git rev-list --count HEAD 2>$null

if ($LASTEXITCODE -ne 0 -or !$commitCount -or $commitCount -eq "0") {
    Write-Host "[+] Creando commit inicial..." -ForegroundColor Yellow
    git commit -m "Initial commit with CI/CD configuration" -m "- API REST con Flask" -m "- Sistema de cache" -m "- 24 pruebas automatizadas (86% cobertura)" -m "- GitHub Actions CI/CD" -m "- Documentacion completa"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Commit creado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "[WARN] No hay cambios para commitear o ya existe un commit" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] Ya existe commit en el repositorio" -ForegroundColor Green
}

# Mostrar instrucciones finales
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "                  CONFIGURACION COMPLETADA                          " -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Crea el repositorio en GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "   Nombre: $RepoName" -ForegroundColor Cyan
Write-Host "   (NO inicialices con README, .gitignore o licencia)" -ForegroundColor Red
Write-Host ""
Write-Host "2. Sube el codigo a GitHub:" -ForegroundColor White
Write-Host "   git push -u origin $Branch" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Configura GitHub Actions:" -ForegroundColor White
Write-Host "   - Ve a Settings -> Actions -> General" -ForegroundColor Cyan
Write-Host "   - Permite 'Read and write permissions'" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Actualiza los badges en README.md:" -ForegroundColor White
Write-Host "   - Reemplaza YOUR_USERNAME con: $GithubUsername" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Habilita Dependabot:" -ForegroundColor White
Write-Host "   - Ve a Settings -> Security -> Dependabot" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. (Opcional) Crea un release:" -ForegroundColor White
Write-Host "   git tag v1.0.0" -ForegroundColor Cyan
Write-Host "   git push origin v1.0.0" -ForegroundColor Cyan
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentacion adicional:" -ForegroundColor Yellow
Write-Host "   - README.md" -ForegroundColor Cyan
Write-Host "   - GUIA_CICD.md (si existe)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Exito! Tu proyecto esta listo para CI/CD." -ForegroundColor Green
Write-Host ""

