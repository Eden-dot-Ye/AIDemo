from decimal import Decimal
import re
from flask import Flask, render_template, jsonify
from sql import DatabaseManager
import json
import requests
from datetime import datetime, time

from fastmcp import FastMCP
from config import DEEPSEEK_API_URL, get_deepseek_headers, tools

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

from fastmcp import FastMCP

mcp = FastMCP("WI AI Review")

# Initialize database manager
db_manager = DatabaseManager()

@app.route('/')
def index():
    """Main page with work item interface"""
    return render_template('index.html')

@app.route('/api/work-items')
def get_work_items():
    """Get work items list"""
    try:
        work_items = db_manager.get_work_items()
        return jsonify({'success': True, 'data': work_items})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>')
def get_work_item_details(item_id):
    """Get specific work item details"""
    try:
        details = db_manager.get_work_item_details(item_id)
        return jsonify({'success': True, 'data': details})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/workflow')
def get_work_item_workflow(item_id):
    """Get workflow tracking data"""
    try:
        workflow = db_manager.get_workflow_tracking(item_id)
        return jsonify({'success': True, 'data': workflow})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/notes')
def get_work_item_notes(item_id):
    """Get work item notes"""
    try:
        notes = db_manager.get_work_item_notes(item_id)
        return jsonify({'success': True, 'data': notes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/related')
def get_related_items(item_id):
    """Get related items"""
    try:
        related = db_manager.get_related_items(item_id)
        return jsonify({'success': True, 'data': related})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/audit')
def get_audit_data(item_id):
    """Get audit data"""
    try:
        audit = db_manager.get_audit_data(item_id)
        return jsonify({'success': True, 'data': audit})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/filters')
def get_filter_options():
    """Get filter options for dropdowns"""
    try:
        filters = db_manager.get_filter_options()
        return jsonify({'success': True, 'data': filters})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/task/<int:task_id>')
def get_task_details(item_id, task_id):
    """Get specific task details within a work item"""
    try:
        details = db_manager.get_task_details(item_id, task_id)
        return jsonify({'success': True, 'data': details})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/task/<int:task_id>/notes')
def get_task_notes(item_id, task_id):
    """Get notes for a specific task"""
    try:
        notes = db_manager.get_task_notes(item_id, task_id)
        return jsonify({'success': True, 'data': notes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/work-item/<int:item_id>/details-with-notes')
def get_work_item_details_with_notes(item_id):
    """Get work item details along with notes for the details tab"""
    try:
        details = db_manager.get_work_item_details(item_id)
        notes = db_manager.get_work_item_notes(item_id)
        
        result = {
            'details': details,
            'notes': notes
        }
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
# ----------------------- Split for AI Review -----------------------

def convert_datetime_to_str(data):
    if isinstance(data, dict):
        return {k: convert_datetime_to_str(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [convert_datetime_to_str(item) for item in data]
    elif isinstance(data, (datetime, time)):
        return data.isoformat()
    return data

def sanitize_json(data):
    if isinstance(data, Decimal):
        return float(data)
    if isinstance(data, (datetime, time)):
        return data.isoformat()
    if isinstance(data, dict):
        return {k: sanitize_json(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [sanitize_json(item) for item in data]
    return data

def process_markdown(text):
    result = text

    result = re.sub(r'^### (.+)$', r'<h3><strong>\1</strong></h3>', result, flags=re.MULTILINE)
    result = re.sub(r'^## (.+)$', r'<h2><strong>\1</strong></h2>', result, flags=re.MULTILINE)
    result = re.sub(r'^# (.+)$', r'<h1><strong>\1</strong></h1>', result, flags=re.MULTILINE)
    result = re.sub(r'\*\*\[([^\]]+)\]\(([^)]+)\)\*\*', r'<strong><a href="\2" target="_blank">\1</a></strong>', result)
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', result)
    result = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', result)
    result = result.replace('\n', '<br>')
    
    return result

@mcp.tool()
def get_work_item_details(item_id):
    """Get specific work item details"""
    details = get_work_item_details_impl(item_id)
    return details

def get_work_item_details_impl(item_id):
    """Get specific work item details"""
    details = db_manager.get_work_item_details(item_id)
    details = convert_datetime_to_str(details)
    return "\n".join(details)

@mcp.tool()        
def get_work_item_workflow(item_id):
    """Get workflow tracking data"""
    workflow = get_work_item_workflow_impl(item_id)
    return workflow

def get_work_item_workflow_impl(item_id):
    """Get workflow tracking data"""
    workflow = db_manager.get_workflow_tracking(item_id)
    workflow = convert_datetime_to_str(workflow)
    return "\n".join(workflow)

@mcp.tool()        
def get_related_items(item_id):
    """Get related items"""
    related = get_related_items_impl(item_id)
    return related

def get_related_items_impl(item_id):
    """Get related items"""
    related = db_manager.get_related_items(item_id)
    related = convert_datetime_to_str(related)
    return "\n".join(related)

@mcp.tool()
def get_work_item_details_with_notes(item_id):
    """Get work item details along with notes for the details tab"""
    result = get_work_item_details_with_notes_impl(item_id)
    return result

def get_work_item_details_with_notes_impl(item_id):
    """Get work item details along with notes for the details tab"""
    details = db_manager.get_work_item_details(item_id)
    notes = db_manager.get_work_item_notes(item_id)
    details = convert_datetime_to_str(details)
    notes = convert_datetime_to_str(notes)
    
    result = {
        'details': details,
        'notes': notes
    }
    return "\n".join([json.dumps(result, indent=2, ensure_ascii=False)])

@mcp.tool()
def get_pr_csharp_code(item_id):
    """Return Pull Request code"""
    return get_pr_csharp_code_impl(item_id)

def get_pr_csharp_code_impl(item_id):
    """Return Pull Request code"""
    return """if (formRect != Rectangle.Empty && !CachedScreenInfo.Instance.Contains(formRect) && form.WindowState != FormWindowState.Maximized)
{
    // cache is invalid
    Enterprise.RemoteDesktopServices.Server.TrackingInfo.TrackingInfoLogger.Instance.NewLog(() =>
    {
        var sb = new StringBuilder();
        sb.AppendLine($"Invalid form area: {formRect}");
        sb.AppendLine($"Current screen work areas:");
        foreach (var screen in CachedScreenInfo.Instance.ScreenInfos)
        {
            sb.AppendLine($"    {screen}");
        }
        return sb.ToString();
    });Expand commentComment on lines R184 to R194ResolvedCode has comments. Press enter to view.
    formRect = Rectangle.Empty;
}
"""

def call_deepseek_with_tools(messages):
    headers = get_deepseek_headers()

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",
        "max_tokens": 2000,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_text = response.text
            raise Exception(f"Deepseek API call failed. {response.status_code} - {error_text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request to Deepseek API failed: {str(e)}")

def execute_fastmcp_tool_call(tool_call):
    function_name = tool_call["function"]["name"]
    arguments = json.loads(tool_call["function"]["arguments"])

    try:
        if function_name == "get_work_item_details":
            result = get_work_item_details_impl(
                item_id=arguments["item_id"]
            )
            return {
                "success": True,
                "data": result
            }
        elif function_name == "get_work_item_workflow":
            result = get_work_item_workflow_impl(
                item_id=arguments["item_id"]
            )
            return {
                "success": True,
                "data": result
            }
        elif function_name == "get_related_items":
            result = get_related_items_impl(
                item_id=arguments["item_id"]
            )
            return {
                "success": True,
                "data": result
            }
        elif function_name == "get_work_item_details_with_notes":
            result = get_work_item_details_with_notes_impl(
                item_id=arguments["item_id"]
            )
            return {
                "success": True,
                "data": result
            }
        elif function_name == "get_pr_csharp_code":
            result = get_pr_csharp_code_impl(
                item_id=arguments["item_id"]
            )
            return {
                "success": True,
                "data": result
            }

        else:
            return {
                "success": False,
                "error": f"Unknown tools.{function_name}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_ai_analysis(user_message):
    messages = [
        {
            "role": "system",
            "content": """You are a Work Item review helper that provides services based on the FastMCP framework. You have the following tools at your disposal:

1. get_work_item_details - Get specific work item details
2. get_work_item_workflow - Get workflow tracking data
3. get_related_items - Get related items
4. get_work_item_details_with_notes - Get work item details along with notes for the details tab
5. get_pr_csharp_code - Return Pull Request code

Policies for handling user queries:
You need to get the required item_id from use message and use the above five tools to get the overview and details for current work item, then analyse them to provide answer.
"""
        },
        {"role": "user", "content": user_message}
    ]

    response = call_deepseek_with_tools(messages)
    assistant_message = response["choices"][0]["message"]

    tool_calls = assistant_message.get("tool_calls", [])
    messages.append(assistant_message)

    if tool_calls:
        for tool_call in tool_calls:
            tool_result = execute_fastmcp_tool_call(tool_call).get("data", "")
            tool_result = sanitize_json(tool_result)
            # Convert tool_result (dict) to json format
            if isinstance(tool_result, dict):
                tool_result = json.dumps(tool_result, indent=2, ensure_ascii=False)
                
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            })

        try:
            final_response = call_deepseek_with_tools(messages)
            final_message = final_response["choices"][0]["message"]["content"]
            
            if not final_message or final_message.strip() == "":
                final_message = "Sorry, I was unable to generate an answer. Please try again later."

            return {
                "message": process_markdown(final_message),
                "tool_calls": tool_calls,
                "conversation": messages
            }
        except Exception as e:
            return {
                "message": f"The FastMCP tool was invoked successfully, but generated the final answer with the error. {str(e)}",
                "tool_calls": tool_calls,
                "conversation": messages
            }
    else:
        return {
            "message": assistant_message["content"],
            "tool_calls": None,
            "conversation": messages
        }

@app.route('/api/work-item/<int:item_id>/ai-review', methods=['POST'])
def perform_ai_review(item_id):
    """Perform AI review of work item using FastMCP"""
    item_id = 1  # For testing purposes, we use a fixed item_id
    try:
        # Get comprehensive work item data
        work_item_data = db_manager.get_comprehensive_work_item_data(item_id)
        
        if not work_item_data:
            return jsonify({'success': False, 'error': 'Work item not found'})
        
        # Call FastMCP for AI analysis
        ai_analysis = get_ai_analysis(f"Please review the work item with ID {item_id} and provide a detailed analysis.")
        
        # Call MCP tool for C# code example
        csharp_code = get_pr_csharp_code_impl(item_id)
        
        # Combine results
        review_results = {
            'ai_analysis': ai_analysis,
            'csharp_code': csharp_code,
            'timestamp': datetime.now().isoformat(),
            'work_item_id': item_id
        }
        
        return jsonify({'success': True, 'data': review_results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
