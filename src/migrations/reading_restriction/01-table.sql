--- requires: entry.01-table.sql
--- requires: kanji.01-table.sql
--- requires: reading.01-table.sql
CREATE SEQUENCE __SCHEMA__.reading_restriction_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.reading_restriction (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.reading_restriction_id_seq'::regclass),
    entry_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    kanji_id INTEGER NOT NULL,
    CONSTRAINT uix_rrestr_unique UNIQUE (entry_id, reading_id, kanji_id)
);

ALTER SEQUENCE __SCHEMA__.reading_restriction_id_seq OWNED BY __SCHEMA__.reading_restriction.id;

CREATE INDEX ix_reading_restriction_entry_id ON __SCHEMA__.reading_restriction (entry_id);
CREATE INDEX ix_reading_restriction_kanji_id ON __SCHEMA__.reading_restriction (kanji_id);
CREATE INDEX ix_reading_restriction_reading_id ON __SCHEMA__.reading_restriction (reading_id);

ALTER TABLE __SCHEMA__.reading_restriction
    ADD CONSTRAINT reading_restriction_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES __SCHEMA__.entry(id);

ALTER TABLE __SCHEMA__.reading_restriction
    ADD CONSTRAINT reading_restriction_kanji_id_fkey FOREIGN KEY (kanji_id) REFERENCES __SCHEMA__.kanji(id);

ALTER TABLE __SCHEMA__.reading_restriction
    ADD CONSTRAINT reading_restriction_reading_id_fkey FOREIGN KEY (reading_id) REFERENCES __SCHEMA__.reading(id);
