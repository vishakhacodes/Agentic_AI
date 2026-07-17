from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from tools import (
    calculator,
    time,
    weather,
    geocoding_converter,
    unit_converter,
    compound_interest_calculator,
)


class Agent:

    def run(self, user_input: str) -> str:

        memory = load_memory()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        messages.extend(memory)
        messages.append({"role": "user", "content": user_input})

        llm_response = chat(messages)
        tool_request = parse_tool_call(llm_response)

        if tool_request is None:
            memory.append({"role": "user", "content": user_input})
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)
            return llm_response

        print("Tool Requested")
        tool_name = tool_request.get("tool")

        tool_handlers = {
            "calculator": lambda args: calculator({"expression": args.get("expression", "")} ),
            "time": lambda args: time({}),
            "weather": lambda args: weather({"city": args.get("city", "")} ),
            "geocoding_converter": lambda args: geocoding_converter({
                "location": args.get("location") or args.get("address") or args.get("query", "")
            }),
            "unit_converter": lambda args: unit_converter({
                "from_value": args.get("from_value") or args.get("value"),
                "from_unit": args.get("from_unit"),
                "to_unit": args.get("to_unit"),
            }),
            "compound_interest_calculator": lambda args: compound_interest_calculator({
                "principal": args.get("principal"),
                "annual_rate": args.get("annual_rate") or args.get("rate"),
                "times_per_year": args.get("times_per_year"),
                "years": args.get("years") or args.get("time"),
            }),
        }

        tool_result = tool_handlers.get(tool_name, lambda args: "Unknown tool.")(tool_request)

        print("Observation:", tool_result)

        final_messages = [
            {
                "role": "system",
                "content": """
You are a helpful AI assistant.

A tool has already executed.

DO NOT call the tool again.

DO NOT output JSON.

Use the tool result to answer the user's original question naturally.

Example:

User:
What is 7*7?

Tool Result:
49

Assistant:
The answer is 49.
"""
            },
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"Tool Result: {tool_result}"},
        ]

        final_response = chat(final_messages)

        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": final_response})
        save_memory(memory)

        return final_response