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
-- Name: fixtures; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.fixtures (
    id integer NOT NULL,
    date timestamp without time zone,
    venue character varying(64),
    home_id integer,
    away_id integer
);


ALTER TABLE public.fixtures OWNER TO group77;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(64),
    team_id integer
);


ALTER TABLE public.groups OWNER TO group77;

--
-- Name: teams; Type: TABLE; Schema: public; Owner: group77
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    name character varying(64),
    code character varying(8),
    logo character varying(64)
);


ALTER TABLE public.teams OWNER TO group77;

--
-- Data for Name: fixtures; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.fixtures (id, date, venue, home_id, away_id) FROM stdin;
1145509	2024-06-14 19:00:00	Allianz Arena	25	1108
1145510	2024-06-15 13:00:00	RheinEnergieStadion	769	15
1145511	2024-06-15 16:00:00	Olympiastadion Berlin	9	3
1145512	2024-06-15 19:00:00	SIGNAL IDUNA PARK	768	778
1145513	2024-06-16 16:00:00	MHP Arena	1091	21
1145514	2024-06-16 19:00:00	VELTINS-Arena	14	10
1145515	2024-06-17 19:00:00	Merkur Spiel-Arena	775	2
1145516	2024-06-17 16:00:00	Deutsche Bank Park	1	773
1145517	2024-06-18 19:00:00	Red Bull Arena	27	770
1145518	2024-06-19 19:00:00	RheinEnergieStadion	1108	15
1145519	2024-06-19 16:00:00	MHP Arena	25	769
1145520	2024-06-19 13:00:00	Volksparkstadion	3	778
1145521	2024-06-20 19:00:00	VELTINS-Arena	9	768
1145522	2024-06-20 16:00:00	Deutsche Bank Park	21	10
1145523	2024-06-20 13:00:00	Allianz Arena	1091	14
1145524	2024-06-21 19:00:00	Red Bull Arena	1118	2
1145525	2024-06-22 19:00:00	RheinEnergieStadion	1	774
1145526	2024-06-22 16:00:00	SIGNAL IDUNA PARK	777	27
1145527	2024-06-23 19:00:00	Deutsche Bank Park	15	25
1145528	2024-06-23 19:00:00	MHP Arena	1108	769
1145529	2024-06-24 19:00:00	Red Bull Arena	3	768
1145530	2024-06-24 19:00:00	Merkur Spiel-Arena	778	9
1145531	2024-06-25 19:00:00	RheinEnergieStadion	10	1091
1145532	2024-06-25 19:00:00	Allianz Arena	21	14
1145533	2024-06-25 16:00:00	Olympiastadion Berlin	1118	775
1145534	2024-06-26 16:00:00	Deutsche Bank Park	773	774
1145535	2024-06-26 19:00:00	Volksparkstadion	770	777
1189846	2024-06-16 13:00:00	Volksparkstadion	24	1118
1189847	2024-06-17 13:00:00	Allianz Arena	774	772
1189848	2024-06-18 16:00:00	SIGNAL IDUNA PARK	777	1104
1189849	2024-06-21 13:00:00	Merkur Spiel-Arena	773	772
1189850	2024-06-21 16:00:00	Olympiastadion Berlin	24	775
1189851	2024-06-22 13:00:00	Volksparkstadion	1104	770
1189852	2024-06-25 16:00:00	SIGNAL IDUNA PARK	2	24
1189853	2024-06-26 16:00:00	MHPArena	772	1
1189854	2024-06-26 19:00:00	VELTINS-Arena	1104	27
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.groups (id, name, team_id) FROM stdin;
0	Group A	25
1	Group A	15
2	Group A	1108
3	Group A	769
4	Group B	768
5	Group B	3
6	Group B	9
7	Group B	778
8	Group C	1091
9	Group C	21
10	Group C	10
11	Group C	14
12	Group D	24
13	Group D	775
14	Group D	2
15	Group D	1118
16	Group E	774
17	Group E	1
18	Group E	773
19	Group E	772
20	Group F	770
21	Group F	777
22	Group F	27
23	Group F	1104
24	Ranking of third-placed teams	2
25	Ranking of third-placed teams	27
26	Ranking of third-placed teams	9
27	Ranking of third-placed teams	1108
28	Ranking of third-placed teams	773
29	Ranking of third-placed teams	10
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: group77
--

COPY public.teams (id, name, code, logo) FROM stdin;
1	Belgium	BEL	https://media.api-sports.io/football/teams/1.png
2	France	FRA	https://media.api-sports.io/football/teams/2.png
3	Croatia	CRO	https://media.api-sports.io/football/teams/3.png
9	Spain	SPA	https://media.api-sports.io/football/teams/9.png
10	England	ENG	https://media.api-sports.io/football/teams/10.png
14	Serbia	SER	https://media.api-sports.io/football/teams/14.png
15	Switzerland	SWI	https://media.api-sports.io/football/teams/15.png
21	Denmark	DEN	https://media.api-sports.io/football/teams/21.png
24	Poland	POL	https://media.api-sports.io/football/teams/24.png
25	Germany	GER	https://media.api-sports.io/football/teams/25.png
27	Portugal	POR	https://media.api-sports.io/football/teams/27.png
768	Italy	ITA	https://media.api-sports.io/football/teams/768.png
769	Hungary	HUN	https://media.api-sports.io/football/teams/769.png
770	Czech Republic	CZE	https://media.api-sports.io/football/teams/770.png
772	Ukraine	UKR	https://media.api-sports.io/football/teams/772.png
773	Slovakia	SLO	https://media.api-sports.io/football/teams/773.png
774	Romania	ROM	https://media.api-sports.io/football/teams/774.png
775	Austria	AUS	https://media.api-sports.io/football/teams/775.png
777	Turkey	TUR	https://media.api-sports.io/football/teams/777.png
778	Albania	ALB	https://media.api-sports.io/football/teams/778.png
1091	Slovenia	SLO	https://media.api-sports.io/football/teams/1091.png
1104	Georgia	GEO	https://media.api-sports.io/football/teams/1104.png
1108	Scotland	SCO	https://media.api-sports.io/football/teams/1108.png
1118	Netherlands	NET	https://media.api-sports.io/football/teams/1118.png
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
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- Name: fixtures fixtures_away_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_away_id_fkey FOREIGN KEY (away_id) REFERENCES public.teams(id);


--
-- Name: fixtures fixtures_home_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.fixtures
    ADD CONSTRAINT fixtures_home_id_fkey FOREIGN KEY (home_id) REFERENCES public.teams(id);


--
-- Name: groups groups_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: group77
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id);


--
-- PostgreSQL database dump complete
--

