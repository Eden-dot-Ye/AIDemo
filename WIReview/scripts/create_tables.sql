-- Create database tables for the work item management system

-- Work Items table
CREATE TABLE work_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    description NVARCHAR(255),
    completion_event NVARCHAR(100),
    sequence_number INT,
    type NVARCHAR(10),
    reminder NVARCHAR(50),
    status NVARCHAR(10),
    staff NVARCHAR(50),
    assigned_group NVARCHAR(100),
    capability NVARCHAR(100),
    low_estimate DECIMAL(10,2),
    factor DECIMAL(5,2),
    high_estimate DECIMAL(10,2),
    std_estimate DECIMAL(10,2),
    estimated_complete DATETIME,
    completed_local DATETIME,
    estimated_handover DATETIME,
    created_date DATETIME DEFAULT GETDATE(),
    modified_date DATETIME DEFAULT GETDATE()
);

-- Work Item Details table
CREATE TABLE work_item_details (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    summary NVARCHAR(500),
    description_text NTEXT,
    created_date DATETIME DEFAULT GETDATE(),
    modified_date DATETIME DEFAULT GETDATE()
);

-- Work Item Schedule table
CREATE TABLE work_item_schedule (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    low_est_duration TIME,
    est_variation_factor DECIMAL(5,2),
    high_est_duration TIME,
    actual_duration TIME,
    interruptible BIT DEFAULT 0,
    workflow NVARCHAR(100),
    created_date DATETIME DEFAULT GETDATE(),
    modified_date DATETIME DEFAULT GETDATE()
);

-- Workflow Tracking table
CREATE TABLE workflow_tracking (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    task_name NVARCHAR(255),
    task_type NVARCHAR(50),
    task_status NVARCHAR(50),
    assigned_to NVARCHAR(100),
    created_date DATETIME DEFAULT GETDATE(),
    completed_date DATETIME,
    duration TIME,
    notes NTEXT
);

-- Work Item Notes table
CREATE TABLE work_item_notes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    note_text NTEXT,
    created_by NVARCHAR(100),
    created_date DATETIME DEFAULT GETDATE(),
    modified_date DATETIME DEFAULT GETDATE()
);

-- Related Items table
CREATE TABLE related_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    related_item_id INT FOREIGN KEY REFERENCES work_items(id),
    relationship_type NVARCHAR(50),
    created_date DATETIME DEFAULT GETDATE()
);

-- Audit Trail table
CREATE TABLE audit_trail (
    id INT IDENTITY(1,1) PRIMARY KEY,
    work_item_id INT FOREIGN KEY REFERENCES work_items(id),
    action_type NVARCHAR(50),
    field_name NVARCHAR(100),
    old_value NVARCHAR(500),
    new_value NVARCHAR(500),
    changed_by NVARCHAR(100),
    changed_date DATETIME DEFAULT GETDATE(),
    comments NTEXT
);
