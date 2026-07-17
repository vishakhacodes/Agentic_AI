def execute(arguments: dict):
    age = arguments.get("age")
    intensity = arguments.get("intensity")

    if age is None:
        return "Heart rate error: missing age"

    try:
        age = float(age)
    except Exception:
        return "Heart rate error: age must be a number"

    max_hr = 220 - age
    intensity_label = ""
    target_min = None
    target_max = None

    if intensity is None:
        target_min = max_hr * 0.5
        target_max = max_hr * 0.85
        intensity_label = "general target zone"
    else:
        if isinstance(intensity, str):
            intensity_lower = intensity.strip().lower()
            if intensity_lower in {"low", "easy"}:
                target_min, target_max = max_hr * 0.5, max_hr * 0.6
                intensity_label = "low intensity"
            elif intensity_lower in {"moderate", "medium"}:
                target_min, target_max = max_hr * 0.6, max_hr * 0.75
                intensity_label = "moderate intensity"
            elif intensity_lower in {"high", "vigorous"}:
                target_min, target_max = max_hr * 0.75, max_hr * 0.85
                intensity_label = "high intensity"
            elif intensity_lower.endswith("%"):
                try:
                    percent = float(intensity_lower.rstrip("%")) / 100.0
                    target_min = target_max = max_hr * percent
                    intensity_label = f"{percent * 100:.0f}% intensity"
                except Exception:
                    return "Heart rate error: invalid intensity percentage"
            else:
                try:
                    percent = float(intensity_lower) / 100.0
                    target_min = target_max = max_hr * percent
                    intensity_label = f"{percent * 100:.0f}% intensity"
                except Exception:
                    return "Heart rate error: invalid intensity value"
        else:
            try:
                percent = float(intensity) / 100.0
                target_min = target_max = max_hr * percent
                intensity_label = f"{percent * 100:.0f}% intensity"
            except Exception:
                return "Heart rate error: invalid intensity value"

    target_min = round(target_min)
    target_max = round(target_max)

    if target_min == target_max:
        return (
            f"Maximum heart rate is {round(max_hr)} bpm. "
            f"Target heart rate at {intensity_label} is {target_min} bpm."
        )

    return (
        f"Maximum heart rate is {round(max_hr)} bpm. "
        f"Target heart rate for {intensity_label} is {target_min} to {target_max} bpm."
    )
