CREATE TABLE candidate_data.candidate_info (
id SERIAL PRIMARY KEY,
name text not null,
age smallint not null,
party text not null,
birthplace text not null,
education text not null,
inclinacion_politica text not null);

CREATE TABLE parties (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    summary TEXT NOT NULL
);
