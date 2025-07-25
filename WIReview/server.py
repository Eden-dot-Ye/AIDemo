import asyncio
import sys
import os
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastmcp import FastMCP
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from sql import DatabaseManager

mcp = FastMCP("WI AI Review")

# Initialize database manager
db_manager = DatabaseManager()

@mcp.tool()
def get_work_item_details(item_id):
    """Get specific work item details"""
    details = db_manager.get_work_item_details(item_id)
    return details

@mcp.tool()        
def get_work_item_workflow(item_id):
    """Get workflow tracking data"""
    workflow = db_manager.get_workflow_tracking(item_id)
    return workflow

@mcp.tool()        
def get_related_items(item_id):
    """Get related items"""
    related = db_manager.get_related_items(item_id)
    return related

@mcp.tool()
def get_work_item_details_with_notes(item_id):
    """Get work item details along with notes for the details tab"""
    details = db_manager.get_work_item_details(item_id)
    notes = db_manager.get_work_item_notes(item_id)
    
    result = {
        'details': details,
        'notes': notes
    }
    return result

@mcp.tool()
def get_pr_csharp_code(item_id):
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

def main():
    mcp.run()

if __name__ == "__main__":
    main() 