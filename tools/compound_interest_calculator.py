def _parse_number(value):
    if value is None:
        return None
    try:
        return float(str(value).strip().rstrip("%"))
    except Exception:
        return None


def execute(arguments: dict):
    principal = _parse_number(arguments.get("principal"))
    annual_rate = _parse_number(arguments.get("annual_rate") or arguments.get("rate"))
    times_per_year = arguments.get("times_per_year")
    years = _parse_number(arguments.get("years") or arguments.get("time"))

    if principal is None:
        return "Compound interest error: missing or invalid principal"

    if annual_rate is None:
        return "Compound interest error: missing or invalid annual_rate"

    if years is None:
        return "Compound interest error: missing or invalid years"

    try:
        times_per_year = int(times_per_year) if times_per_year is not None else 1
    except Exception:
        return "Compound interest error: times_per_year must be an integer"

    rate_decimal = annual_rate / 100.0
    amount = principal * (1 + rate_decimal / times_per_year) ** (times_per_year * years)
    interest = amount - principal

    return (
        f"With a principal of {principal}, annual rate of {annual_rate}% over {years} years "
        f"compounded {times_per_year} times per year, the final amount is {round(amount, 2)} "
        f"and interest earned is {round(interest, 2)}."
    )
