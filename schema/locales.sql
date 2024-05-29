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

ALTER TABLE IF EXISTS ONLY public.locales DROP CONSTRAINT IF EXISTS locales_pkey;
DROP TABLE IF EXISTS public.locales;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: locales; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.locales (
    id character varying(255) NOT NULL,
    locale json
);


ALTER TABLE public.locales OWNER TO group77;

--
-- Data for Name: locales; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.locales (id, locale) FROM stdin;
en_EN	{"id": "en_EN", "name": "EN", "views": {"error": {"0": "Return to the", "1": "frontpage", "404": "Nothing here"}, "/": {}}, "navbar": {"0": "Teams", "1": "Groups", "2": "Matches"}, "counter": {"0": "days", "1": "hours", "2": "minutes", "3": "seconds"}, "groups": {"name": {"0": "Group A", "1": "Group B", "2": "Group C", "3": "Group D", "4": "Group E", "5": "Group F"}}, "teams": {"name": {"1": "Belgium", "2": "France", "3": "Croatia", "9": "Spain", "10": "England", "14": "Serbia", "15": "Switzerland", "21": "Denmark", "24": "Poland", "25": "Germany", "27": "Portugal", "768": "Italy", "769": "Hungary", "770": "Czech Republic", "772": "Ukraine", "773": "Slovakia", "774": "Romania", "775": "Austria", "777": "Turkey", "778": "Albania", "1091": "Slovenia", "1104": "Georgia", "1108": "Scotland", "1118": "Netherlands"}}}
da_DK	{"id": "da_DK", "name": "DK", "views": {"error": {"0": "Vend tilbage til", "1": "forsiden", "404": "Ingenting her"}, "/": {}}, "navbar": {"0": "Hold", "1": "Grupper", "2": "Kampe"}, "counter": {"0": "dage", "1": "timer", "2": "minutter", "3": "sekunder"}, "groups": {"name": {"0": "Gruppe A", "1": "Gruppe B", "2": "Gruppe C", "3": "Gruppe D", "4": "Gruppe E", "5": "Gruppe F"}}, "teams": {"name": {"1": "Belgien", "2": "Frankrig", "3": "Kroatien", "9": "Spanien", "10": "England", "14": "Serbien", "15": "Schweiz", "21": "Danmark", "24": "Polen", "25": "Tyskland", "27": "Portugal", "768": "Italien", "769": "Ungarn", "770": "Tjekkiet", "772": "Ukraine", "773": "Slovakiet ", "774": "Rum\\u00e6nien", "775": "\\u00d8strig", "777": "Tyrkiet", "778": "Albanien", "1091": "Slovenien", "1104": "Georgien", "1108": "Skotland", "1118": "Holland"}}}
sv_SWE	{"id": "sv_SWE", "name": "SWE", "views": {"error": {"0": "G\\u00e5 tillbaka till", "1": "startsida", "404": "H\\u00e4r var det tomt"}, "/": {}}, "navbar": {"0": "Lag", "1": "Grupper", "2": "Matches"}, "counter": {"0": "dagar", "1": "timmar", "2": "minuter", "3": "sekunder"}, "groups": {"name": {"0": "Grupp A", "1": "Grupp B", "2": "Grupp C", "3": "Grupp D", "4": "Grupp E", "5": "Grupp F"}}, "teams": {"name": {"1": "Belgien", "2": "Frankrike", "3": "Kroatien", "9": "Spanien", "10": "England", "14": "Serbien", "15": "Schweiz", "21": "Danmark", "24": "Polen", "25": "Tyskland", "27": "Portugal", "768": "Italien", "769": "Ungern", "770": "Tjeckien", "772": "Ukraina", "773": "Slovakien ", "774": "Rum\\u00e4nien", "775": "\\u00d6sterrike", "777": "Turkiet", "778": "Albanien", "1091": "Slovenien", "1104": "Georgien", "1108": "Skottland", "1118": "Nederl\\u00e4nderna"}}}
\.


--
-- Name: locales locales_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

