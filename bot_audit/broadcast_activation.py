import json

# Финальный реестр целей (G7 + EU + UN + Hague Depositary)
targets = {
    "EU_Commission": "@EU_Commission",
    "UN_HumanRights": "@UNHumanRights",
    "USA_StateDept": "@StateDept",
    "UK_FCDO": "@FCDOGovUK",
    "France_MFA": "@francediplo",
    "Germany_MFA": "@AuswaertigesAmt",
    "Hague_Sec": "@Hague_Convention",
    "Romania_MFA": "@MAERomania"
}

# Пейлоад: ст. 405-407 + ловушка "Timbru de Stat"
def generate_broadcast_msg(handle):
    return (f"URGENT {handle}: Case CASE-MACHERET-1997-2026. "
            "Financial blockade of justice by Moldova Court (Ref 2-3062/26). "
            "Violation of EU Association Arts 405-407. MinFinance is sole proper debtor. "
            "Evidence: https://arhiv1973b.github.io/apostille-legal-case/docs/notification/emergency_blockade.md")

activation_log = {target: generate_broadcast_msg(handle) for target, handle in targets.items()}

with open('bot_audit/broadcast_logs/active_payload.json', 'w') as f:
    json.dump(activation_log, f, indent=2)

print("Neuro-Notification Payload Generated.")
