# genpark-messaging-recipe-automation-workflow-skill

> Declarative Recipe Automation Engine for Messaging Personal Agents. 100% Python Standard Library.

Distilled from **Poke**'s signature "Recipes" architecture, allowing users to express natural language automations as reactive event-condition-action pipelines without needing complex code.

## Architecture

```mermaid
flowchart LR
    Event["Incoming Event (Email / Calendar / SMS)"] --> Matcher["Event Type Matcher"]
    Matcher --> Filter["Condition Evaluator (Comparison / Thresholds)"]
    Filter -- Matched --> Render["Template Formatter"]
    Render --> ActionSeq["Action Dispatch (iMessage alert / API callback)"]
    ActionSeq --> AuditLog["Execution History & Audit"]
```

## Features
- **Zero-Dependency Engine**: Pure Python 3 rule evaluation.
- **Templated String Interpolation**: Seamlessly hydrates event data into customized notification messages.
- **Execution Audit Log**: Tracks invocation timestamps, parameters, and action results.
