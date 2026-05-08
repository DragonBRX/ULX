#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULQ Parser - Parser para Inteligências Artificiais
Converte ULQ (JSON) para ULX e vice-versa

Uso: ulq-parser <arquivo.ulq> [--to-ulx] [--to-ulv]
"""

import json
import sys
import os


class ULQParser:
    """Parser ULQ - Interface para IAs"""

    # Tipos válidos de componentes ULQ
    VALID_TYPES = [
        "window", "dialog", "panel",
        "text", "label", "heading",
        "button", "icon_button", "toggle",
        "input", "textarea", "checkbox", "radio", "dropdown",
        "image", "icon", "canvas", "svg",
        "grid", "list", "table", "tree",
        "video", "audio", "iframe"
    ]

    def __init__(self):
        self.errors = []
        self.warnings = []

    def parse_file(self, filepath):
        """Lê arquivo ULQ e retorna dicionário"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.errors.append(f"Arquivo não encontrado: {filepath}")
            return None
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON inválido: {e}")
            return None

    def validate(self, ulq_data):
        """Valida estrutura ULQ"""
        self.errors = []
        self.warnings = []

        if not isinstance(ulq_data, dict):
            self.errors.append("ULQ deve ser um objeto JSON")
            return False

        # Verifica tipo base
        if "type" not in ulq_data:
            self.errors.append("Campo 'type' é obrigatório")
            return False

        if ulq_data["type"] not in self.VALID_TYPES:
            self.errors.append(f"Tipo '{ulq_data['type']}' não reconhecido")
            return False

        # Valida children se existir
        if "children" in ulq_data:
            if not isinstance(ulq_data["children"], list):
                self.errors.append("'children' deve ser uma lista")
                return False

            for child in ulq_data["children"]:
                if not self.validate(child):
                    return False

        return len(self.errors) == 0

    def to_ulx(self, ulq_data, indent=0):
        """Converte ULQ para código ULX"""
        lines = []
        prefix = "    " * indent

        ulq_type = ulq_data.get("type", "")

        if ulq_type == "window":
            name = ulq_data.get("name", "app")
            lines.append(f'// Janela: {name}')
            lines.append(f'escreva("Criando janela: {name}")')

            if "children" in ulq_data:
                for child in ulq_data["children"]:
                    lines.extend(self.to_ulx(child, indent))

        elif ulq_type == "text" or ulq_type == "label":
            content = ulq_data.get("content", "")
            lines.append(f'escreva("{content}")')

        elif ulq_type == "heading":
            content = ulq_data.get("content", "")
            level = ulq_data.get("level", 1)
            lines.append(f'escreva("=== {content} ===")')

        elif ulq_type == "button":
            text = ulq_data.get("text", "Button")
            action = ulq_data.get("action", "")
            lines.append(f'// Botão: {text}')
            if action:
                lines.append(f'// Ação: {action}')

        elif ulq_type == "input":
            name = ulq_data.get("name", "input")
            label = ulq_data.get("label", name)
            lines.append(f'{name} = leia("{label}: ")')

        elif ulq_type == "image":
            src = ulq_data.get("src", "")
            alt = ulq_data.get("alt", "Imagem")
            lines.append(f'// Imagem: {alt} ({src})')

        elif ulq_type == "canvas":
            width = ulq_data.get("width", 100)
            height = ulq_data.get("height", 100)
            lines.append(f'// Canvas: {width}x{height}')

        elif ulq_type == "grid":
            cols = ulq_data.get("columns", 3)
            rows = ulq_data.get("rows", 3)
            lines.append(f'// Grid: {cols}x{rows}')

        elif ulq_type == "list":
            items = ulq_data.get("items", [])
            lines.append(f'// Lista com {len(items)} itens')
            for item in items:
                if isinstance(item, str):
                    lines.append(f'escreva("  - {item}")')

        else:
            lines.append(f'// Componente: {ulq_type}')

        return lines

    def from_ulx(self, ulx_code):
        """Converte código ULX para ULQ (experimental)"""
        lines = ulx_code.split('\n')
        ulq_data = {
            "type": "window",
            "name": "App",
            "children": []
        }

        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            if line.startswith('escreva('):
                content = line[8:-1]
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                ulq_data["children"].append({
                    "type": "text",
                    "content": content
                })

            elif line.startswith('se ('):
                ulq_data["children"].append({
                    "type": "text",
                    "content": "[Condicional]"
                })

        return ulq_data

    def create_window(self, name, title="", width=400, height=300):
        """Cria estrutura básica de janela ULQ"""
        return {
            "type": "window",
            "name": name,
            "title": title or name,
            "width": width,
            "height": height,
            "children": []
        }

    def create_button(self, text, action=""):
        """Cria botão ULQ"""
        return {
            "type": "button",
            "text": text,
            "action": action,
            "style": {
                "background": "#007bff",
                "color": "#ffffff",
                "padding": "10px 20px"
            }
        }

    def create_text(self, content):
        """Cria texto ULQ"""
        return {
            "type": "text",
            "content": content
        }

    def create_input(self, name, label="", placeholder=""):
        """Cria input ULQ"""
        return {
            "type": "input",
            "name": name,
            "label": label or name,
            "placeholder": placeholder
        }

    def export_to_file(self, ulq_data, filepath):
        """Exporta ULQ para arquivo"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(ulq_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.errors.append(f"Erro ao exportar: {e}")
            return False

    def import_from_string(self, json_string):
        """Importa ULQ de string JSON"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON inválido: {e}")
            return None

    def optimize_for_ai(self, ulq_data):
        """Otimiza ULQ para processamento por IAs"""
        return {
            "v": 1,
            "t": ulq_data.get("type", "unknown"),
            "c": ulq_data.get("children", []),
            "s": ulq_data.get("style", {}),
            "a": ulq_data.get("action", ""),
            "k": list(ulq_data.keys())
        }

    def print_errors(self):
        """Imprime erros e avisos"""
        for err in self.errors:
            print(f"[ERRO] {err}")
        for warn in self.warnings:
            print(f"[AVISO] {warn}")


def main():
    print("=" * 50)
    print("   ULQ Parser - Interface para IAs")
    print("=" * 50)
    print()

    if len(sys.argv) < 2:
        print("Uso: ulq-parser <arquivo.ulq> [--to-ulx]")
        print()
        print("Exemplo:")
        print("  ulq-parser app.ulq --to-ulx")
        print()
        print("Para criar ULQ via código:")
        print("  from ulq_parser import ULQParser")
        print("  parser = ULQParser()")
        print("  window = parser.create_window('Meu App')")
        print("  window['children'].append(parser.create_text('Olá!'))")
        sys.exit(0)

    filepath = sys.argv[1]

    parser = ULQParser()
    ulq_data = parser.parse_file(filepath)

    if not ulq_data:
        parser.print_errors()
        sys.exit(1)

    if not parser.validate(ulq_data):
        print("[ERRO] ULQ inválido:")
        parser.print_errors()
        sys.exit(1)

    print(f"[OK] ULQ válido: {filepath}")
    print()

    if "--to-ulx" in sys.argv:
        print("Convertendo para ULX:")
        print("-" * 30)
        ulx_lines = parser.to_ulx(ulq_data)
        for line in ulx_lines:
            print(line)

        ulx_file = filepath.replace('.ulq', '.ulx')
        with open(ulx_file, 'w') as f:
            f.write('\n'.join(ulx_lines))
        print()
        print(f"[OK] ULX gerado: {ulx_file}")


if __name__ == '__main__':
    main()