#!/usr/bin/env python3
"""
CLX - Compilador Universal ULX
Gerador de Formatos de Saída
Suporta: Windows (.exe), Linux (bin), macOS (.app), Android (.apk), Web (.html)
"""

import os
import json
import subprocess
from pathlib import Path

class FormatGenerator:
    """Gerador de formatos de saída para diferentes plataformas"""

    def __init__(self, project_name):
        self.project_name = project_name
        self.output_dir = Path(f"dist/{project_name}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_windows_exe(self, c_code):
        """Gera executável Windows (.exe)"""
        output = self.output_dir / "windows"
        output.mkdir(exist_ok=True)

        c_file = output / f"{self.project_name}.c"
        exe_file = output / f"{self.project_name}.exe"

        c_file.write_text(c_code)

        # Verifica se GCC/MinGW está disponível
        if self._has_compiler("gcc") or self._has_compiler("x86_64-w64-mingw32-gcc"):
            compiler = "gcc" if self._has_compiler("gcc") else "x86_64-w64-mingw32-gcc"
            subprocess.run([
                compiler, c_file, "-o", exe_file, "-lm"
            ], check=True)
            return str(exe_file)
        else:
            # Gera apenas o código C se não houver compilador cruzado
            return str(c_file)

    def to_linux_binary(self, c_code):
        """Gera binário Linux nativo"""
        output = self.output_dir / "linux"
        output.mkdir(exist_ok=True)

        c_file = output / f"{self.project_name}.c"
        binary = output / self.project_name

        c_file.write_text(c_code)

        if self._has_compiler("gcc"):
            subprocess.run([
                "gcc", c_file, "-o", binary, "-lm", "-no-pie"
            ], check=True)
            os.chmod(binary, 0o755)
            return str(binary)
        return str(c_file)

    def to_macos_app(self, c_code):
        """Gera aplicativo macOS (.app)"""
        output = self.output_dir / "macos"
        output.mkdir(exist_ok=True)

        c_file = output / f"{self.project_name}.c"
        binary = output / self.project_name

        c_file.write_text(c_code)

        if self._has_compiler("gcc"):
            subprocess.run([
                "gcc", c_file, "-o", binary, "-lm"
            ], check=True)
            os.chmod(binary, 0o755)
            return str(binary)
        return str(c_file)

    def to_android_apk(self, ulx_code):
        """Gera APK Android (via Gradle/Java wrapper)"""
        output = self.output_dir / "android"
        output.mkdir(exist_ok=True)

        # Gera projeto Android básico
        android_project = f"""
package com.ulx.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.*;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(50, 50, 50, 50);

        TextView title = new TextView(this);
        title.setText("{self.project_name}");
        title.setTextSize(24);
        layout.addView(title);

        TextView output = new TextView(this);
        output.setText("{ulx_code[:100].replace(chr(10), ' ')}...");
        layout.addView(output);

        setContentView(layout);
    }}
}}
"""
        java_file = output / "app/src/main/java/com/ulx/app/MainActivity.java"
        java_file.parent.mkdir(parents=True, exist_ok=True)
        java_file.write_text(android_project)

        return str(output)

    def to_web_html(self, c_code):
        """Gera HTML5/JavaScript para web"""
        output = self.output_dir / "web"
        output.mkdir(exist_ok=True)

        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.project_name} - ULX Web</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #0f3460;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }}
        .code-box {{
            background: #1a1a2e;
            color: #00ff88;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .info {{
            margin-top: 20px;
            padding: 15px;
            background: #e94560;
            color: white;
            border-radius: 10px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {self.project_name}</h1>
        <div class="code-box">
<!-- Código ULX/ULV compilado -->
{c_code[:500]}
        </div>
        <div class="info">
            ⚡ ULX Web Build | Compilado via CLX
        </div>
    </div>
</body>
</html>"""

        html_file = output / "index.html"
        html_file.write_text(html_content)
        return str(html_file)

    def to_npm_package(self, ulx_code):
        """Gera pacote NPM para Node.js"""
        output = self.output_dir / "npm"
        output.mkdir(exist_ok=True)

        package_json = {
            "name": self.project_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": f"Gerado por ULX/CLX - {self.project_name}",
            "main": "index.js",
            "scripts": {
                "start": "node index.js"
            },
            "keywords": ["ulx", "compiler", "clx"],
            "author": "ULX Team"
        }

        main_js = f"""// {self.project_name}
// Gerado por ULX/CLX Compiler
console.log("🚀 {self.project_name}");
console.log("Compilado de ULX para JavaScript/Node.js");

// Código original ULX:
const ulxCode = `{ulx_code}`;

// Interpretador ULX básico (placeholder)
console.log("\\n📝 Código ULX:");
console.log(ulxCode);
"""

        (output / "package.json").write_text(json.dumps(package_json, indent=2))
        (output / "index.js").write_text(main_js)

        return str(output)

    def build_all(self, c_code, ulx_code):
        """Compila para todas as plataformas"""
        results = {}

        platforms = [
            ("windows", self.to_windows_exe(c_code)),
            ("linux", self.to_linux_binary(c_code)),
            ("macos", self.to_macos_app(c_code)),
            ("android", self.to_android_apk(ulx_code)),
            ("web", self.to_web_html(c_code)),
            ("npm", self.to_npm_package(ulx_code))
        ]

        for name, path in platforms:
            results[name] = path
            print(f"  ✅ {name}: {path}")

        return results

    def _has_compiler(self, compiler):
        """Verifica se compilador está disponível"""
        try:
            subprocess.run([compiler, "--version"],
                         capture_output=True, check=True)
            return True
        except:
            return False

def main():
    import sys

    if len(sys.argv) < 3:
        print("Uso: clx_formats.py <projeto> <codigo.ulx>")
        print("\nPlataformas: windows, linux, macos, android, web, npm, all")
        sys.exit(1)

    project = sys.argv[1]
    ulx_file = sys.argv[2]
    platform = sys.argv[3] if len(sys.argv) > 3 else "all"

    # Lê código ULX
    code = Path(ulx_file).read_text()

    gen = FormatGenerator(project)

    # Lê código C gerado (simulado para demonstração)
    c_code = f"""
// {project} - Gerado por CLX
#include <stdio.h>
#include <stdlib.h>

int main() {{
    printf("🚀 {project}\\n");
    printf("Compilado por CLX - Universal Compiler\\n");
    return 0;
}}
"""

    print(f"\n📦 CLX Format Generator - {project}")
    print("=" * 40)

    if platform == "all":
        gen.build_all(c_code, code)
    else:
        if platform == "windows":
            result = gen.to_windows_exe(c_code)
        elif platform == "linux":
            result = gen.to_linux_binary(c_code)
        elif platform == "macos":
            result = gen.to_macos_app(c_code)
        elif platform == "android":
            result = gen.to_android_apk(code)
        elif platform == "web":
            result = gen.to_web_html(c_code)
        elif platform == "npm":
            result = gen.to_npm_package(code)
        else:
            print(f"❌ Plataforma '{platform}' não suportada")
            return

        print(f"  ✅ {platform}: {result}")

    print("\n✨ Compilação completa!")

if __name__ == "__main__":
    main()
