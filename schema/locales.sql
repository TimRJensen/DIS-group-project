--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

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
-- Name: locales; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.locales (
    id character varying(255) NOT NULL,
    en_en character varying(255),
    da_dk character varying(255)
);


ALTER TABLE public.locales OWNER TO group77;

--
-- Data for Name: locales; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.locales (id, en_en, da_dk) FROM stdin;
views:error:404	Nothing here	Ingenting her
views:error:1	frontpage	forsiden
views:error:0	Return to the	Vend tilbage til
navbar:2	Matches	Kampe
navbar:1	Groups	Grupper
navbar:0	Teams	Hold
counter:3	seconds	sekunder
counter:2	minutes	minutter
counter:1	hours	timer
counter:0	days	dage
teams:name:1118	Netherlands	Holland
teams:name:1108	Scotland	Skotland
teams:name:1104	Georgia	Georgien
teams:name:1091	Slovenia	Slovenien
teams:name:778	Albania	Albanien
teams:name:777	Turkey	Tyrkiet
teams:name:775	Austria	Østrig
teams:name:774	Romania	Rumænien
teams:name:773	Slovakia	Slovakiet
teams:name:772	Ukraine	Ukraine
teams:name:770	Czech Republic	Tjekkiet
teams:name:769	Hungary	Ungarn
teams:name:768	Italy	Italien
teams:name:27	Portugal	Portugal
teams:name:25	Germany	Tyskland
teams:name:24	Poland	Polen
teams:name:21	Denmark	Danmark
teams:name:15	Switzerland	Schweiz
teams:name:14	Serbia	Serbien
teams:name:10	England	England
teams:name:9	Spain	Spanien
teams:name:3	Croatia	Kroatien
teams:name:2	France	Frankrig
teams:name:1	Belgium	Belgien
\.


--
-- Name: locales locales_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

