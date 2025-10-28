--- requires: sense.01-table.sql
CREATE SEQUENCE __SCHEMA__.gloss_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.gloss (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.gloss_id_seq'::regclass),
    sense_id INTEGER NOT NULL,
    "order" INTEGER NOT NULL,
    text TEXT NOT NULL,
    lang VARCHAR NOT NULL
);

ALTER SEQUENCE __SCHEMA__.gloss_id_seq OWNED BY __SCHEMA__.gloss.id;

CREATE INDEX ix_gloss_sense_id ON __SCHEMA__.gloss (sense_id);
CREATE INDEX ix_gloss_text ON __SCHEMA__.gloss (text);

ALTER TABLE __SCHEMA__.gloss
    ADD CONSTRAINT gloss_sense_id_fkey FOREIGN KEY (sense_id) REFERENCES __SCHEMA__.sense(id);
