--- requires: entry.01-table.sql
CREATE SEQUENCE __SCHEMA__.reading_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.reading (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.reading_id_seq'::regclass),
    entry_id INTEGER NOT NULL,
    text VARCHAR NOT NULL,
    no_kanji BOOLEAN NOT NULL,
    CONSTRAINT uix_reading_entry_text UNIQUE (entry_id, text)
);

ALTER SEQUENCE __SCHEMA__.reading_id_seq OWNED BY __SCHEMA__.reading.id;

CREATE INDEX ix_reading_entry_id ON __SCHEMA__.reading (entry_id);
CREATE INDEX ix_reading_text ON __SCHEMA__.reading (text);

ALTER TABLE __SCHEMA__.reading
    ADD CONSTRAINT reading_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES __SCHEMA__.entry(id);
