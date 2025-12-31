#!/usr/bin/env python3
"""
Script to merge AMRYTT directory list into directories.json
Filters out entries with DR < 40 and identifies new entries only
"""

import json
import re

# Current directories.json path
DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# AMRYTT data (pasted from website)
AMRYTT_DATA = """
1	www.patreon.com/	93	6335483
2	sourceforge.net/	92	2354445
3	gumroad.com	91	394169
4	www.deviantart.com/	91	8083337
5	www.producthunt.com/	91	1071989
6	g2.com	91	965689
7	www.g2.com/	91	901259
8	www.gartner.com/en/digital-markets/claim-profile	91	6
9	capterra.com	90	946908
10	news.ycombinator.com/	90	1095069
11	dev.to/	90	889971
12	hackernoon.com/	88	266292
13	uneed.lemonsqueezy.com/	87	11
14	www.scoop.it	86	84551
15	appsumo.com/	84	273563
16	www.f6s.com/	83	316993
17	media-index.kochava.com/	81	3681
18	www.indiehackers.com/	80	12118
19	alternativeto.net/	80	685767
20	onepagelove.com/	80	32619
21	technologyadvice.com/	79	100063
22	list.ly/	78	12839
23	www.eu-startups.com/	77	113379
24	www.softwaresuggest.com/	77	144369
25	crozdesk.com/	75	21882
26	www.killerstartups.com/	74	4003
27	www.saasworthy.com/	73	54227
28	betalist.com/	73	28515
29	saasworthy.com	73	54227
30	www.startus.cc/	72	6201
31	land-book.com/	72	10871
32	www.saashub.com/	72	33679
33	alternative.me/	72	165048
34	www.webdesign-inspiration.com/	71	3655
35	dynamicbusiness.com/	71	7319
36	www.sideprojectors.com/	70	1897
37	www.serchen.com/	70	5789
38	www.bunity.com/	69	0
39	www.peerspot.com/	67	11590
40	startupstash.com/	67	3960
41	www.startupranking.com/	67	15392
42	pitchwall.co/	65	3899
43	peerlist.io/	65	15541
44	webdesignernews.com/	64	413
45	indiepa.ge/discover	62	0
46	www.ebool.com/	61	101
47	toolfinder.co/	61	26057
48	www.saasgenius.com/	59	9319
49	devhunt.org/	58	2934
50	fazier.com/	58	32
51	getmakerlog.com/	57	8
52	supertools.therundown.ai	57	421930
53	www.shno.co/	57	4402
54	www.startupguys.net/	57	10
55	www.spotsaas.com/	55	47864
56	wip.co/	55	730
57	famewall.io/landing-tools-directory/	55	0
58	www.curated.design/	53	1052
59	nocodefounders.com/	52	858
60	app.innmind.com/	51	124
61	www.alistdirectory.com/	51	2
62	www.launchingnext.com/submit/	48	3
63	cuspera.com	48	6384
64	www.techpluto.com/	48	3476
65	www.tinystartups.com/	47	25
66	www.toools.design/	45	12050
67	nocodelist.co/	43	874
68	microlaunch.net/	43	1035
69	seotoolbelt.co/	42	0
70	startuptracker.io/	42	32
71	discovercloud.com	39	10524
72	launched.io/	39	12
73	www.toolio.ai/	39	1416
74	crazyaboutstartups.com/	38	82
75	resource.fyi/	38	12
76	startupbuffer.com/	38	13916
77	thestartuppitch.com/	38	63
78	startups.watch/	38	103
79	ctrlalt.cc/	37	4
80	hunted.space/products	36	0
81	listskit.com/directorystarters/	35	0
82	www.thestartupinc.com/	35	100
83	startuplister.com/	34	20
84	tools.robingood.com/	34	185
85	www.promoteproject.com/	33	692
86	1000.tools/	33	56
87	devresourc.es/	33	1043
88	www.affordhunt.com/	32	11
89	postmake.io/	32	1140
90	saaspo.com/	32	1760
91	earlyshark.com/	31	947
92	www.spaceleads.pro/indie-founders-wall-of-fame	30	0
93	www.indielogs.com/	29	4
94	startupdope.com/	29	28
95	startup88.com/	28	117
96	www.startupspotlight.co/	27	0
97	www.betafy.co/	27	1
98	10words.io/	26	27
99	startupstage.app/	26	22
100	make.rs/	26	13
101	www.startups.fyi/	25	1
102	saassurf.com/	25	34
103	www.disrupt500.com/	25	64
104	www.joinly.xyz/	24	3
105	owwly.com/	23	86
106	yesramen.com/	23	0
107	startupcollections.com/	23	1829
108	indiemaker.space/	23	10
109	onigiri.one/tools	23	0
110	freakyseo.com/	22	1153
111	appsandwebsites.com/	21	2
112	opengraphexamples.com/	21	39
113	startupeurope.net/	20	1
114	www.early.tools/	20	0
115	www.cloudfindr.co/	19	0
116	insanelycooltools.com/	19	26
117	www.bufferapps.com/	18	0
118	once.tools/	18	3
119	www.indietool.io/	18	6
120	payoncealternatives.com/	18	88
121	bestwebdesigntools.com/	16	1
122	saasscreenshots.com/	16	38
123	awesomeindie.com/	15	314
124	under1000mrr.tools/	14	0
125	www.internetisbeautiful.com/	14	0
126	growthjunkie.com/	14	143
127	indieaffiliate.io/	13	0
128	toolbattles.com/	13	0
129	productcanyon.com/	13	8
130	www.bestaffiliateprograms.io/	12	41
131	ecommerce-stack.com/	12	0
132	saasgallery.com/	12	0
133	www.getbyte.tech/	11	0
134	www.websitehunt.co/	11	4765
135	1payment.tools/	11	2
136	taalk.com/	11	969
137	www.makermove.com/	9	0
138	allhrsoftware.com/	9	126
139	twelve.tools/	9	0
140	awesomemarketingwebsites.com/	9	45
141	tools.landin.page/	7	0
142	foundertools.co/	6	0
143	www.prodpapa.com/	6	0
144	buildinpublic.page/	5	0
145	startuptile.com/	4.6	0
146	primeindies.com/	4.3	24
147	feedbrew.com/	3.7	0
148	startuproulette.com/	3.1	0
149	www.findcool.tools/	3.1	0
150	mavtools.com/	2.7	1548
151	feedbacktools.org/	2.7	0
152	www.saasrefs.com/	2.6	8
153	www.businesstoolvault.com/	2.4	0
154	lazyhunt.com/	2	0
155	www.indiehacker.tools/	1.9	0
156	extendhunt.com/	1.9	0
157	allonce.co/	1.8	0
158	www.justfree.io/	1.7	19
159	handpickedtools.com/	1.6	0
160	www.webpostz.com/	1.3	9
161	700.tools/	1.2	0
162	onlyforcreators.com/	1.2	0
163	www.submityour.tools/	0.9	1
164	www.indieproducts.io/	0.9	0
165	saasaffiliates.co/	0.8	0
166	findthe.tools/	0.7	1
167	www.makerthrive.com/	0.1	0
168	www.b2btools.tech/	0	0
169	toolty.website/	0	0
"""

