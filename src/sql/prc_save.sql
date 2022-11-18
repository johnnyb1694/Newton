DROP PROCEDURE main.save(text);

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
    IF NOT EXISTS(SELECT 1 from reference.source where source = _source) THEN
        INSERT INTO reference.source (source) 
        VALUES (_source) RETURNING source_id INTO _source_id;
    END IF;

    -- Section
    IF NOT EXISTS(SELECT 1 from reference.section where section = _section) THEN
        INSERT INTO reference.section (section) 
        VALUES (_section) RETURNING section_id INTO _section_id;
    END IF;

    -- Article
    INSERT INTO main.article (publication_date, section_id, source_id) 
    VALUES (_publication_date, _section_id, _source_id) RETURNING article_id INTO _article_id;

    -- Content
    
    INSERT INTO main.content (content, content_type_id, article_id) 
    (
        SELECT a.headline, ct.content_type_id, _article_id 
        FROM staging.article a 
        LEFT JOIN reference.content_type ct ON ct.content_type = 'headline'
    );

    INSERT INTO main.content (content, content_type_id, article_id) 
    (
        SELECT a.abstract, ct.content_type_id, _article_id 
        FROM staging.article a 
        LEFT JOIN reference.content_type ct ON ct.content_type = 'abstract'
    );

    INSERT INTO main.content (content, content_type_id, article_id) 
    (
        SELECT a.body, ct.content_type_id, _article_id 
        FROM staging.article a 
        LEFT JOIN reference.content_type ct ON ct.content_type = 'body'
    );

END;
$$;

GRANT ALL ON PROCEDURE main.save TO newton;