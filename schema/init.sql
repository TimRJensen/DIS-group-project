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

ALTER TABLE IF EXISTS ONLY public.teams DROP CONSTRAINT IF EXISTS teams_pkey;
ALTER TABLE IF EXISTS ONLY public.locales DROP CONSTRAINT IF EXISTS locales_pkey;
ALTER TABLE IF EXISTS ONLY public.groups DROP CONSTRAINT IF EXISTS groups_pkey;
ALTER TABLE IF EXISTS ONLY public.fixtures DROP CONSTRAINT IF EXISTS fixtures_pkey;
DROP TABLE IF EXISTS public.teams;
DROP TABLE IF EXISTS public.locales;
DROP TABLE IF EXISTS public.groups;
DROP TABLE IF EXISTS public.fixtures;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: fixtures; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.fixtures (
    id integer NOT NULL,
    date timestamp without time zone,
    venue character varying(64),
    home_id integer,
    away_id integer,
    status character varying(4),
    home_goals integer,
    away_goals integer,
    halftime_home integer,
    halftime_away integer,
    fulltime_home integer,
    fulltime_away integer,
    extratime_home integer,
    extratime_away integer,
    penalty_home integer,
    penalty_away integer
);


ALTER TABLE public.fixtures OWNER TO group77;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(64)
);


ALTER TABLE public.groups OWNER TO group77;

--
-- Name: locales; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.locales (
    id character varying(6) NOT NULL,
    locale json
);


ALTER TABLE public.locales OWNER TO group77;

--
-- Name: teams; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    name character varying(64),
    code character varying(8),
    logo character varying(64),
    rank integer,
    points integer,
    goals_for integer,
    goals_against integer,
    wins integer,
    loses integer,
    draws integer,
    group_id integer
);


ALTER TABLE public.teams OWNER TO group77;

--
-- Data for Name: fixtures; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.fixtures (id, date, venue, home_id, away_id, status, home_goals, away_goals, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away) FROM stdin;
1145509	2024-06-14 19:00:00	Fußball Arena München	25	1108	NS	0	0	0	0	0	0	0	0	0	0
1145510	2024-06-15 13:00:00	Cologne Stadium	769	15	NS	0	0	0	0	0	0	0	0	0	0
1145511	2024-06-15 16:00:00	Olympiastadion Berlin	9	3	NS	0	0	0	0	0	0	0	0	0	0
1145512	2024-06-15 19:00:00	BVB Stadion Dortmund	768	778	NS	0	0	0	0	0	0	0	0	0	0
1145513	2024-06-16 16:00:00	Stuttgart Arena	1091	21	NS	0	0	0	0	0	0	0	0	0	0
1145514	2024-06-16 19:00:00	Arena AufSchalke	14	10	NS	0	0	0	0	0	0	0	0	0	0
1145515	2024-06-17 19:00:00	Düsseldorf Arena	775	2	NS	0	0	0	0	0	0	0	0	0	0
1145516	2024-06-17 16:00:00	Frankfurt Arena	1	773	NS	0	0	0	0	0	0	0	0	0	0
1145517	2024-06-18 19:00:00	Leipzig Stadium	27	770	NS	0	0	0	0	0	0	0	0	0	0
1145518	2024-06-19 19:00:00	Cologne Stadium	1108	15	NS	0	0	0	0	0	0	0	0	0	0
1145519	2024-06-19 16:00:00	Stuttgart Arena	25	769	NS	0	0	0	0	0	0	0	0	0	0
1145520	2024-06-19 13:00:00	Volksparkstadion	3	778	NS	0	0	0	0	0	0	0	0	0	0
1145521	2024-06-20 19:00:00	Arena AufSchalke	9	768	NS	0	0	0	0	0	0	0	0	0	0
1145522	2024-06-20 16:00:00	Frankfurt Arena	21	10	NS	0	0	0	0	0	0	0	0	0	0
1145523	2024-06-20 13:00:00	Fußball Arena München	1091	14	NS	0	0	0	0	0	0	0	0	0	0
1145524	2024-06-21 19:00:00	Leipzig Stadium	1118	2	NS	0	0	0	0	0	0	0	0	0	0
1145525	2024-06-22 19:00:00	Cologne Stadium	1	774	NS	0	0	0	0	0	0	0	0	0	0
1145526	2024-06-22 16:00:00	BVB Stadion Dortmund	777	27	NS	0	0	0	0	0	0	0	0	0	0
1145527	2024-06-23 19:00:00	Frankfurt Arena	15	25	NS	0	0	0	0	0	0	0	0	0	0
1145528	2024-06-23 19:00:00	Stuttgart Arena	1108	769	NS	0	0	0	0	0	0	0	0	0	0
1145529	2024-06-24 19:00:00	Leipzig Stadium	3	768	NS	0	0	0	0	0	0	0	0	0	0
1145530	2024-06-24 19:00:00	Düsseldorf Arena	778	9	NS	0	0	0	0	0	0	0	0	0	0
1145531	2024-06-25 19:00:00	Cologne Stadium	10	1091	NS	0	0	0	0	0	0	0	0	0	0
1145532	2024-06-25 19:00:00	Fußball Arena München	21	14	NS	0	0	0	0	0	0	0	0	0	0
1145533	2024-06-25 16:00:00	Olympiastadion Berlin	1118	775	NS	0	0	0	0	0	0	0	0	0	0
1145534	2024-06-26 16:00:00	Frankfurt Arena	773	774	NS	0	0	0	0	0	0	0	0	0	0
1145535	2024-06-26 19:00:00	Volksparkstadion	770	777	NS	0	0	0	0	0	0	0	0	0	0
1189846	2024-06-16 13:00:00	Volksparkstadion	24	1118	NS	0	0	0	0	0	0	0	0	0	0
1189847	2024-06-17 13:00:00	Fußball Arena München	774	772	NS	0	0	0	0	0	0	0	0	0	0
1189848	2024-06-18 16:00:00	BVB Stadion Dortmund	777	1104	NS	0	0	0	0	0	0	0	0	0	0
1189849	2024-06-21 13:00:00	Düsseldorf Arena	773	772	NS	0	0	0	0	0	0	0	0	0	0
1189850	2024-06-21 16:00:00	Olympiastadion Berlin	24	775	NS	0	0	0	0	0	0	0	0	0	0
1189851	2024-06-22 13:00:00	Volksparkstadion	1104	770	NS	0	0	0	0	0	0	0	0	0	0
1189852	2024-06-25 16:00:00	BVB Stadion Dortmund	2	24	NS	0	0	0	0	0	0	0	0	0	0
1189853	2024-06-26 16:00:00	Stuttgart Arena	772	1	NS	0	0	0	0	0	0	0	0	0	0
1189854	2024-06-26 19:00:00	Arena AufSchalke	1104	27	NS	0	0	0	0	0	0	0	0	0	0
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.groups (id, name) FROM stdin;
0	Group A
1	Group B
2	Group C
3	Group D
4	Group E
5	Group F
\.


