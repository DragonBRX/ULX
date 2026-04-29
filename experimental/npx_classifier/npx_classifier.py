#!/usr/bin/env python3
"""
NPX - Neural Pulse Classifier
Classificador Semântico para IA baseada em indexação
"""

import json
import struct
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

MAGIC_BYTES = b"NPX\n"

# DNA Semântico - Domínios e Códigos
DOMAIN_CODES = {
    "MECANICA": 0x01, "CULINARIA": 0x02, "SAUDE": 0x03,
    "TECNOLOGIA": 0x04, "CIENCIA": 0x05, "HUMANAS": 0x06,
    "ARTE": 0x07, "DIREITO": 0x08, "FINANCAS": 0x09,
    "ESPORTES": 0x0A, "MATEMATICA": 0x0B, "IDIOMAS": 0x0C,
    "MUSICA": 0x0D, "GAMES": 0x0E, "FINANCE": 0x0F,
    "PROGRAMACAO": 0x10, "HARDWARE": 0x11, "REDES": 0x12,
    "IA_ML": 0x13, "DATA_SCIENCE": 0x14, "ASTROFISICA": 0x15,
    "QUIMICA": 0x16, "BIOLOGIA": 0x17, "ENGENHARIA": 0x18,
    "AGRICULTURA": 0x19, "MEIO_AMBIENTE": 0x1A, "EDUCACAO": 0x1B,
    "PSICOLOGIA": 0x1C, "FILOSOFIA": 0x1D, "HISTORIA": 0x1E,
    "GEOGRAFIA": 0x1F, "POLITICA": 0x20, "RELIGIAO": 0x21,
    "MODA": 0x22, "ARQUITETURA": 0x23, "ESPACIAL": 0x24,
    "OCEANO": 0x25, "METEOROLOGIA": 0x26, "FARMACIA": 0x27,
    "VETERINARIA": 0x28, "AUTOMOTIVO": 0x29, "AERONAUTICA": 0x2A,
    "NAVAL": 0x2B, "ENERGIA": 0x2C, "MINERACAO": 0x2D,
    "TEXTIL": 0x2E, "COSMETICOS": 0x2F, "LAZER": 0x30
}

# Palavras-chave para classificação
KEYWORD_MAP = {
    "motor": ("MECANICA", "AUTOMOTIVO"),
    "carro": ("MECANICA", "AUTOMOTIVO"),
    "receita": ("CULINARIA", "RECEITAS"),
    "cozinhar": ("CULINARIA", "TECNICAS"),
    "medicamento": ("SAUDE", "FARMACIA"),
    "remédio": ("SAUDE", "FARMACIA"),
    "treinar": ("SAUDE", "FITNESS"),
    "python": ("PROGRAMACAO", "TECNOLOGIA"),
    "código": ("PROGRAMACAO", "TECNOLOGIA"),
    "api": ("PROGRAMACAO", "REDES"),
    "neural": ("IA_ML", "TECNOLOGIA"),
    "machine learning": ("IA_ML", "DATA_SCIENCE"),
    "estrela": ("ASTROFISICA", "ESPACIAL"),
    "planeta": ("ASTROFISICA", "ESPACIAL"),
    "física": ("CIENCIA", "FISICA"),
    "química": ("CIENCIA", "QUIMICA"),
    "dna": ("BIOLOGIA", "GENETICA"),
    "célula": ("BIOLOGIA", "CITOLOGIA"),
    "história": ("HISTORIA", "HUMANAS"),
    "lei": ("DIREITO", "JURIDICO"),
    "investimento": ("FINANCAS", "INVESTIMENTOS"),
    "ações": ("FINANCAS", "BOLSA"),
    "futebol": ("ESPORTES", "FUTEBOL"),
    "nadar": ("ESPORTES", "AQUATICOS"),
    "guitarra": ("MUSICA", "INSTRUMENTOS"),
    "piano": ("MUSICA", "INSTRUMENTOS"),
    "pintura": ("ARTE", "VISUAL"),
    "desenho": ("ARTE", "VISUAL"),
    "poesia": ("ARTE", "LITERATURA"),
    "matemática": ("MATEMATICA", "CIENCIA"),
    "equação": ("MATEMATICA", "ALGEBRA"),
    "inglês": ("IDIOMAS", "INGLES"),
    "espanhol": ("IDIOMAS", "ESPANHOL"),
    "português": ("IDIOMAS", "PORTUGUES"),
    "jogo": ("GAMES", "LAZER"),
    "xbox": ("GAMES", "HARDWARE"),
    "ps5": ("GAMES", "HARDWARE"),
    "pc": ("HARDWARE", "TECNOLOGIA"),
    "memória": ("HARDWARE", "COMPONENTES"),
    "rede": ("REDES", "INTERNET"),
    "wi-fi": ("REDES", "WIRELESS"),
    "banco de dados": ("DATA_SCIENCE", "DATABASES"),
    "sql": ("DATA_SCIENCE", "DATABASES"),
    "machine learning": ("IA_ML", "ALGORITMOS"),
    "deep learning": ("IA_ML", "REDES_NEURAIS"),
    "astro": ("ESPACIAL", "ASTRONOMIA"),
    "satélite": ("ESPACIAL", "AERONAUTICA"),
    "planeta": ("ESPACIAL", "ASTRONOMIA"),
    "energia": ("ENERGIA", "RENOVAVEL"),
    "solar": ("ENERGIA", "RENOVAVEL"),
    "vento": ("ENERGIA", "EOLICA"),
    "tratamento": ("SAUDE", "MEDICINA"),
    "vacina": ("SAUDE", "IMUNIZACAO"),
    "construção": ("ENGENHARIA", "CIVIL"),
    "edifício": ("ENGENHARIA", "CIVIL"),
    "soldar": ("ENGENHARIA", "METALURGICA"),
    "fazer": ("CULINARIA", "TECNICAS"),
    "preparar": ("CULINARIA", "TECNICAS"),
    "assado": ("CULINARIA", "TECNICAS"),
    "ferver": ("CULINARIA", "TECNICAS"),
}

