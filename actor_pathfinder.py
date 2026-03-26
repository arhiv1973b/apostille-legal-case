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
        # ЮРИДИЧЕСКИЙ ВЕС (v.11.5): Прямая корреляция с легитимностью подписи
        rules = {
            "Jus Cogens": 1.0, "ECHR": 0.9, "Torture": 1.0,
            "Rehabilitation": 0.95, "Macheret": 0.8,
            "Illegal": 0.1, "Forced": 0.05, "Forgery": 0.01,
            "Nantoi": 0.02, "Dulca": 0.02, "Murianu": 0.02,
            "semnatura indescifrabila": 0.05  # Флаг фальсификации
        }
        weight = base
        content_lower = content.lower()
        title_lower = self.title.lower()
        for key, val in rules.items():
            if key.lower() in content_lower or key.lower() in title_lower:
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
                        content=node.content,
                        metadata=node.metadata)
        for p in parents:
            self.G.add_edge(p, node.id)

    def generate_report(self):
        report = [f"--- A©TŌR LEGAL INTEGRITY REPORT | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ---"]
        total_weight = 0
        nodes = self.G.nodes(data=True)
        for n_id, data in nodes:
            status = "🛡️ VALID" if data['weight'] > 0.7 else "⚠️ TOXIC/FRAUD"
            report.append(f"{status} | ID: {n_id} | Title: {data['title']} | Weight: {data['weight']}")
            total_weight += data['weight']
        
        avg_integrity = (total_weight / len(nodes)) * 100
        report.append(f"\n--- SYSTEM INTEGRITY INDEX: {avg_integrity:.2f}% ---")
        return "\n".join(report)

auditor = LegalAuditor()
auditor.add_evidence(JusCogensNode("ROOT_JC", "UN Jus Cogens Protocol", "Fundamental International Law Integrity", 1.0))

# РЕАЛЬНЫЕ ДАННЫЕ РЕЕСТРА (Выборка 97 записей)
real_records = [
    {"id": "IMWM44AZGX6N6", "title": "Apostille #1", "sign": "Топорец Ирина", "date": "04.01.2021"},
    {"id": "CQ0VC27VGTCK6", "title": "Apostille #3", "sign": "Гонза Наталья", "date": "24.03.2021"},
    {"id": "5GTUD58SJQ5N6", "title": "Apostille #6", "sign": "Гузун Корнелиу", "date": "21.07.2009"},
    {"id": "DLTP7B8ZHWGQ7", "title": "Apostille #36", "sign": "semnatura indescifrabila", "date": "08.07.2022"},
    {"id": "CG0T6Y1TBUEL7", "title": "Apostille #41", "sign": "semnatura indescifrabila", "date": "12.07.2022"},
    {"id": "DFVMD2FQLW5N3", "title": "Apostille #68", "sign": "semnatura indescifrabila", "date": "14.12.2022"},
    {"id": "IMTQ930Z8U4N7", "title": "Apostille #69", "sign": "semnatura indescifrabila", "date": "05.10.2022"},
    {"id": "4J20E98WFY7J2", "title": "Apostille #90", "sign": "semnatura indescifrabila", "date": "03.10.2022"},
    {"id": "6OZUD89VBUEJ3", "title": "Apostille #93", "sign": "semnatura indescifrabila", "date": "01.11.2022"},
    {"id": "IHW093CZ8U8R7", "title": "Apostille #96", "sign": "semnatura indescifrabila", "date": "03.08.2022"}
]

for rec in real_records:
    auditor.add_evidence(JusCogensNode(rec['id'], rec['title'], f"Signatory: {rec['sign']}", metadata=rec), ["ROOT_JC"])

# Добавление Узлов Ответственности (Liability Nodes)
for target in [("NODE_NANTOI", "Nantoi Liudmila"), ("NODE_DULCA", "Dulca V.G."), ("NODE_MURIANU", "Murianu I.")]:
    auditor.add_evidence(JusCogensNode(target[0], target[1], f"Liability: {target[1]} systematic violation"), ["ROOT_JC"])

with open("audit_report.txt", "w", encoding="utf-8") as f:
    f.write(auditor.generate_report())

with open("legal_graph.json", "w", encoding="utf-8") as f:
    json.dump(nx.node_link_data(auditor.G), f, indent=4, ensure_ascii=False)
