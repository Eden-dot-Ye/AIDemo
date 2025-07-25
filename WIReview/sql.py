import pyodbc
import os
from datetime import datetime
from config import DB_SERVER, DB_USERNAME, DB_NAME, DB_PASSWORD

class DatabaseManager:
    def __init__(self):
        # Database connection parameters
        # You'll need to set these environment variables or modify with your actual connection details
        
        self.server = DB_SERVER
        self.username = DB_USERNAME
        self.database = DB_NAME
        self.password = DB_PASSWORD
        
        # Connection string
        self.connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};TrustServerCertificate=yes'
    
    def get_connection(self):
        """Get database connection"""
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    def get_work_items(self):
        """Get all work items for the main list"""
        query = """
        SELECT 
            wi.id,
            wi.description,
            wi.completion_event,
            wi.sequence_number,
            wi.type,
            wi.reminder,
            wi.status,
            wi.staff,
            wi.assigned_group,
            wi.capability,
            wi.low_estimate,
            wi.factor,
            wi.high_estimate,
            wi.std_estimate,
            wi.estimated_complete,
            wi.completed_local,
            wi.estimated_handover
        FROM work_items wi
        ORDER BY wi.sequence_number
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching work items: {e}")
            return []
    
    def get_work_item_details(self, item_id):
        """Get detailed information for a specific work item"""
        query = """
        SELECT 
            wi.*,
            wd.summary,
            wd.description_text,
            ws.low_est_duration,
            ws.est_variation_factor,
            ws.high_est_duration,
            ws.actual_duration,
            ws.interruptible,
            ws.workflow
        FROM work_items wi
        LEFT JOIN work_item_details wd ON wi.id = wd.work_item_id
        LEFT JOIN work_item_schedule ws ON wi.id = ws.work_item_id
        WHERE wi.id = ?
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id,))
                columns = [column[0] for column in cursor.description]
                row = cursor.fetchone()
                if row:
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            print(f"Error fetching work item details: {e}")
            return None
    
    def get_workflow_tracking(self, item_id):
        """Get workflow tracking data"""
        query = """
        SELECT 
            wt.id,
            wt.task_name,
            wt.task_type,
            wt.task_status,
            wt.assigned_to,
            wt.created_date,
            wt.completed_date,
            wt.duration,
            wt.notes
        FROM workflow_tracking wt
        WHERE wt.work_item_id = ?
        ORDER BY wt.created_date DESC
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id,))
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching workflow tracking: {e}")
            return []
    
    def get_work_item_notes(self, item_id):
        """Get notes for a work item"""
        query = """
        SELECT 
            n.id,
            n.note_text,
            n.created_by,
            n.created_date,
            n.modified_date
        FROM work_item_notes n
        WHERE n.work_item_id = ?
        ORDER BY n.created_date DESC
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id,))
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching notes: {e}")
            return []
    
    def get_related_items(self, item_id):
        """Get related work items"""
        query = """
        SELECT 
            ri.work_item_id,
            wd.summary as related_description,
            ri.relationship_type,
            wi.status as related_status
        FROM related_items ri
        JOIN work_items wi ON ri.work_item_id = wi.id
        JOIN work_item_details wd ON wi.id = wd.work_item_id
        WHERE ri.related_item_id = ?
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id,))
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching related items: {e}")
            return []
    
    def get_audit_data(self, item_id):
        """Get audit trail data"""
        query = """
        SELECT 
            a.id,
            a.action_type,
            a.field_name,
            a.old_value,
            a.new_value,
            a.changed_by,
            a.changed_date,
            a.comments
        FROM audit_trail a
        WHERE a.work_item_id = ?
        ORDER BY a.changed_date DESC
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id,))
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching audit data: {e}")
            return []
    
    def get_filter_options(self):
        """Get options for filter dropdowns"""
        queries = {
            'types': "SELECT DISTINCT type FROM work_items WHERE type IS NOT NULL",
            'statuses': "SELECT DISTINCT status FROM work_items WHERE status IS NOT NULL",
            'staff': "SELECT DISTINCT staff FROM work_items WHERE staff IS NOT NULL",
            'groups': "SELECT DISTINCT assigned_group FROM work_items WHERE assigned_group IS NOT NULL"
        }
        
        results = {}
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for key, query in queries.items():
                    cursor.execute(query)
                    results[key] = [row[0] for row in cursor.fetchall()]
                return results
        except Exception as e:
            print(f"Error fetching filter options: {e}")
            return {}

    def get_task_details(self, item_id, task_id):
        """Get detailed information for a specific task"""
        query = """
        SELECT 
            wt.*,
            ws.low_est_duration,
            ws.est_variation_factor,
            ws.high_est_duration,
            ws.actual_duration,
            ws.interruptible,
            ws.workflow
        FROM workflow_tracking wt
        LEFT JOIN work_item_schedule ws ON wt.work_item_id = ws.work_item_id
        WHERE wt.work_item_id = ? AND wt.id = ?
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id, task_id))
                columns = [column[0] for column in cursor.description]
                row = cursor.fetchone()
                if row:
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            print(f"Error fetching task details: {e}")
            return None

    def get_task_notes(self, item_id, task_id):
        """Get notes for a specific task"""
        query = """
        SELECT 
            tn.id,
            tn.note_text,
            tn.created_by,
            tn.created_date,
            tn.modified_date
        FROM task_notes tn
        WHERE tn.work_item_id = ? AND tn.task_id = ?
        ORDER BY tn.created_date DESC
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (item_id, task_id))
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error fetching task notes: {e}")
            return []

    def get_comprehensive_work_item_data(self, item_id):
        """Get comprehensive work item data for AI analysis"""
        try:
            # Get basic work item details
            work_item = self.get_work_item_details(item_id)
            if not work_item:
                return None
            
            # Get related data
            tasks = self.get_workflow_tracking(item_id)
            notes = self.get_work_item_notes(item_id)
            audit_trail = self.get_audit_data(item_id)
            related_items = self.get_related_items(item_id)
            
            # Combine all data
            comprehensive_data = {
                **work_item,
                'tasks': tasks,
                'notes': notes,
                'audit_trail': audit_trail,
                'related_items': related_items
            }
            
            return comprehensive_data
            
        except Exception as e:
            print(f"Error fetching comprehensive work item data: {e}")
            return None
