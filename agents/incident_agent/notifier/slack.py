def notify(payload: dict, channel: str = "#incidents") -> str:
    msg = f"[MOCK-SLACK] {payload['incident_id']} -> {channel} breaches={len(payload['breaches'])}"
    print(msg)
    return msg