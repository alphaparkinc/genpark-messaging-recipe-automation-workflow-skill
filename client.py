"""Messaging Recipe Workflow Engine.
100% Python Standard Library.
"""

import time

class MessagingRecipeWorkflowEngine:
    """Compiles and executes declarative trigger-condition-action recipes for personal agents."""
    def __init__(self):
        self.recipes = {}
        self.execution_log = []

    def register_recipe(self, recipe_id, name, trigger_event, conditions, actions):
        self.recipes[recipe_id] = {
            "name": name,
            "trigger_event": trigger_event,
            "conditions": conditions,
            "actions": actions,
            "run_count": 0
        }

    def ingest_event(self, event_type, payload):
        fired = []
        for rid, recipe in self.recipes.items():
            if recipe["trigger_event"] != event_type:
                continue
            
            match = True
            for field, expected in recipe["conditions"].items():
                val = payload.get(field)
                if isinstance(expected, dict) and "gte" in expected:
                    if val is None or val < expected["gte"]:
                        match = False; break
                elif val != expected:
                    match = False; break
            
            if match:
                executed_actions = []
                for act in recipe["actions"]:
                    rendered = act["template"].format(**payload)
                    executed_actions.append({"action": act["action"], "result": rendered})
                
                recipe["run_count"] += 1
                record = {
                    "recipe_id": rid,
                    "event_type": event_type,
                    "actions_taken": executed_actions,
                    "timestamp": time.time()
                }
                self.execution_log.append(record)
                fired.append(record)
        return fired