INTENT_TYPES = {
    "pergunta": "QUER_SABER",
    "como": "QUER_SABER",
    "o que é": "QUER_SABER",
    "onde": "LOCALIZACAO",
    "quando": "TEMPORAL",
    "por que": "EXPLICACAO",
    "quanto": "QUANTIDADE",
    "faça": "ACAO",
    "como fazer": "ACAO",
    "melhor": "COMPARACAO",
    "diferença": "COMPARACAO",
}


@dataclass
class Classification:
    """Resultado da classificação NPX"""
    domain: str
    category: str
    object_type: str
    action: str
    binary_code: int
    pointer: str
    intent_type: str
    urgency: str
    confidence: float


class NPXClassifier:
    """Classificador Semântico NPX"""

    def __init__(self):
        self.domains = DOMAIN_CODES
        self.keywords = KEYWORD_MAP
        self.intents = INTENT_TYPES

    def classify(self, text: str) -> Classification:
        """Classifica texto e retorna estrutura semântica"""

        text_lower = text.lower()

        # 1. Detecta domínio principal
        domain_scores = {}
        for keyword, (domain, category) in self.keywords.items():
            if keyword in text_lower:
                domain_scores[domain] = domain_scores.get(domain, 0) + 1

        if not domain_scores:
            primary_domain = "GENERICO"
            primary_category = "GERAL"
        else:
            primary_domain = max(domain_scores, key=domain_scores.get)
            primary_category = self.keywords[
                max(self.keywords, key=lambda k: self.keywords[k][0] == primary_domain)
            ][1]

        # 2. Detecta intenção
        intent_type = "NEUTRAL"
        for pattern, intent in self.intents.items():
            if pattern in text_lower:
                intent_type = intent
                break

        # 3. Detecta objeto e ação
        object_type = self._extract_object(text_lower)
        action = self._extract_action(text_lower)

        # 4. Gera código binário
        binary_code = self.domains.get(primary_domain, 0)
        if binary_code == 0:
            binary_code = 0xFF  # GENERICO

        # 5. Gera ponteiro (endereço no .nfx)
        pointer = f"0x{binary_code:08X}"

        # 6. Detecta urgência
        urgency = "LOW"
        if any(w in text_lower for w in ["urgente", "emergência", "socorro", "ajuda"]):
            urgency = "HIGH"
        elif any(w in text_lower for w in ["preciso", "necessito", "importante"]):
            urgency = "MEDIUM"

        # 7. Calcula confiança
        confidence = min(0.95, 0.5 + (len(domain_scores) * 0.15))

        return Classification(
            domain=primary_domain,
            category=primary_category,
            object_type=object_type,
            action=action,
            binary_code=binary_code,
            pointer=pointer,
            intent_type=intent_type,
            urgency=urgency,
            confidence=confidence
        )

    def _extract_object(self, text: str) -> str:
        """Extrai objeto principal do texto"""
        objects = ["motor", "sistema", "processo", "componente", "estrutura"]
        for obj in objects:
            if obj in text:
                return obj.upper()
        return "OBJETO_DESCONHECIDO"

    def _extract_action(self, text: str) -> str:
        """Extrai ação do texto"""
        actions = {
            "consertar": "REPARO",
            "arrumar": "REPARO",
            "fazer": "CRIACAO",
            "criar": "CRIACAO",
            "construir": "CONSTRUCAO",
            "aprender": "APRENDIZADO",
            "ensinar": "ENSINO",
            "explicar": "EXPLICACAO",
            "calcular": "CALCULO",
            "analisar": "ANALISE",
            "comparar": "COMPARACAO",
            "otimizar": "OTIMIZACAO",
            "instalar": "INSTALACAO",
            "configurar": "CONFIGURACAO",
            "programar": "PROGRAMACAO",
            "desenvolver": "DESENVOLVIMENTO",
        }
        for action_word, action_type in actions.items():
            if action_word in text:
                return action_type
        return "INFO"

    def to_ulq(self, text: str) -> Dict:
        """Converte para formato ULQ"""
        classification = self.classify(text)

        return {
            "project": "npx_classifier",
            "type": "classification",
            "input": text,
            "dna_semantic": {
                "domain": classification.domain,
                "category": classification.category,
                "object": classification.object_type,
                "action": classification.action
            },
            "binary_code": {
                "decimal": classification.binary_code,
                "hex": f"0x{classification.binary_code:02X}",
                "binary": format(classification.binary_code, "08b")
            },
            "pointer": classification.pointer,
            "intent": {
                "type": classification.intent_type,
                "urgency": classification.urgency,
                "confidence": f"{classification.confidence:.2%}"
            },
            "nfx_target": f"{classification.pointer}.nfx",
            "speed_profile": "FAST" if classification.confidence > 0.8 else "MODERATE"
        }

    def explain(self, text: str) -> str:
        """Explica classificação em formato legível"""
        ulq = self.to_ulq(text)
        dna = ulq["dna_semantic"]
        binary = ulq["binary_code"]

        lines = [
            f"📥 Input: \"{text}\"",
            "",
            "🧬 DNA Semântico:",
            f"   Domínio:    {dna['domain']}",
            f"   Categoria:  {dna['category']}",
            f"   Objeto:     {dna['object']}",
            f"   Ação:       {dna['action']}",
            "",
            "📊 Código Binário:",
            f"   Decimal: {binary['decimal']}",
            f"   Hex:     {binary['hex']}",
            f"   Binário: {binary['binary']}",
            "",
            "🎯 Ponteiro NFX:",
            f"   → {ulq['pointer']} (acesso direto aos dados)",
            "",
            "⚡ Intenção:",
            f"   Tipo:      {ulq['intent']['type']}",
            f"   Urgência:  {ulq['intent']['urgency']}",
            f"   Confiança: {ulq['intent']['confidence']}",
            "",
            f"🚀 Velocidade: {ulq['speed_profile']}",
        ]

        return "\n".join(lines)


