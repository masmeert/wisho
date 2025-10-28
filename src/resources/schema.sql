--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: entry; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.entry (
    id integer NOT NULL
);


ALTER TABLE public.entry OWNER TO wisho;

--
-- Name: entry_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.entry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entry_id_seq OWNER TO wisho;

--
-- Name: entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.entry_id_seq OWNED BY public.entry.id;


--
-- Name: entry_priority; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.entry_priority (
    id integer NOT NULL,
    entry_id integer NOT NULL,
    kanji_id integer,
    reading_id integer,
    raw character varying NOT NULL,
    CONSTRAINT ck_priority_exclusive_target CHECK (((kanji_id IS NOT NULL) <> (reading_id IS NOT NULL)))
);


ALTER TABLE public.entry_priority OWNER TO wisho;

--
-- Name: entry_priority_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.entry_priority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entry_priority_id_seq OWNER TO wisho;

--
-- Name: entry_priority_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.entry_priority_id_seq OWNED BY public.entry_priority.id;


--
-- Name: gloss; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.gloss (
    id integer NOT NULL,
    sense_id integer NOT NULL,
    "order" integer NOT NULL,
    text text NOT NULL,
    lang character varying NOT NULL
);


ALTER TABLE public.gloss OWNER TO wisho;

--
-- Name: gloss_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.gloss_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gloss_id_seq OWNER TO wisho;

--
-- Name: gloss_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.gloss_id_seq OWNED BY public.gloss.id;


--
-- Name: kanji; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.kanji (
    id integer NOT NULL,
    entry_id integer NOT NULL,
    text character varying NOT NULL
);


ALTER TABLE public.kanji OWNER TO wisho;

--
-- Name: kanji_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.kanji_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kanji_id_seq OWNER TO wisho;

--
-- Name: kanji_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.kanji_id_seq OWNED BY public.kanji.id;


--
-- Name: reading; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.reading (
    id integer NOT NULL,
    entry_id integer NOT NULL,
    text character varying NOT NULL,
    no_kanji boolean NOT NULL
);


ALTER TABLE public.reading OWNER TO wisho;

--
-- Name: reading_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.reading_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_id_seq OWNER TO wisho;

--
-- Name: reading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.reading_id_seq OWNED BY public.reading.id;


--
-- Name: reading_restriction; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.reading_restriction (
    id integer NOT NULL,
    entry_id integer NOT NULL,
    reading_id integer NOT NULL,
    kanji_id integer NOT NULL
);


ALTER TABLE public.reading_restriction OWNER TO wisho;

--
-- Name: reading_restriction_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.reading_restriction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_restriction_id_seq OWNER TO wisho;

--
-- Name: reading_restriction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.reading_restriction_id_seq OWNED BY public.reading_restriction.id;


--
-- Name: sense; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.sense (
    id integer NOT NULL,
    entry_id integer NOT NULL,
    "order" integer NOT NULL
);


ALTER TABLE public.sense OWNER TO wisho;

--
-- Name: sense_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.sense_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sense_id_seq OWNER TO wisho;

--
-- Name: sense_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.sense_id_seq OWNED BY public.sense.id;


--
-- Name: sense_pos; Type: TABLE; Schema: public; Owner: wisho
--

CREATE TABLE public.sense_pos (
    id integer NOT NULL,
    sense_id integer NOT NULL,
    tag character varying NOT NULL
);


ALTER TABLE public.sense_pos OWNER TO wisho;

--
-- Name: sense_pos_id_seq; Type: SEQUENCE; Schema: public; Owner: wisho
--

CREATE SEQUENCE public.sense_pos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sense_pos_id_seq OWNER TO wisho;

--
-- Name: sense_pos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wisho
--

ALTER SEQUENCE public.sense_pos_id_seq OWNED BY public.sense_pos.id;


--
-- Name: entry id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry ALTER COLUMN id SET DEFAULT nextval('public.entry_id_seq'::regclass);


--
-- Name: entry_priority id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority ALTER COLUMN id SET DEFAULT nextval('public.entry_priority_id_seq'::regclass);


--
-- Name: gloss id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.gloss ALTER COLUMN id SET DEFAULT nextval('public.gloss_id_seq'::regclass);


--
-- Name: kanji id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.kanji ALTER COLUMN id SET DEFAULT nextval('public.kanji_id_seq'::regclass);


--
-- Name: reading id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading ALTER COLUMN id SET DEFAULT nextval('public.reading_id_seq'::regclass);


--
-- Name: reading_restriction id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction ALTER COLUMN id SET DEFAULT nextval('public.reading_restriction_id_seq'::regclass);


--
-- Name: sense id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense ALTER COLUMN id SET DEFAULT nextval('public.sense_id_seq'::regclass);


--
-- Name: sense_pos id; Type: DEFAULT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense_pos ALTER COLUMN id SET DEFAULT nextval('public.sense_pos_id_seq'::regclass);


--
-- Name: entry entry_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry
    ADD CONSTRAINT entry_pkey PRIMARY KEY (id);


--
-- Name: entry_priority entry_priority_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT entry_priority_pkey PRIMARY KEY (id);


--
-- Name: gloss gloss_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.gloss
    ADD CONSTRAINT gloss_pkey PRIMARY KEY (id);


