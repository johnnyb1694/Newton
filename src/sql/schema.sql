DROP PROCEDURE IF EXISTS main.save(text);
DROP TABLE IF EXISTS staging.article;
DROP TABLE IF EXISTS main.content;
DROP TABLE IF EXISTS main.article;
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

INSERT INTO reference.content_type (content_type) VALUES ('headline'), ('abstract'), ('body');

CREATE TABLE main.article (
    article_id SERIAL PRIMARY KEY,
    publication_date DATE,
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

CREATE PROCEDURE main.save(
    staging_uid TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
	_source TEXT;
    _publication_date DATE;
    _section TEXT;
   	_source_id INT;
    _section_id INT;
    _article_id INT;
BEGIN

    IF EXISTS(
        SELECT 1 
        FROM main.content c 
        WHERE c.content = (SELECT a.headline FROM staging.article a WHERE a.uid = staging_uid)
    ) THEN
        RETURN;
    END IF;

    SELECT 
        a.source,
        a.publication_date,
        a.section
    INTO 
        _source,
        _publication_date,
        _section
    FROM staging.article a 
    WHERE a.uid = staging_uid;

    -- Source
    IF NOT EXISTS(SELECT 1 FROM reference.source WHERE source = _source) THEN
        INSERT INTO reference.source (source) 
        VALUES (_source) RETURNING source_id INTO _source_id;
    END IF;

    -- Section
    IF NOT EXISTS(SELECT 1 FROM reference.section WHERE section = _section) THEN
        INSERT INTO reference.section (section) 
        VALUES (_section) RETURNING section_id INTO _section_id;
    END IF;

    -- Article
    INSERT INTO main.article (publication_date, section_id, source_id) 
    VALUES (_publication_date, _section_id, _source_id) RETURNING article_id INTO _article_id;

    -- Content (Headline, Abstract and Body)
    IF (SELECT a.headline FROM staging.article a WHERE a.uid = staging_uid) IS NOT NULL THEN
        INSERT INTO main.content (content, content_type_id, article_id) 
        (
            SELECT a.headline, ct.content_type_id, _article_id 
            FROM staging.article a 
            LEFT JOIN reference.content_type ct ON ct.content_type = 'headline'
            WHERE a.uid = staging_uid
        );
    END IF;

    IF (SELECT a.abstract FROM staging.article a WHERE a.uid = staging_uid) IS NOT NULL THEN
        INSERT INTO main.content (content, content_type_id, article_id) 
        (
            SELECT a.abstract, ct.content_type_id, _article_id 
            FROM staging.article a 
            LEFT JOIN reference.content_type ct ON ct.content_type = 'abstract'
            WHERE a.uid = staging_uid
        );
    END IF;

    IF (SELECT a.body FROM staging.article a WHERE a.uid = staging_uid) IS NOT NULL THEN
        INSERT INTO main.content (content, content_type_id, article_id) 
        (
            SELECT a.body, ct.content_type_id, _article_id 
            FROM staging.article a 
            LEFT JOIN reference.content_type ct ON ct.content_type = 'body'
            WHERE a.uid = staging_uid
        );
    END IF;

END;
$$;

GRANT ALL ON PROCEDURE main.save TO newton;
