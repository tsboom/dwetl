-- This SQL script terminates all active connections to the "usmai_dw_etl" database,
-- then drops the database.
--
-- WARNING: Using the SQL script will DESTROY all the data in the  "usmai_dw_etl" database.

-- Terminate active connections
-- See: https://dba.stackexchange.com/questions/11893/force-drop-db-while-others-may-be-connected

-- Make sure no one can connect to this database by updating the system catalog
UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'usmai_dw_etl';

-- Force disconnection of all clients connected to this database, using pg_terminate_backend
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'usmai_dw_etl';

-- DROP the usmai_dw_etl database
DROP DATABASE 'usmai_dw_etl'