def extract_name(url_string):
    """Extract clean name from URL string"""
    # Remove trailing slash and www.
    url = url_string.strip()
    if url.endswith('/'):
        url = url[:-1]
    if url.startswith('www.'):
        url = url[4:]
    
    # Split by dots and hyphens to get first part (name)
    parts = re.split(r'[.\-]', url.lower())
    name = parts[0]
    
    return name

def parse_amrytt():
    """Parse AMRYTT data and return list of dicts"""
    entries = []
    for line in AMRYTT_DATA.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 3:
            try:
                num = int(parts[0])
                url = parts[1].strip()
                dr = float(parts[2])
                
                if dr >= 40:  # Only include DR >= 40
                    name = extract_name(url)
                    entries.append({
                        'name': name,
                        'url': url,
                        'dr': dr,
                        'num': num
                    })
            except:
                pass
    return entries

def load_existing():
    """Load existing directories.json"""
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    return data

def find_new_entries(amrytt_entries, existing_data):
    """Find entries in AMRYTT not in existing data"""
    existing_names = {dir['name'].lower(): dir for dir in existing_data['directories']}
    existing_urls = {dir['url'].lower() for dir in existing_data['directories']}
    
    new_entries = []
    duplicates_found = []
    
    for entry in amrytt_entries:
        name_lower = entry['name'].lower()
        url_lower = entry['url'].lower()
        
        if name_lower in existing_names or url_lower in existing_urls:
            duplicates_found.append(entry)
        else:
            new_entries.append(entry)
    
    return new_entries, duplicates_found

def main():
    print("Parsing AMRYTT data (DR >= 40)...")
    amrytt = parse_amrytt()
    print(f"Found {len(amrytt)} entries with DR >= 40")
    
    print(f"\nLoading existing directories.json...")
    existing = load_existing()
    print(f"Currently have {len(existing['directories'])} directories")
    
    print(f"\nFinding new entries...")
    new_entries, dupes = find_new_entries(amrytt, existing)
    
    print(f"\n=== RESULTS ===")
    print(f"New entries to add: {len(new_entries)}")
    print(f"Already in database: {len(dupes)}")
    print(f"Filtered out (DR < 40): {len(amrytt) - len(new_entries) - len(dupes)}")
    
    print(f"\n=== NEW ENTRIES (DR >= 40) ===")
    for entry in new_entries:
        print(f"{entry['num']:3d}. {entry['url']:40s} DR: {entry['dr']:5.1f}")
    
    return new_entries

if __name__ == "__main__":
    new = main()
