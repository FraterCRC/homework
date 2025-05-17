CREATE DATABASE dev;

CREATE TABLE public.users (
	id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	username text NOT NULL,
	password text NOT NULL,
	first_name text,
	last_name text,
	birth_date Date,
	gender text,
	hobbies text,
	city text
);
