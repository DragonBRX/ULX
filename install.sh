#!/bin/bash
# ULX Installer - Linux/macOS
# Versão: 3.0

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "============================================================"
echo "   ULX - Instalador v3.0"
echo "============================================================"
echo -e "${NC}"

# Verifica se é root (para Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[✗] Execute como root: sudo bash install.sh${NC}"
   exit 1
fi

echo -e "${YELLOW}[*] Verificando dependências...${NC}"

# Verifica Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[✗] Python 3 não encontrado!${NC}"
    echo "Instale com:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora: sudo dnf install python3"
    exit 1
fi

echo -e "${GREEN}[✓] Python 3: $(python3 --version)${NC}"

# Verifica GCC
if ! command -v gcc &> /dev/null; then
    echo -e "${YELLOW}[*] GCC não encontrado. Instalando...${NC}"
    if command -v apt-get &> /dev/null; then
        apt-get update -qq
        apt-get install -y gcc gcc-multilib
    elif command -v dnf &> /dev/null; then
        dnf install -y gcc
    elif command -v pacman &> /dev/null; then
        pacman -S --noconfirm gcc
    fi
fi

if command -v gcc &> /dev/null; then
    echo -e "${GREEN}[✓] GCC: $(gcc --version | head -1)${NC}"
fi

# Diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${YELLOW}[1/5] Instalando compilador ULX...${NC}"

# Copia compilador
cp "$SCRIPT_DIR/compiler/clx_compiler.py" /usr/local/bin/ulx-compile
chmod +x /usr/local/bin/ulx-compile
echo -e "${GREEN}[✓] ulx-compile instalado${NC}"

echo ""
echo -e "${YELLOW}[2/5] Instalando runtime ULX...${NC}"

# Copia runtime
cp "$SCRIPT_DIR/runtime/ulx_runner.py" /usr/local/bin/ulx-run
chmod +x /usr/local/bin/ulx-run
echo -e "${GREEN}[✓] ulx-run instalado${NC}"

# Copia packager
cp "$SCRIPT_DIR/runtime/ulx_packager.py" /usr/local/bin/ulx-pack
chmod +x /usr/local/bin/ulx-pack
echo -e "${GREEN}[✓] ulx-pack instalado${NC}"

# Copia init
cp "$SCRIPT_DIR/runtime/ulx_init.py" /usr/local/bin/ulx-init
chmod +x /usr/local/bin/ulx-init
echo -e "${GREEN}[✓] ulx-init instalado${NC}"

echo ""
echo -e "${YELLOW}[3/5] Registrando tipo MIME...${NC}"

# Cria definição MIME
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > /usr/share/mime/packages/application-x-ulx.xml << 'XMLEOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-ulx">
    <comment>ULX Executable</comment>
    <comment xml:lang="pt">Executável ULX</comment>
    <glob pattern="*.ulx"/>
    <magic>
      <match type="string" offset="0" value="ULX"/>
    </magic>
    <icon name="application-x-executable"/>
  </mime-type>
</mime-info>
XMLEOF

    update-mime-database /usr/share/mime 2>/dev/null || true
    echo -e "${GREEN}[✓] Tipo MIME registrado${NC}"
fi

echo ""
echo -e "${YELLOW}[4/5] Registrando handler...${NC}"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > /usr/share/applications/ulx-handler.desktop << 'DESKTOPEOF'
[Desktop Entry]
Type=Application
Name=ULX Runtime
Comment=Executa aplicativos ULX
Exec=/usr/local/bin/ulx-run %f
Icon=application-x-executable
Terminal=true
MimeType=application/x-ulx;
Categories=Development;
DESKTOPEOF

    update-desktop-database /usr/share/applications 2>/dev/null || true
    echo -e "${GREEN}[✓] Handler registrado${NC}"
fi

echo ""
echo -e "${YELLOW}[5/5] Configuração final...${NC}"

echo -e "${GREEN}[✓] ULX instalado com sucesso!${NC}"

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}   ULX Runtime instalado com sucesso!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "Comandos disponíveis:"
echo -e "  ${YELLOW}ulx-compile <arquivo.ulx>${NC}  - Compila para binário"
echo -e "  ${YELLOW}ulx-run <app.ulx>${NC}          - Executa aplicativo"
echo -e "  ${YELLOW}ulx-pack pack <bin> -o app.ulx${NC} - Empacota aplicativo"
echo -e "  ${YELLOW}ulx-init <nome>${NC}             - Cria novo projeto"
echo ""
echo -e "Exemplo:"
echo -e "  ${YELLOW}ulx-compile exemplo.ulx -o app${NC}"
echo -e "  ${YELLOW}./app${NC}"
echo ""
