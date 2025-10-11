CREATE TABLE candidate_data.candidate_info (
id SERIAL PRIMARY KEY,
name text not null,
age smallint not null,
party text not null,
birthplace text not null,
education text not null,
inclinacion_politica text not null);