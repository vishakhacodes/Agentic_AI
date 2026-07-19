from .calculator import execute as calculator
from .time_tool import execute as time
from .weather import execute as weather
from .geocoding_converter import execute as geocoding_converter
from .unit_converter import execute as unit_converter
from .compound_interest_calculator import execute as compound_interest_calculator
from .web_search import execute as web_search
from .translation import execute as translation

TOOLS = {
    "calculator": calculator,
    "time": time,
    "weather": weather,
    "geocoding_converter": geocoding_converter,
    "unit_converter": unit_converter,
    "compound_interest_calculator": compound_interest_calculator,
    "web_search": web_search,
    "translation": translation,
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"Unknown tool: {tool_name}"
    return tool(arguments)


def list_table():
    return list(TOOLS.keys())


if __name__ == "__main__":
    print("Registered tools\n")
    print(execute_tool("calculator", {"expression": "25*10"}))
    print("\n")
    print(execute_tool("time", {}))
    print(execute_tool("weather", {"city":"delhi"}))
    print(execute_tool("geocoding_converter", {"location":"Eiffel Tower"}))
    print(execute_tool("unit_converter", {"from_value":100, "from_unit":"km", "to_unit":"mi"}))
    print(execute_tool("compound_interest_calculator", {"principal":1000, "annual_rate":5, "times_per_year":12, "years":10}))