import networkx as nx
import hashlib
import json
import datetime

class JusCogensNode:
    def __init__(self, id, title, content, weight=0.5, metadata=None):
        self.id = id
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.weight = self.evaluate_semantics(content, weight)
        self.hash = hashlib.sha256(f"{id}{content}".encode()).hexdigest()

    def evaluate_semantics(self, content, base):
        # РАСШИРЕННЫЕ ПРАВИЛА ВЕСОВ (Критический аудит)
        rules = {
            "Jus Cogens": 1.0, "ECHR": 0.9, "Torture": 1.0,
            "Rehabilitation": 0.95, "Macheret": 0.8,
            "Illegal": 0.1, "Forced": 0.05, "Forgery": 0.01,
            "Nantoi": 0.02, "Dulca": 0.02, "Murianu": 0.02,
            "Indescifrabila": 0.05 # Подозрительные подписи
        }
        weight = base
        for key, val in rules.items():
            if key.lower() in content.lower() or key.lower() in self.title.lower():
                weight = max(weight, val) if val > 0.5 else min(weight, val)
        return weight

class LegalAuditor:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_evidence(self, node, parents=[]):
        self.G.add_node(node.id, 
                        title=node.title, 
                        weight=node.weight, 
                        hash=node.hash,
                        content=node.content)
        for p in parents:
            self.G.add_edge(p, node.id)

    def export_for_web(self):
        # Экспорт для твоих HTML-дашбордов
        data = nx.node_link_data(self.G)
        with open("legal_graph.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def generate_report(self):
        report = [f"--- A©TŌR LEGAL INTEGRITY REPORT | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ---"]
        total_weight = 0
        nodes = self.G.nodes(data=True)
        for n_id, data in nodes:
            status = "🛡️ VALID" if data['weight'] > 0.7 else "⚠️ TOXIC"
            report.append(f"{status} | {n_id} | {data['title']} | Weight: {data['weight']}")
            total_weight += data['weight']
        
        avg_integrity = (total_weight / len(nodes)) * 100
        report.append(f"\n--- SYSTEM INTEGRITY INDEX: {avg_integrity:.2f}% ---")
        return "\n".join(report)

# --- Инициализация Case-Macheret-1997-2026 ---
auditor = LegalAuditor()

# Корень Jus Cogens
auditor.add_evidence(JusCogensNode("ROOT_JC", "UN Jus Cogens Protocol", "Fundamental International Law Integrity", 1.0))

# Интеграция Узлов Ответственности (из твоих HTML-файлов)
liability_nodes = [
    ("NODE_NANTOI", "Nantoi Liudmila", "Liability node: GNS Tax Authority violation"),
    ("NODE_DULCA", "Dulca V.G.", "Liability node: MAI Ministry of Interior violation"),
    ("NODE_MURIANU", "Murianu I.", "Liability node: Court System violation")
]

for n_id, title, desc in liability_nodes:
    auditor.add_evidence(JusCogensNode(n_id, title, desc), ["ROOT_JC"])

# Симуляция 90 апостилей (в будущем заменим на чтение из apostilles.csv)
for i in range(1, 91):
    signatory = "Indescifrabila" if i % 10 == 0 else "Official Signature"
    auditor.add_evidence(JusCogensNode(f"APO_{i}", f"Apostille #{i}", f"Signatory: {signatory}"), ["ROOT_JC"])

# Генерация артефактов
with open("audit_report.txt", "w", encoding="utf-8") as f:
    f.write(auditor.generate_report())

auditor.export_for_web()
