DROP TABLE IF EXISTS staging.article;
DROP TABLE IF EXISTS main.article;
DROP TABLE IF EXISTS main.content;
DROP TABLE IF EXISTS reference.source;
DROP TABLE IF EXISTS reference.section;
DROP TABLE IF EXISTS reference.content_type;

DROP SCHEMA IF EXISTS staging;
DROP SCHEMA IF EXISTS main;
DROP SCHEMA IF EXISTS reference;

CREATE SCHEMA staging;
CREATE SCHEMA main;
CREATE SCHEMA reference;

CREATE TABLE staging.article (
    source TEXT,
    publication_date DATE,
    section TEXT,
    headline TEXT,
    abstract TEXT,
    body TEXT,
	uid TEXT
);

CREATE TABLE reference.source (
    source_id SERIAL PRIMARY KEY,
    source TEXT
);

CREATE TABLE reference.section (
    section_id SERIAL PRIMARY KEY,
    section TEXT
);

CREATE TABLE reference.content_type (
    content_type_id SERIAL PRIMARY KEY,
    content_type TEXT
);

CREATE TABLE main.article (
    article_id SERIAL PRIMARY KEY,
    publication_datetime DATE,
    source_id INTEGER,
    section_id INTEGER,
    CONSTRAINT article_source_id_fky FOREIGN KEY (source_id) REFERENCES reference.source (source_id),
    CONSTRAINT article_section_id_fky FOREIGN KEY (section_id) REFERENCES reference.section (section_id)
);

CREATE TABLE main.content (
    content_id SERIAL PRIMARY KEY,
    content TEXT,
    content_type_id INTEGER,
    article_id INTEGER,
    CONSTRAINT content_content_type_id_fky FOREIGN KEY (content_type_id) REFERENCES reference.content_type (content_type_id),
    CONSTRAINT content_article_id_fky FOREIGN KEY (article_id) REFERENCES main.article (article_id)
);
