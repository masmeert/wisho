--- requires: entry.01-table.sql
CREATE SEQUENCE __SCHEMA__.sense_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.sense (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.sense_id_seq'::regclass),
    entry_id INTEGER NOT NULL,
    "order" INTEGER NOT NULL
);

ALTER SEQUENCE __SCHEMA__.sense_id_seq OWNED BY __SCHEMA__.sense.id;

CREATE INDEX ix_sense_entry_id ON __SCHEMA__.sense (entry_id);

ALTER TABLE __SCHEMA__.sense
    ADD CONSTRAINT sense_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES __SCHEMA__.entry(id);
