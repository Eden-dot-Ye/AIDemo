-- Delete existing data
DELETE FROM work_item_details;
DELETE FROM work_item_schedule;
DELETE FROM workflow_tracking;
DELETE FROM work_item_notes;
DELETE FROM related_items;
DELETE FROM audit_trail;
DELETE FROM work_items;

-- Reset identity columns
DBCC CHECKIDENT ('work_items', RESEED, 0);
DBCC CHECKIDENT ('work_item_details', RESEED, 0);
DBCC CHECKIDENT ('work_item_schedule', RESEED, 0);
DBCC CHECKIDENT ('workflow_tracking', RESEED, 0);
DBCC CHECKIDENT ('work_item_notes', RESEED, 0);
DBCC CHECKIDENT ('related_items', RESEED, 0);
DBCC CHECKIDENT ('audit_trail', RESEED, 0);

-- Insert work items
INSERT INTO work_items (description, completion_event, sequence_number, type, reminder, status, staff, assigned_group, capability, low_estimate, factor, high_estimate, std_estimate, estimated_complete, completed_local, estimated_handover)
VALUES 
('Investigate', 'INT', 1, 'INT', NULL, 'CLS', 'EY', NULL, NULL, 0, 2, 0, 0, '2025-07-24 22:06:00', '2025-07-24 22:06:00', NULL),
('Coding Unit Test', 'CTC', 2, 'CTC', NULL, 'CLS', 'EY', NULL, NULL, 0, 2, 0, 0, '2025-07-24 22:06:00', '2025-07-24 22:06:00', NULL),
('Coding function', 'CTC', 3, 'CTC', NULL, 'CLS', 'EY', NULL, NULL, 0, 2, 0, 0, '2025-07-24 22:07:00', '2025-07-24 22:07:00', NULL),
('Review', 'CBR', 4, 'CBR', NULL, 'ASN', 'EY', NULL, NULL, 0, 2, 0, 0, NULL, NULL, NULL);

