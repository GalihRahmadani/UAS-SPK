
--
-- Postg\ m m ho hvn .hxczxcvbm,.eSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: tblhelm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblhelm (
    no integer NOT NULL,
    nama_helm character varying(255) NOT NULL,
    harga character varying(255) NOT NULL,
    berat character varying(255) NOT NULL,
    double_visor character varying(255) NOT NULL,
    sertifikasi character varying(255) NOT NULL,
    garansi character varying(255) NOT NULL
);


ALTER TABLE public.tblhelm OWNER TO postgres;

--
-- Name: tblhelm_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblhelm_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblhelm_no_seq OWNER TO postgres;

--
-- Name: tblhelm_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblhelm_no_seq OWNED BY public.tblhelm.no;


--
-- Name: tblhelm no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblhelm ALTER COLUMN no SET DEFAULT nextval('public.tblhelm_no_seq'::regclass);


--
-- Data for Name: tblhelm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblhelm (no, nama_helm, harga, berat, double_visor, sertifikasi, garansi) FROM stdin;
2	HIU ARROW	150000	1100 gram	Ada	SNI	1
5	KYT GALAXY SLIDE	350,000	1400 gram	Ada	SNI DOT	5
6	INK Trooper	650,000	1300 gram	Ada	SNI	2
7	NJS Freedom	650,000	1200 gram	Ada	SNI	3
8	JPX JP Signature	700000	1200 gram	Ada	SNI	2
9	Zeus ZS816 C Retro	700000	1200 gram	Tidak ada	SNI	2
10	HBC Cakil	400000	1000 gram	Ada	SNI	1
1	BMC TOURING	100000	1100 gram	Tidak Ada	SNI	1
3	INK CX 22	300000	1400 gram	Tidak Ada	SNI DOT	4
4	MDS PROTECT OR	200000	1300 gram	Tidak Ada	SNI	2
\.


--
-- Name: tblhelm_no_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblhelm_no_seq', 10, true);


--
-- Name: tblhelm tblhelm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblhelm
    ADD CONSTRAINT tblhelm_pkey PRIMARY KEY (no);


--
-- PostgreSQL database dump complete
--

