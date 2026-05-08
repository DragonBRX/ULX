#!/usr/bin/env python3
"""
ULX Package Manager - Gerenciador de pacotes ULX
"""

import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict


REGISTRY_URL = "https://registry.ulx.dev"
PACKAGES_DIR = Path.home() / ".ulx" / "packages"


@dataclass
class Package:
    """Representa um pacote ULX"""
    name: str
    version: str
    description: str = ""
    author: str = ""
    license: str = "MIT"
    dependencies: List[str] = None
    files: List[str] = None
    entry_point: str = ""
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.files is None:
            self.files = []
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Package':
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Package':
        return cls.from_dict(json.loads(json_str))


class PackageManager:
    """Gerenciador de pacotes ULX"""
    
    def __init__(self):
        self.packages_dir = PACKAGES_DIR
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.installed = self._load_installed()
    
    def _load_installed(self) -> Dict[str, str]:
        """Carrega lista de pacotes instalados"""
        registry = self.packages_dir / "registry.json"
        if registry.exists():
            with open(registry, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_installed(self):
        """Salva lista de pacotes instalados"""
        registry = self.packages_dir / "registry.json"
        with open(registry, 'w', encoding='utf-8') as f:
            json.dump(self.installed, f, indent=2)
    
    def init(self, name: str, description: str = "", author: str = "") -> Package:
        """Inicializa um novo pacote"""
        pkg = Package(
            name=name,
            version="1.0.0",
            description=description,
            author=author
        )
        
        # Cria ulx.json
        with open("ulx.json", 'w', encoding='utf-8') as f:
            f.write(pkg.to_json())
        
        # Cria estrutura de diretórios
        Path("src").mkdir(exist_ok=True)
        Path("tests").mkdir(exist_ok=True)
        Path("docs").mkdir(exist_ok=True)
        
        # Cria arquivo principal
        main_file = Path("src") / "main.ulx"
        if not main_file.exists():
            main_file.write_text('escreva("Hello from ' + name + '!")\n')
        
        print(f"Pacote '{name}' inicializado!")
        return pkg
    
    def install(self, package_name: str, version: str = None) -> bool:
        """Instala um pacote"""
        print(f"Instalando {package_name}...")
        
        # Verifica se já está instalado
        if package_name in self.installed:
            print(f"  {package_name} já instalado (v{self.installed[package_name]})")
            return False
        
        # Aqui você implementaria o download do registry
        # Por enquanto, simula a instalação
        version = version or "latest"
        self.installed[package_name] = version
        self._save_installed()
        
        print(f"  ✅ {package_name}@{version} instalado")
        return True
    
    def uninstall(self, package_name: str) -> bool:
        """Remove um pacote"""
        if package_name not in self.installed:
            print(f"  {package_name} não está instalado")
            return False
        
        del self.installed[package_name]
        self._save_installed()
        
        # Remove diretório do pacote
        pkg_dir = self.packages_dir / package_name
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)
        
        print(f"  ✅ {package_name} removido")
        return True
    
    def list_installed(self) -> Dict[str, str]:
        """Lista pacotes instalados"""
        return self.installed.copy()
    
    def update(self, package_name: str = None) -> bool:
        """Atualiza pacotes"""
        if package_name:
            if package_name in self.installed:
                print(f"Atualizando {package_name}...")
                # Simula atualização
                print(f"  ✅ {package_name} atualizado")
                return True
            else:
                print(f"  {package_name} não instalado")
                return False
        else:
            print("Atualizando todos os pacotes...")
            for pkg in self.installed:
                print(f"  ✅ {pkg} atualizado")
            return True
    
    def search(self, query: str) -> List[str]:
        """Busca pacotes no registry"""
        # Simula busca
        return [f"{query}-core", f"{query}-utils", f"{query}-advanced"]
    
    def build(self, output_dir: str = "dist") -> str:
        """Compila pacote para distribuição"""
        if not Path("ulx.json").exists():
            print("Erro: ulx.json não encontrado. Execute 'ulx-pkg init' primeiro.")
            return None
        
        with open("ulx.json", 'r', encoding='utf-8') as f:
            pkg = Package.from_json(f.read())
        
        # Cria diretório de saída
        out = Path(output_dir)
        out.mkdir(exist_ok=True)
        
        # Cria pacote .ulxp (zip)
        pkg_file = out / f"{pkg.name}-{pkg.version}.ulxp"
        
        with zipfile.ZipFile(pkg_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in Path("src").rglob("*.ulx"):
                zf.write(file, file.relative_to("."))
            zf.write("ulx.json")
        
        print(f"Pacote compilado: {pkg_file}")
        return str(pkg_file)
    
    def show_info(self, package_name: str = None):
        """Mostra informações do pacote"""
        if package_name is None:
            # Mostra info do pacote local
            if not Path("ulx.json").exists():
                print("Nenhum pacote encontrado (ulx.json não existe)")
                return
            
            with open("ulx.json", 'r', encoding='utf-8') as f:
                pkg = Package.from_json(f.read())
        else:
            # Mostra info de pacote instalado
            if package_name not in self.installed:
                print(f"Pacote '{package_name}' não instalado")
                return
            pkg = Package(name=package_name, version=self.installed[package_name])
        
        print(f"\n{'='*40}")
        print(f"  {pkg.name} v{pkg.version}")
        print(f"{'='*40}")
        if pkg.description:
            print(f"  Descrição: {pkg.description}")
        if pkg.author:
            print(f"  Autor: {pkg.author}")
        if pkg.license:
            print(f"  Licença: {pkg.license}")
        if pkg.dependencies:
            print(f"  Dependências: {', '.join(pkg.dependencies)}")
        print(f"{'='*40}\n")


def main():
    import sys
    
    pm = PackageManager()
    
    if len(sys.argv) < 2:
        print("""
ULX Package Manager

Uso:
  ulx-pkg init <nome> [descricao] [autor]  - Inicializa pacote
  ulx-pkg install <pacote> [versao]         - Instala pacote
  ulx-pkg uninstall <pacote>                - Remove pacote
  ulx-pkg list                              - Lista instalados
  ulx-pkg update [pacote]                   - Atualiza pacotes
  ulx-pkg search <query>                    - Busca pacotes
  ulx-pkg build                             - Compila pacote
  ulx-pkg info [pacote]                     - Informações
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'init':
        name = sys.argv[2] if len(sys.argv) > 2 else "meu-pacote"
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        author = sys.argv[4] if len(sys.argv) > 4 else ""
        pm.init(name, desc, author)
    
    elif cmd == 'install':
        pkg = sys.argv[2] if len(sys.argv) > 2 else ""
        version = sys.argv[3] if len(sys.argv) > 3 else None
        pm.install(pkg, version)
    
    elif cmd == 'uninstall':
        pkg = sys.argv[2] if len(sys.argv) > 2 else ""
        pm.uninstall(pkg)
    
    elif cmd == 'list':
        installed = pm.list_installed()
        if installed:
            print("\nPacotes instalados:")
            for name, version in installed.items():
                print(f"  {name}@{version}")
        else:
            print("Nenhum pacote instalado")
    
    elif cmd == 'update':
        pkg = sys.argv[2] if len(sys.argv) > 2 else None
        pm.update(pkg)
    
    elif cmd == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = pm.search(query)
        print(f"\nResultados para '{query}':")
        for r in results:
            print(f"  {r}")
    
    elif cmd == 'build':
        pm.build()
    
    elif cmd == 'info':
        pkg = sys.argv[2] if len(sys.argv) > 2 else None
        pm.show_info(pkg)
    
    else:
        print(f"Comando desconhecido: {cmd}")


if __name__ == '__main__':
    main()
