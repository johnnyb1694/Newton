-- NB: commands below require the user to be a superuser (or, failing that, have the 'CREATEROLE' privilege)
CREATE ROLE newton WITH LOGIN;

CREATE DATABASE newton WITH OWNER newton;