class NPXFile:
    """Gerencia arquivos .npx"""

    def __init__(self, path: str):
        self.path = path
        self.magic = MAGIC_BYTES
        self.taxonomy: List[Dict] = []
        self.classifications: List[Dict] = []

    def save(self):
        """Salva arquivo .npx"""
        with open(self.path, "wb") as f:
            f.write(self.magic)
            data = json.dumps({
                "taxonomy": self.taxonomy,
                "classifications": self.classifications
            }).encode()
            f.write(struct.pack("I", len(data)))
            f.write(data)

    def load(self):
        """Carrega arquivo .npx"""
        with open(self.path, "rb") as f:
            magic = f.read(4)
            if magic != self.magic:
                raise ValueError("Arquivo não é .npx válido")
            size = struct.unpack("I", f.read(4))[0]
            data = json.loads(f.read(size).decode())
            self.taxonomy = data["taxonomy"]
            self.classifications = data["classifications"]


def main():
    import sys

    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════╗
║        NEURAL.PULSE (.npx) Classifier v1.0           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Classificar texto:                                  ║
║    python npx_classifier.py classify "Como consertar   ║
║                                um motor?"             ║
║                                                       ║
║  Exportar ULQ:                                       ║
║    python npx_classifier.py ulq "texto..."            ║
║                                                       ║
║  Criar arquivo .npx:                                 ║
║    python npx_classifier.py create                    ║
║                                                       ║
║  Exemplos:                                           ║
║    "Receita de bolo de chocolate"                    ║
║    "Como instalar Python no Ubuntu"                   ║
║    "Qual a capital da França?"                       ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
        """)
        sys.exit(1)

    classifier = NPXClassifier()
    cmd = sys.argv[1]

    if cmd == "classify":
        text = sys.argv[2]
        print(classifier.explain(text))

    elif cmd == "ulq":
        text = sys.argv[2]
        ulq = classifier.to_ulq(text)
        print(json.dumps(ulq, indent=2))

    elif cmd == "create":
        npx = NPXFile("knowledge.npx")
        npx.taxonomy = [
            {"code": hex(v), "name": k}
            for k, v in DOMAIN_CODES.items()
        ]
        npx.save()
        print("✅ Arquivo .npx criado: knowledge.npx")

    elif cmd == "demo":
        examples = [
            "Como consertar um motor de carro?",
            "Receita de bolo de chocolate",
            "Como instalar Python no Ubuntu?",
            "Qual a capital da França?",
            "Como fazer um site em React?",
        ]
        print("\n🎯 Demo NPX Classifier:\n")
        for text in examples:
            print(classifier.explain(text))
            print("=" * 50)

    else:
        print(f"❌ Comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()