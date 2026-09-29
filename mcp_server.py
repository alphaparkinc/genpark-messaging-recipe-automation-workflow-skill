import sys
import json
from client import MessagingRecipeWorkflowEngine

engine = MessagingRecipeWorkflowEngine()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-messaging-recipe-automation-workflow-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "register_recipe",
                        "description": "Register a new reactive rule recipe with trigger, conditions, and actions",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "recipe_id": {"type": "string"},
                                "name": {"type": "string"},
                                "trigger_event": {"type": "string"},
                                "conditions": {"type": "object"},
                                "actions": {"type": "array"}
                            },
                            "required": ["recipe_id", "name", "trigger_event", "conditions", "actions"]
                        }
                    },
                    {
                        "name": "ingest_event",
                        "description": "Ingest an incoming event and fire matching automation recipes",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "event_type": {"type": "string"},
                                "payload": {"type": "object"}
                            },
                            "required": ["event_type", "payload"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "register_recipe":
            engine.register_recipe(args["recipe_id"], args["name"], args["trigger_event"], args["conditions"], args["actions"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Recipe registered"}]}}
        elif tool_name == "ingest_event":
            fired = engine.ingest_event(args["event_type"], args["payload"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(fired, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
