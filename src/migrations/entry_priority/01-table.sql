--- requires: entry.01-table.sql
--- requires: kanji.01-table.sql
--- requires: reading.01-table.sql
CREATE SEQUENCE __SCHEMA__.entry_priority_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.entry_priority (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.entry_priority_id_seq'::regclass),
    entry_id INTEGER NOT NULL,
    kanji_id INTEGER,
    reading_id INTEGER,
    raw VARCHAR NOT NULL,
    CONSTRAINT ck_priority_exclusive_target CHECK ((kanji_id IS NOT NULL) <> (reading_id IS NOT NULL)),
    CONSTRAINT uix_priority_kanji_raw UNIQUE (kanji_id, raw),
    CONSTRAINT uix_priority_reading_raw UNIQUE (reading_id, raw)
);

ALTER SEQUENCE __SCHEMA__.entry_priority_id_seq OWNED BY __SCHEMA__.entry_priority.id;

CREATE INDEX ix_entry_priority_entry_id ON __SCHEMA__.entry_priority (entry_id);
CREATE INDEX ix_entry_priority_kanji_id ON __SCHEMA__.entry_priority (kanji_id);
CREATE INDEX ix_entry_priority_reading_id ON __SCHEMA__.entry_priority (reading_id);
CREATE INDEX ix_priority_raw ON __SCHEMA__.entry_priority (raw);

ALTER TABLE __SCHEMA__.entry_priority
    ADD CONSTRAINT entry_priority_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES __SCHEMA__.entry(id);

ALTER TABLE __SCHEMA__.entry_priority
    ADD CONSTRAINT entry_priority_kanji_id_fkey FOREIGN KEY (kanji_id) REFERENCES __SCHEMA__.kanji(id);

ALTER TABLE __SCHEMA__.entry_priority
    ADD CONSTRAINT entry_priority_reading_id_fkey FOREIGN KEY (reading_id) REFERENCES __SCHEMA__.reading(id);
