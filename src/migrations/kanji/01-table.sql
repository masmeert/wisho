--- requires: entry.01-table.sql
CREATE SEQUENCE __SCHEMA__.kanji_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.kanji (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.kanji_id_seq'::regclass),
    entry_id INTEGER NOT NULL,
    text VARCHAR NOT NULL,
    CONSTRAINT uix_kanji_entry_text UNIQUE (entry_id, text)
);

ALTER SEQUENCE __SCHEMA__.kanji_id_seq OWNED BY __SCHEMA__.kanji.id;

CREATE INDEX ix_kanji_entry_id ON __SCHEMA__.kanji (entry_id);
CREATE INDEX ix_kanji_text ON __SCHEMA__.kanji (text);

ALTER TABLE __SCHEMA__.kanji
    ADD CONSTRAINT kanji_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES __SCHEMA__.entry(id);
