def _parse_number(value):
    if value is None:
        return None
    try:
        return float(str(value).strip())
    except Exception:
        return None


def execute(arguments: dict):
    value = _parse_number(arguments.get("from_value") or arguments.get("value"))
    from_unit = str(arguments.get("from_unit", "")).strip().lower()
    to_unit = str(arguments.get("to_unit", "")).strip().lower()

    if value is None:
        return "Unit converter error: missing or invalid from_value"

    if not from_unit or not to_unit:
        return "Unit converter error: both from_unit and to_unit are required"

    conversions = {
        ("km", "mi"): lambda x: x * 0.621371,
        ("mi", "km"): lambda x: x / 0.621371,
        ("m", "ft"): lambda x: x * 3.28084,
        ("ft", "m"): lambda x: x / 3.28084,
        ("cm", "in"): lambda x: x * 0.393701,
        ("in", "cm"): lambda x: x / 0.393701,
        ("kg", "lb"): lambda x: x * 2.20462,
        ("lb", "kg"): lambda x: x / 2.20462,
        ("g", "oz"): lambda x: x * 0.035274,
        ("oz", "g"): lambda x: x / 0.035274,
        ("c", "f"): lambda x: x * 9 / 5 + 32,
        ("f", "c"): lambda x: (x - 32) * 5 / 9,
        ("c", "k"): lambda x: x + 273.15,
        ("k", "c"): lambda x: x - 273.15,
        ("f", "k"): lambda x: (x - 32) * 5 / 9 + 273.15,
        ("k", "f"): lambda x: (x - 273.15) * 9 / 5 + 32,
        ("l", "ml"): lambda x: x * 1000,
        ("ml", "l"): lambda x: x / 1000,
        ("l", "cup"): lambda x: x * 4.22675,
        ("cup", "l"): lambda x: x / 4.22675,
        ("km/h", "mph"): lambda x: x * 0.621371,
        ("mph", "km/h"): lambda x: x / 0.621371,
        ("m/s", "km/h"): lambda x: x * 3.6,
        ("km/h", "m/s"): lambda x: x / 3.6,
    }

    converter = conversions.get((from_unit, to_unit))
    if converter is None:
        return (
            f"Unit converter error: unsupported conversion from {from_unit} to {to_unit}. "
            "Supported conversions include km<->mi, m<->ft, cm<->in, kg<->lb, g<->oz, "
            "C<->F, C<->K, L<->mL, L<->cup, km/h<->mph, m/s<->km/h."
        )

    result = converter(value)
    result = round(result, 6)

    return f"{value} {from_unit} = {result} {to_unit}"
