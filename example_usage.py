from client import MessagingRecipeWorkflowEngine

engine = MessagingRecipeWorkflowEngine()

# Register a recipe: When flight delayed > 30m, alert via text and reschedule dinner
engine.register_recipe(
    "RECIPE_FLIGHT",
    "Flight Delay Auto-Alert",
    trigger_event="flight_update",
    conditions={"delay_minutes": {"gte": 30}},
    actions=[
        {"action": "send_imessage", "template": "Notice: Flight {flight_no} delayed by {delay_minutes} min."},
        {"action": "adjust_reservation", "template": "Shift restaurant reservation by {delay_minutes} min."}
    ]
)

# Ingest event
results = engine.ingest_event("flight_update", {
    "flight_no": "DL449",
    "delay_minutes": 40
})

print(f"Executed {len(results)} recipes:")
for r in results:
    for a in r["actions_taken"]:
        print(f" - [{a['action']}] {a['result']}")
