--- requires: sense.01-table.sql
CREATE SEQUENCE __SCHEMA__.sense_pos_id_seq
    AS INTEGER
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE __SCHEMA__.sense_pos (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('__SCHEMA__.sense_pos_id_seq'::regclass),
    sense_id INTEGER NOT NULL,
    tag VARCHAR NOT NULL,
    CONSTRAINT uix_sense_pos_once UNIQUE (sense_id, tag)
);

ALTER SEQUENCE __SCHEMA__.sense_pos_id_seq OWNED BY __SCHEMA__.sense_pos.id;

CREATE INDEX ix_sense_pos_sense_id ON __SCHEMA__.sense_pos (sense_id);

ALTER TABLE __SCHEMA__.sense_pos
    ADD CONSTRAINT sense_pos_sense_id_fkey FOREIGN KEY (sense_id) REFERENCES __SCHEMA__.sense(id);
