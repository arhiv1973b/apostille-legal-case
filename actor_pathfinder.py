import networkx as nx
import hashlib
import datetime

class JusCogensNode:
    def __init__(self, id, title, content, weight=0.5):
        self.id = id
        self.title = title
        self.content = content
        self.weight = self.evaluate_semantics(content, weight)
        self.hash = hashlib.sha256(content.encode()).hexdigest()

    def evaluate_semantics(self, content, base):
        # АВТОМАТИЧЕСКИЙ ВЕС: ПРИОРИТЕТ МЕЖДУНАРОДНОГО ПРАВА
        rules = {
            "Jus Cogens": 1.0, "ECHR": 0.9, "Torture": 1.0,
            "Rehabilitation": 0.95, "Illegal Arrest": 0.1, 
            "Forced": 0.05, "Forgery": 0.01, "Macheret": 0.8
        }
        weight = base
        for key, val in rules.items():
            if key.lower() in content.lower():
                weight = max(weight, val) if val > 0.5 else min(weight, val)
        return weight

class LegalAuditor:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_evidence(self, node, parents=[]):
        self.G.add_node(node.id, title=node.title, weight=node.weight, hash=node.hash)
        for p in parents:
            self.G.add_edge(p, node.id)

    def generate_report(self, start, end):
        try:
            path = nx.shortest_path(self.G, source=start, target=end, weight='weight')
            report = [f"--- LEGAL INTEGRITY REPORT: {datetime.date.today()} ---"]
            for n_id in path:
                n = self.G.nodes[n_id]
                marker = "🛡️" if n['weight'] > 0.7 else "⚠️"
                report.append(f"{marker} ID: {n_id} | Title: {n['title']} | Weight: {n['weight']}")
            return "\n".join(report)
        except:
            return "❌ CRITICAL: LEGAL CHAIN DISRUPTED"

# Инициализация графа CASE-MACHERET-1997-2026
auditor = LegalAuditor()
auditor.add_evidence(JusCogensNode("NODE_1997", "Base Evidence", "Primary Jus Cogens Documents 1997", 1.0))
auditor.add_evidence(JusCogensNode("NODE_2009", "Toxic Event", "Forced Illegal Arrest 2009", 0.1), ["NODE_1997"])
auditor.add_evidence(JusCogensNode("NODE_2026", "Final Victory", "ECHR Judgment and Rehabilitation", 1.0), ["NODE_2009"])

with open("audit_report.txt", "w", encoding="utf-8") as f:
    f.write(auditor.generate_report("NODE_1997", "NODE_2026"))
