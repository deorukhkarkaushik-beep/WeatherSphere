def rain_risk_advisory(probability: float) -> tuple[str, str]:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Rain probability must be between 0 and 1.")

    if probability < 0.25:
        return "Low", "Rain is unlikely; no rain-specific plans are needed."
    if probability < 0.50:
        return "Watch", "Showers are possible; keep an eye on local conditions."
    if probability < 0.75:
        return "Elevated", "Consider carrying an umbrella and allowing extra travel time."
    return "High", "Bring rain protection and plan for wet or slippery conditions."
