# Function calling end to end: schema -> model emits JSON -> validate -> execute -> return result or error.
import json

TOOLS = {
    "get_fx_rate": {
        "description": "Get the spot FX rate for a currency pair, e.g. EURUSD.",
        "parameters": {"type": "object", "required": ["pair"],
                       "properties": {"pair": {"type": "string", "pattern": "^[A-Z]{6}$"}}},
        "fn": lambda pair: {"pair": pair, "rate": {"EURUSD": 1.08, "GBPUSD": 1.27}[pair]},
    }
}

def validate(args, schema):
    import re
    for req in schema["required"]:
        if req not in args: return f"missing required argument '{req}'"
    for k, v in args.items():
        spec = schema["properties"].get(k)
        if spec is None: return f"unknown argument '{k}'"
        if spec["type"] == "string" and not isinstance(v, str): return f"'{k}' must be a string"
        if "pattern" in spec and not re.fullmatch(spec["pattern"], v):
            return f"'{k}'={v!r} must match {spec['pattern']} (e.g. EURUSD)"
    return None

def run_tool_call(raw):
    call = json.loads(raw)
    tool = TOOLS.get(call["name"])
    if tool is None: return {"error": f"no tool named {call['name']}; available: {list(TOOLS)}"}
    err = validate(call["arguments"], tool["parameters"])
    if err: return {"error": err}                  # returned to the model so it can self-correct
    return tool["fn"](**call["arguments"])

# What the model might emit (first attempt malformed, second corrected after seeing the error)
for raw in ['{"name": "get_fx_rate", "arguments": {"pair": "eur/usd"}}',
            '{"name": "get_fx_rate", "arguments": {"pair": "EURUSD"}}']:
    print(raw, "\n  ->", run_tool_call(raw))
