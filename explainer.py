

def explain_anomaly(voltage: float, current: float, power: float, severity: str) -> str:

    if voltage > 250:
        issue = f"Overvotage detectedat {voltage:.1f}V (normal: 200-240V)"
        action = "Check the power supply and voltage regulator immediately"
    elif voltage < 200:
        issue = f"Undervotage detectedat {voltage:.1f}V (normal: 200-240V)"
        action = "Check the power supply and voltage regulator immediately"
    elif power > 3000:
        issue = f"Abnormal power consumption at  {power:.1f}W "
        action = "Check the short circuits or unexpected load increases."
    else:
        issue = f"Abnormaly detected with severity: {severity}"
        action = "Inspect the system for unusual behavior."

    return f"{issue}. {action}"
