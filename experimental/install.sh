#!/bin/bash
#============================================#
#   ULX Installer - Shell Script              #
#   Universal Language X v3.0                #
#============================================#

set -e

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║                                               ║"
echo "║   ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ║"
echo "║   ██║    ██║██╔════╝██║     ██╔═══██╗██╔══██╗║"
echo "║   ██║ █╗ ██║█████╗  ██║     ██║   ██║██████╔╝║"
echo "║   ██║███╗██║██╔══╝  ██║     ██║   ██║██╔══██╗║"
echo "║   ╚███╔███╔╝███████╗███████╗╚██████╔╝██║  ██║║"
echo "║    ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝║"
echo "║                                               ║"
echo "║   Universal Language X - v3.0                 ║"
echo "║   Instalador Shell                            ║"
echo "║                                               ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Verifica Python
info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 não encontrado!"
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
info "Python $PYTHON_VERSION encontrado"

# Verifica GCC
info "Verificando GCC..."
if command -v gcc &> /dev/null; then
    GCC_VERSION=$(gcc --version | head -n1)
    info "$GCC_VERSION"
else
    warn "GCC não encontrado - instalando..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y gcc make
    elif command -v brew &> /dev/null; then
        brew install gcc
    else
        warn "Instale o GCC manualmente"
    fi
fi

# Instala diretórios
info "Criando diretórios..."
mkdir -p "$HOME/.ulx"
mkdir -p "$HOME/.local/bin"
ULX_DIR="$HOME/.ulx"
BIN_DIR="$HOME/.local/bin"

# Copia arquivos
info "Instalando ULX..."

# Compilador
if [ -f "clx_compiler/clx_compiler.py" ]; then
    cp clx_compiler/clx_compiler.py "$ULX_DIR/"
    info "✓ CLX Compiler"
fi

# Formatos
if [ -f "clx_compiler/clx_formats.py" ]; then
    cp clx_compiler/clx_formats.py "$ULX_DIR/"
    info "✓ CLX Formats"
fi

# Linguagem
if [ -d "ulx_language" ]; then
    cp -r ulx_language "$ULX_DIR/"
    info "✓ ULX Language"
fi

# Visual
if [ -d "ulv_visual" ]; then
    cp -r ulv_visual "$ULX_DIR/"
    info "✓ ULV Visual"
fi

# ULQ
if [ -d "ulq_intelligence" ]; then
    cp -r ulq_intelligence "$ULX_DIR/"
    info "✓ ULQ Intelligence"
fi

# NFX
if [ -d "nfx_format" ]; then
    cp -r nfx_format "$ULX_DIR/"
    info "✓ NFX Format"
fi

# Wrapper ULX
cat > "$BIN_DIR/ulx" << 'WRAPPER'
#!/bin/bash
~/.ulx/clx_compiler.py "$@"
WRAPPER
chmod +x "$BIN_DIR/ulx"

# Wrapper CLX
cat > "$BIN_DIR/clx" << 'CLX_WRAPPER'
#!/bin/bash
~/.ulx/clx_formats.py "$@"
CLX_WRAPPER
chmod +x "$BIN_DIR/clx"

info "✓ Comandos ulx e clx"

# Adiciona ao PATH se necessário
SHELL_RC="$HOME/.bashrc"
if [ -f "$SHELL_RC" ]; then
    if ! grep -q '~/.local/bin' "$SHELL_RC"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        info "PATH atualizado em ~/.bashrc"
    fi
fi

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              Instalação Completa!                     ║"
echo "╠═══════════════════════════════════════════════════════╣"
echo "║                                                       ║"
echo "║  Execute seus programas ULX:                          ║"
echo "║                                                       ║"
echo "║    ulx meu_programa.ulx           # Compila e executa  ║"
echo "║    clx build all meuapp.ulx      # Todas plataformas  ║"
echo "║                                                       ║"
echo "║  Plataformas: Windows, Linux, macOS, Android, Web     ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
info "Reinicie o terminal ou execute: source ~/.bashrc"