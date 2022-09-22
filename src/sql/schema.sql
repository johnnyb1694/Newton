DROP SCHEMA IF EXISTS staging;
DROP SCHEMA IF EXISTS main;
DROP SCHEMA IF EXISTS reference;

CREATE SCHEMA staging;
CREATE SCHEMA main;
CREATE SCHEMA reference;
GO

DROP TABLE IF EXISTS staging.Article;
DROP TABLE IF EXISTS main.Article;
DROP TABLE IF EXISTS main.Content;
DROP TABLE IF EXISTS reference.Source;
DROP TABLE IF EXISTS reference.Section;
DROP TABLE IF EXISTS reference.ContentType;
GO

CREATE TABLE staging.Article (
    source_id TEXT,
    source TEXT,
    publication_date DATE,
    section TEXT,
    headline TEXT,
    abstract TEXT,
    body TEXT
);
GO

CREATE TABLE reference.Source (
    SourceID SERIAL,
    Source TEXT
    UNIQUE(Source)
);

CREATE TABLE reference.Section (
    SectionID SERIAL
    Section TEXT
    UNIQUE(Section)
);

CREATE TABLE reference.ContentType (
    ContentTypeID SERIAL
    ContentType TEXT
    UNIQUE(ContentType)
);
GO

CREATE TABLE main.Article (
    ArticleID SERIAL,
    Headline TEXT,
    PublicationDate DATE,
    fkySourceID INTEGER,
    fkySectionID INTEGER,
    CONSTRAINT Article_ArticleID_pky PRIMARY KEY (ArticleID),
    CONSTRAINT Article_fkySourceID_fky FOREIGN KEY (fkySourceID) REFERENCES reference.Source (SourceID),
    CONSTRAINT Article_fkySectionID_fky FOREIGN KEY (fkySourceID) REFERENCES reference.Section (SectionID)
    UNIQUE(Headline, PublicationDate)
);
GO

CREATE TABLE main.Content (
    ContentID SERIAL,
    Content TEXT,
    fkyContentTypeID INTEGER,
    fkyArticleID INTEGER,
    CONSTRAINT Content_ContentID_pky PRIMARY KEY (ContentID),
    CONSTRAINT Content_fkyContentTypeID_fky FOREIGN KEY (fkyContentTypeID) REFERENCES reference.ContentType (ContentTypeID),
    CONSTRAINT Content_fkyArticleID_fky FOREIGN KEY (fkyArticleID) REFERENCES main.Article (ArticleID)
    UNIQUE(Content, fkyContentTypeID, fkyArticleID)
);
GO