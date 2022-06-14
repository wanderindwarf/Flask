drop table if exists entries;
create table entries (
  id serial primary key not null,
  date timestamp with time zone not null default now(),
  title varchar(80) not null,
  content text not null
);


-- The DROP TABLE command deletes a table from the database. All data in the table is lost forever. The IF EXISTS part
-- makes it so we won't get an error message if the table doesn't already exist. This command is necessary because the
-- following command, CREATE TABLE, will create the entries table from scratch.

-- The CREATE TABLE command creates a table in the database. Each one of the four lines specifies an attribute in the
-- table. The first part of the line specifies the name of the attribute (e.g., id, date, title, content), the second
-- part specifies the datatype (serial, timestamp, varchar(80), text), and any parts after the data type are extra
-- pieces of information. NOT NULL specifies that an attribute may not be null. PRIMARY KEY sets the attribute as the
-- primary key of the table. The DEFAULT part specifies the default value for a column. This means that when we add data
-- to the table using INSERT we can leave out any columns that have DEFAULT values.

-- The now() part is a special function that exists in PostgreSQL. DEFAULT now() means that the default value for the
-- date column will be the current time.