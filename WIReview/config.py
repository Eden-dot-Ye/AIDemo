DB_SERVER = '47S1D44'
DB_USERNAME = 'Eden'
DB_NAME = 'OdysseyWIReview'
DB_PASSWORD = 'a46513'

DEEPSEEK_API_KEY = 'sk-311533ffaf944e43a96f1225977e72b8'
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

def get_deepseek_headers():
    return {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_work_item_details",
            "description": "Get specific work item details, return all fields, including description, completion_event, sequence_number, type, reminder, status, staff, assigned_group, capability, low_estimate, factor, high_estimate, std_estimate, estimated_complete, completed_local, estimated_handover, summary, description_text, workflow",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "work item ID"
                    }
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_work_item_workflow",
            "description": "Get specific work item workflow, return all fields, including task_name, task_type, task_status, assigned_to, created_date, completed_date, notes",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "work item ID"
                    }
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_related_items",
            "description": "Get specific work item details, return all fields, including work_item_id, related_description, relationship_type, related_status",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "work item ID"
                    }
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_work_item_details_with_notes",
            "description": "Get specific work item details and notes, return all fields, including details (same with `get_work_item_details`) and notes (note_text)",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "work item ID"
                    }
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pr_csharp_code",
            "description": "Get C# core code for a specific Pull Request, return code as a string",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "work item ID"
                    }
                },
                "required": ["item_id"]
            }
        }
    }
]