--
-- Name: kanji kanji_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.kanji
    ADD CONSTRAINT kanji_pkey PRIMARY KEY (id);


--
-- Name: reading reading_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading
    ADD CONSTRAINT reading_pkey PRIMARY KEY (id);


--
-- Name: reading_restriction reading_restriction_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction
    ADD CONSTRAINT reading_restriction_pkey PRIMARY KEY (id);


--
-- Name: sense sense_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense
    ADD CONSTRAINT sense_pkey PRIMARY KEY (id);


--
-- Name: sense_pos sense_pos_pkey; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense_pos
    ADD CONSTRAINT sense_pos_pkey PRIMARY KEY (id);


--
-- Name: kanji uix_kanji_entry_text; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.kanji
    ADD CONSTRAINT uix_kanji_entry_text UNIQUE (entry_id, text);


--
-- Name: entry_priority uix_priority_kanji_raw; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT uix_priority_kanji_raw UNIQUE (kanji_id, raw);


--
-- Name: entry_priority uix_priority_reading_raw; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT uix_priority_reading_raw UNIQUE (reading_id, raw);


--
-- Name: reading uix_reading_entry_text; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading
    ADD CONSTRAINT uix_reading_entry_text UNIQUE (entry_id, text);


--
-- Name: reading_restriction uix_rrestr_unique; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction
    ADD CONSTRAINT uix_rrestr_unique UNIQUE (entry_id, reading_id, kanji_id);


--
-- Name: sense_pos uix_sense_pos_once; Type: CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense_pos
    ADD CONSTRAINT uix_sense_pos_once UNIQUE (sense_id, tag);


--
-- Name: ix_entry_priority_entry_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_entry_priority_entry_id ON public.entry_priority USING btree (entry_id);


--
-- Name: ix_entry_priority_kanji_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_entry_priority_kanji_id ON public.entry_priority USING btree (kanji_id);


--
-- Name: ix_entry_priority_reading_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_entry_priority_reading_id ON public.entry_priority USING btree (reading_id);


--
-- Name: ix_gloss_sense_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_gloss_sense_id ON public.gloss USING btree (sense_id);


--
-- Name: ix_gloss_text; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_gloss_text ON public.gloss USING btree (text);


--
-- Name: ix_kanji_entry_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_kanji_entry_id ON public.kanji USING btree (entry_id);


--
-- Name: ix_kanji_text; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_kanji_text ON public.kanji USING btree (text);


--
-- Name: ix_priority_raw; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_priority_raw ON public.entry_priority USING btree (raw);


--
-- Name: ix_reading_entry_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_reading_entry_id ON public.reading USING btree (entry_id);


--
-- Name: ix_reading_restriction_entry_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_reading_restriction_entry_id ON public.reading_restriction USING btree (entry_id);


--
-- Name: ix_reading_restriction_kanji_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_reading_restriction_kanji_id ON public.reading_restriction USING btree (kanji_id);


--
-- Name: ix_reading_restriction_reading_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_reading_restriction_reading_id ON public.reading_restriction USING btree (reading_id);


--
-- Name: ix_reading_text; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_reading_text ON public.reading USING btree (text);


--
-- Name: ix_sense_entry_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_sense_entry_id ON public.sense USING btree (entry_id);


--
-- Name: ix_sense_pos_sense_id; Type: INDEX; Schema: public; Owner: wisho
--

CREATE INDEX ix_sense_pos_sense_id ON public.sense_pos USING btree (sense_id);


--
-- Name: entry_priority entry_priority_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT entry_priority_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entry(id);


--
-- Name: entry_priority entry_priority_kanji_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT entry_priority_kanji_id_fkey FOREIGN KEY (kanji_id) REFERENCES public.kanji(id);


--
-- Name: entry_priority entry_priority_reading_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.entry_priority
    ADD CONSTRAINT entry_priority_reading_id_fkey FOREIGN KEY (reading_id) REFERENCES public.reading(id);


--
-- Name: gloss gloss_sense_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.gloss
    ADD CONSTRAINT gloss_sense_id_fkey FOREIGN KEY (sense_id) REFERENCES public.sense(id);


--
-- Name: kanji kanji_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.kanji
    ADD CONSTRAINT kanji_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entry(id);


--
-- Name: reading reading_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading
    ADD CONSTRAINT reading_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entry(id);


--
-- Name: reading_restriction reading_restriction_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction
    ADD CONSTRAINT reading_restriction_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entry(id);


--
-- Name: reading_restriction reading_restriction_kanji_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction
    ADD CONSTRAINT reading_restriction_kanji_id_fkey FOREIGN KEY (kanji_id) REFERENCES public.kanji(id);


--
-- Name: reading_restriction reading_restriction_reading_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.reading_restriction
    ADD CONSTRAINT reading_restriction_reading_id_fkey FOREIGN KEY (reading_id) REFERENCES public.reading(id);


--
-- Name: sense sense_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense
    ADD CONSTRAINT sense_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entry(id);


--
-- Name: sense_pos sense_pos_sense_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wisho
--

ALTER TABLE ONLY public.sense_pos
    ADD CONSTRAINT sense_pos_sense_id_fkey FOREIGN KEY (sense_id) REFERENCES public.sense(id);


--
-- PostgreSQL database dump complete
--