-- Insert work item details
INSERT INTO work_item_details (work_item_id, summary, description_text)
VALUES 
(1, 'When opening a new Screen in Cargowise', 'EY 02-Jul-25 18:58 GMT+08:00: 
Reproduction: open a Shippment, maximize the form, then close it, then open it again, you will find that its size becomes the default size (Incident says it is a smaller size, but it is actually the default size)
Cause: Assuming the current screen resolution is 3440 x 1380. after maximizing the form, the actual size is (-9, -9, 3449, 1389), which exceeds the current local screen size (0, 0, 3440, 1380), resulting in EnterpriseFormLookStrategy.RestoreJustPositionAndSize that the need to restore the formRect is invalid, so the return of the default size
Solution: Since the logic of maximizing the form will already be in the RestoreFormLayout, and can handle the case where the form exceeds the screen size, I chose to add the check in this case, and the original logic is to let it return to the initial size when restoring, but I think a better way is to avoid recording the wrong size when writing to the cache
'),
(2, 'Screen not open on a right display - RDP version', 'This is a unit test for the function that restores the form layout in Cargowise. The test ensures that the form is restored to its previous position and size when opened on a different monitor or display.'),
(3, '[Tier 3] Restore the page in the previous position.', 'Function implementation description'),
(4, 'Review Summary', 'Code review description');

-- Insert work item schedule
INSERT INTO work_item_schedule (work_item_id, low_est_duration, est_variation_factor, high_est_duration, actual_duration, interruptible, workflow)
VALUES 
(1, '00:00:00', 2.0, '00:00:00', '00:00:01', 0, NULL),
(2, '00:30:00', 2.0, '01:00:00', '00:25:00', 0, NULL),
(3, '01:00:00', 2.0, '02:00:00', '01:15:00', 0, NULL),
(4, '00:15:00', 2.0, '00:30:00', NULL, 1, NULL);

-- Insert workflow tracking
INSERT INTO workflow_tracking (work_item_id, task_name, task_type, task_status, assigned_to, created_date, completed_date, duration, notes)
VALUES 
(1, 'Investigation Task', 'Analysis', 'Completed', 'CargoWise Support', '2025-07-24 20:00:00', '2025-07-24 22:06:00', '00:00:01', 'Investigation completed successfully'),
(2, 'Unit Test Development', 'Development', 'Completed', 'CargoWise Support', '2025-07-24 20:30:00', '2025-07-24 22:06:00', '00:25:00', 'Unit tests implemented'),
(3, 'Function Implementation', 'Development', 'Completed', 'CargoWise Support', '2025-07-24 21:00:00', '2025-07-24 22:07:00', '01:15:00', 'Function coding completed'),
(4, 'Code Review', 'Review', 'In Progress', 'CargoWise Support', '2025-07-24 22:00:00', NULL, NULL, 'Review in progress');

-- Insert work item notes
INSERT INTO work_item_notes (work_item_id, note_text, created_by, created_date)
VALUES 
(1, '1)What is the business impact? 
Local/Global, how often could a customer experience it during their daily operations?
2)Based on the business impact, what is the appropriate criticality in order to deliver the patch in a timely manner? 
(CR1-3 WI deliver patches immediately, upon completion, CR4 wait for the next weekly release, on a Friday)
3)What are the conditions under which the defect is reproduced? 
Document it and reference the document as a link below
4)Is there a workaround? 
Document it and provide clear information.
5)Provide the standard response that you wish our customer to receive for this issue "referencing the WTA links that may be required by the customers" .', 'CargoWise Support', '2025-07-24 22:07:00'),
(2, 'Unit tests created for all main functions', 'CargoWise Support', '2025-07-24 21:30:00'),
(3, 'M.K. 18-Jul-25 06:00 GMT+08:00:
Situation: I use laptop in office and at home connected to monitors with different size.
If form was open and layout saved on bigger monitor, and then I opened same form when connected to smaller monitor, then without this code form will be out of bounds - partially visible, or depending on new monitor layout form may be fully invisible.
Suggested solution: still check that form is in screen bounds, and if not then:
if form is maximized - adjust its size and position to related screen sizes (with correct dpi scaling);
if form is not maximized - reset its bounds to default (Rectangle.Empty).

EY 20-Jul-25 06:00 GMT+08:00:
After investigation, I think this will not happen. This is because in lines 230-236 of this file, it will re-process the form based on the current ScreenBounds information after applying the position and size of the cache, constraining it within the viewport.
Let say I have two Monitors right now, one with a size of (3440,1440) and one with a size of (1920,1280), and then I open a Form in the first Monitor and close it after placing it near the bottom-right corner (assuming that it is at this point in time with a size of (2000,1200) and left-top coordinates of (500,200)). Then disconnect the first Monitor and try to open it on the second Monitor. At this point the Form info will first be based on the Cache to get the size that needs to be applied as (2000,1200), with the left-top coordinates as (500, 200), but after checking the current screen info it realizes that this size is out of the screen range so it will constrain it back to the left-top of (0,0) and the size of (1920, 1200).
', 'CargoWise Support', '2025-07-24 22:00:00'),
(4, 'Pull Request Link: https://github.com/WiseTechGlobal/CargoWise/pull/1968', 'CargoWise Support', '2025-07-24 22:05:00');

-- Insert related items
INSERT INTO related_items (work_item_id, related_item_id, relationship_type)
VALUES 
(2, 1, 'Depends On'),
(3, 1, 'Depends On'),
(4, 2, 'Depends On');

-- Insert audit trail
INSERT INTO audit_trail (work_item_id, action_type, field_name, old_value, new_value, changed_by, changed_date, comments)
VALUES 
(1, 'Status Change', 'status', 'ASN', 'CLS', 'CargoWise Support', '2025-07-24 22:06:00', 'Investigation completed'),
(2, 'Status Change', 'status', 'ASN', 'CLS', 'CargoWise Support', '2025-07-24 22:06:00', 'Unit testing completed'),
(3, 'Status Change', 'status', 'ASN', 'CLS', 'CargoWise Support', '2025-07-24 22:07:00', 'Function coding completed'),
(4, 'Assignment', 'assigned_to', NULL, 'CargoWise Support', 'CargoWise Support', '2025-07-24 22:00:00', 'Assigned for review');