--
-- Data for Name: locales; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.locales (id, locale) FROM stdin;
da_DK	{"counter":{"0":"dage","1":"timer","2":"minutter","3":"sekunder"},"groups":{"name":{"0":"Gruppe A","1":"Gruppe B","2":"Gruppe C","3":"Gruppe D","4":"Gruppe E","5":"Gruppe F"}},"id":"da_DK","name":"DK","navbar":{"0":"Hold","1":"Grupper","2":"Kampe"},"teams":{"name":{"1":"Belgien","10":"England","1091":"Slovenien","1104":"Georgien","1108":"Skotland","1118":"Holland","14":"Serbien","15":"Schweiz","2":"Frankrig","21":"Danmark","24":"Polen","25":"Tyskland","27":"Portugal","3":"Kroatien","768":"Italien","769":"Ungarn","770":"Tjekkiet","772":"Ukraine","773":"Slovakiet","774":"Rumænien","775":"Østrig","777":"Tyrkiet","778":"Albanien","9":"Spanien"}},"views":{"/":{},"error":{"0":"Vend tilbage til","1":"forsiden","404":"Ingenting her"},"group":{"0":"Stillinger","06":"Juni","07":"Juli","1":"V","2":"U","3":"T","4":"Kommende kampe","5":"Seneste kampe"},"groups":{"0":"Grupper"}}}
en_EN	{"counter":{"0":"days","1":"hours","2":"minutes","3":"seconds"},"groups":{"name":{"0":"Group A","1":"Group B","2":"Group C","3":"Group D","4":"Group E","5":"Group F"}},"id":"en_EN","name":"EN","navbar":{"0":"Teams","1":"Groups","2":"Matches"},"teams":{"name":{"1":"Belgium","10":"England","1091":"Slovenia","1104":"Georgia","1108":"Scotland","1118":"Netherlands","14":"Serbia","15":"Switzerland","2":"France","21":"Denmark","24":"Poland","25":"Germany","27":"Portugal","3":"Croatia","768":"Italy","769":"Hungary","770":"Czech Republic","772":"Ukraine","773":"Slovakia","774":"Romania","775":"Austria","777":"Turkey","778":"Albania","9":"Spain"}},"views":{"/":{},"error":{"0":"Return to the","1":"frontpage","404":"Nothing here"},"group":{"0":"Standings","06":"June","07":"July","1":"W","2":"D","3":"L","4":"Upcomming matches","5":"Latest matches"},"groups":{"0":"Groups"}}}
sv_SWE	{"counter":{"0":"dagar","1":"timmar","2":"minuter","3":"sekunder"},"groups":{"name":{"0":"Grupp A","1":"Grupp B","2":"Grupp C","3":"Grupp D","4":"Grupp E","5":"Grupp F"}},"id":"sv_SWE","name":"SWE","navbar":{"0":"Lag","1":"Grupper","2":"Matches"},"teams":{"name":{"1":"Belgien","10":"England","1091":"Slovenien","1104":"Georgien","1108":"Skottland","1118":"Nederländerna","14":"Serbien","15":"Schweiz","2":"Frankrike","21":"Danmark","24":"Polen","25":"Tyskland","27":"Portugal","3":"Kroatien","768":"Italien","769":"Ungern","770":"Tjeckien","772":"Ukraina","773":"Slovakien","774":"Rumänien","775":"Österrike","777":"Turkiet","778":"Albanien","9":"Spanien"}},"views":{"/":{},"error":{"0":"Gå tillbaka till","1":"startsida","404":"Här var det tomt"},"group":{"0":"Ställningar","06":"Juni","07":"Juli","1":"V","2":"D","3":"F","4":"Kommande matcher","5":"Senaste matcher"},"groups":{"0":"Grupper"}}}
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.teams (id, name, code, logo, rank, points, goals_for, goals_against, wins, loses, draws, group_id) FROM stdin;
1	Belgium	BEL	https://media.api-sports.io/football/teams/1.png	2	0	0	0	0	0	0	4
2	France	FRA	https://media.api-sports.io/football/teams/2.png	3	0	0	0	0	0	0	3
3	Croatia	CRO	https://media.api-sports.io/football/teams/3.png	2	0	0	0	0	0	0	1
9	Spain	SPA	https://media.api-sports.io/football/teams/9.png	3	0	0	0	0	0	0	1
10	England	ENG	https://media.api-sports.io/football/teams/10.png	3	0	0	0	0	0	0	2
14	Serbia	SER	https://media.api-sports.io/football/teams/14.png	4	0	0	0	0	0	0	2
15	Switzerland	SWI	https://media.api-sports.io/football/teams/15.png	2	0	0	0	0	0	0	0
21	Denmark	DEN	https://media.api-sports.io/football/teams/21.png	2	0	0	0	0	0	0	2
24	Poland	POL	https://media.api-sports.io/football/teams/24.png	1	0	0	0	0	0	0	3
25	Germany	GER	https://media.api-sports.io/football/teams/25.png	1	0	0	0	0	0	0	0
27	Portugal	POR	https://media.api-sports.io/football/teams/27.png	3	0	0	0	0	0	0	5
768	Italy	ITA	https://media.api-sports.io/football/teams/768.png	1	0	0	0	0	0	0	1
769	Hungary	HUN	https://media.api-sports.io/football/teams/769.png	4	0	0	0	0	0	0	0
770	Czech Republic	CZE	https://media.api-sports.io/football/teams/770.png	1	0	0	0	0	0	0	5
772	Ukraine	UKR	https://media.api-sports.io/football/teams/772.png	4	0	0	0	0	0	0	4
773	Slovakia	SLO	https://media.api-sports.io/football/teams/773.png	3	0	0	0	0	0	0	4
774	Romania	ROM	https://media.api-sports.io/football/teams/774.png	1	0	0	0	0	0	0	4
775	Austria	AUS	https://media.api-sports.io/football/teams/775.png	2	0	0	0	0	0	0	3
777	Turkey	TUR	https://media.api-sports.io/football/teams/777.png	2	0	0	0	0	0	0	5
778	Albania	ALB	https://media.api-sports.io/football/teams/778.png	4	0	0	0	0	0	0	1
1091	Slovenia	SLO	https://media.api-sports.io/football/teams/1091.png	1	0	0	0	0	0	0	2
1104	Georgia	GEO	https://media.api-sports.io/football/teams/1104.png	4	0	0	0	0	0	0	5
1108	Scotland	SCO	https://media.api-sports.io/football/teams/1108.png	3	0	0	0	0	0	0	0
1118	Netherlands	NET	https://media.api-sports.io/football/teams/1118.png	4	0	0	0	0	0	0	3
\.


--
-- Name: fixtures fixtures_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_pkey PRIMARY KEY (id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: locales locales_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_pkey PRIMARY KEY (id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

