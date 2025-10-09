-- Start transaction
BEGIN;

-- Insert first employee
INSERT INTO my_table (column1, column2) VALUES ('John Doe', 4321);

-- Insert second employee, but only commit if first insert succeeded
INSERT INTO my_table (column1, column2) VALUES ('Jane Doe', 5432);
IF (SELECT COUNT(*) FROM my_table WHERE column2 = 1) > 0 THEN
  -- Both inserts were successful, so commit changes
  COMMIT;
ELSE
  -- Rollback any changes made during this transaction
  ROLLBACK;
END IF;

-- If we reach this point, all changes will be automatically committed or rolled back at the end of the transaction


