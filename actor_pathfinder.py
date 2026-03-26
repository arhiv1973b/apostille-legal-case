import networkx as nx
import hashlib
import json
import datetime

class JusCogensNode:
    def __init__(self, id, title, doc_date, apo_date, content, metadata=None):
        self.id = id
        self.title = title
        self.doc_date = self.parse_date(doc_date)
        self.apo_date = self.parse_date(apo_date)
        self.content = content
        self.metadata = metadata or {}
        
        # Вычисление временной аномалии (разрыв в днях)
        self.delay_days = (self.apo_date - self.doc_date).days if self.doc_date and self.apo_date else 0
        self.weight = self.evaluate_integrity(content)
        self.hash = hashlib.sha256(f"{id}{content}{self.delay_days}".encode()).hexdigest()

    def parse_date(self, date_str):
        for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%d-%m-%Y'):
            try: return datetime.datetime.strptime(date_str.strip(), fmt)
            except: continue
        return None

    def evaluate_integrity(self, content):
        rules = {
            "Jus Cogens": 1.0, "semnatura indescifrabila": 0.05,
            "Nantoi": 0.02, "Dulca": 0.02, "Murianu": 0.02
        }
        weight = 0.5
        for key, val in rules.items():
            if key.lower() in content.lower(): weight = min(weight, val) if val < 0.5 else max(weight, val)
        
        # ШТРАФ ЗА ВРЕМЕННУЮ АНОМАЛИЮ (v.11.6)
        if self.delay_days < 0: weight = 0.01  # Невозможно: апостиль раньше документа
        elif self.delay_days > 365 * 5: weight *= 0.5  # Задержка более 5 лет — признак симуляции
        
        return round(weight, 3)

class LegalAuditor:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_evidence(self, node, parents=[]):
        self.G.add_node(node.id, title=node.title, weight=node.weight, delay=node.delay_days)
        for p in parents: self.G.add_edge(p, node.id)

    def generate_report(self):
        nodes = self.G.nodes(data=True)
        report = [f"--- A©TŌR COURT REPORT (LUPAŞCU SESSION) | {datetime.date.today()} ---"]
        total_w = 0
        for n_id, data in nodes:
            status = "🛡️ VALID" if data['weight'] > 0.7 else "⚠️ TOXIC"
            report.append(f"{status} | {n_id} | Delay: {data['delay']} days | Weight: {data['weight']}")
            total_w += data['weight']
        report.append(f"\n--- GLOBAL INTEGRITY INDEX: {round((total_w/len(nodes))*100, 2)}% ---")
        return "\n".join(report)

auditor = LegalAuditor()
auditor.add_evidence(JusCogensNode("ROOT", "Jus Cogens", "01.01.1997", "01.01.1997", "Core principle"), [])

# РЕАЛЬНЫЕ ДАННЫЕ С АНОМАЛИЯМИ ИЗ РЕЕСТРА
records = [
    ("IMWM44AZGX6N6", "Apostille #1", "04.01.2021", "18.01.2021", "Toporet I."),
    ("DR4Y1584JW9F4", "Apostille #4", "12.11.2003", "05.04.2021", "Aliona Miron (17 YEAR DELAY)"),
    ("DLTP7B8ZHWGQ7", "Apostille #36", "08.07.2022", "08.07.2022", "semnatura indescifrabila"),
    ("4J20E98WFY7J2", "Apostille #90", "03.10.2022", "03.10.2022", "semnatura indescifrabila")
]

for rid, tit, d1, d2, cont in records:
    auditor.add_evidence(JusCogensNode(rid, tit, d1, d2, cont), ["ROOT"])

with open("audit_report.txt", "w", encoding="utf-8") as f:
    f.write(auditor.generate_report())
