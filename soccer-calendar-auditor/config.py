"""Configuration for the Maryland Soccer Calendar auditor."""

CALENDAR_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/"
    "pub?gid=924645803&single=true&output=csv"
)

# Authoritative Maryland college soccer scope: 31 NCAA teams across 16 schools.
# Catholic is intentionally excluded; it is in Washington, D.C.
SOURCES = [
    # Division I
    {"team": "Maryland", "gender": "Men", "url": "https://umterps.com/sports/mens-soccer/schedule/text"},
    {"team": "Maryland", "gender": "Women", "url": "https://umterps.com/sports/womens-soccer/schedule/text"},
    {"team": "UMBC", "gender": "Men", "url": "https://umbcretrievers.com/sports/mens-soccer/schedule/2026"},
    {"team": "UMBC", "gender": "Women", "url": "https://umbcretrievers.com/sports/womens-soccer/schedule/2026"},
    {"team": "Mount St. Mary's", "gender": "Men", "url": "https://mountathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "Mount St. Mary's", "gender": "Women", "url": "https://mountathletics.com/sports/womens-soccer/schedule/2026"},
    {"team": "Loyola", "gender": "Men", "url": "https://loyolagreyhounds.com/sports/mens-soccer/schedule/2026"},
    {"team": "Loyola", "gender": "Women", "url": "https://loyolagreyhounds.com/sports/womens-soccer/schedule/2026"},
    {"team": "Navy", "gender": "Men", "url": "https://navysports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Navy", "gender": "Women", "url": "https://navysports.com/sports/womens-soccer/schedule/2026"},
    {"team": "Towson", "gender": "Women", "url": "https://towsontigers.com/sports/womens-soccer/schedule/2026"},

    # Division II
    {"team": "Frostburg State", "gender": "Men", "url": "https://frostburgsports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Frostburg State", "gender": "Women", "url": "https://frostburgsports.com/sports/womens-soccer/schedule/2026"},

    # Division III
    {"team": "Johns Hopkins", "gender": "Men", "url": "https://hopkinssports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Johns Hopkins", "gender": "Women", "url": "https://hopkinssports.com/sports/womens-soccer/schedule/2026"},
    {"team": "McDaniel", "gender": "Men", "url": "https://mcdanielathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "McDaniel", "gender": "Women", "url": "https://mcdanielathletics.com/sports/womens-soccer/schedule/2026"},
    {"team": "Washington College", "gender": "Men", "url": "https://washcollsports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Washington College", "gender": "Women", "url": "https://washcollsports.com/sports/womens-soccer/schedule/2026"},
    {"team": "Salisbury", "gender": "Men", "url": "https://suseagulls.com/sports/mens-soccer/schedule/2026"},
    {"team": "Salisbury", "gender": "Women", "url": "https://suseagulls.com/sports/womens-soccer/schedule/2026"},
    {"team": "Goucher", "gender": "Men", "url": "https://athletics.goucher.edu/sports/msoc/2026-27/schedule"},
    {"team": "Goucher", "gender": "Women", "url": "https://athletics.goucher.edu/sports/wsoc/2026-27/schedule"},
    {"team": "Hood", "gender": "Men", "url": "https://hoodathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "Hood", "gender": "Women", "url": "https://hoodathletics.com/sports/womens-soccer/schedule/2026"},
    {"team": "Notre Dame (MD)", "gender": "Men", "url": "https://notredamegators.com/sports/mens-soccer/schedule/2026"},
    {"team": "Notre Dame (MD)", "gender": "Women", "url": "https://notredamegators.com/sports/womens-soccer/schedule/2026"},
    {"team": "St. Mary's", "gender": "Men", "url": "https://smcmathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "St. Mary's", "gender": "Women", "url": "https://smcmathletics.com/sports/womens-soccer/schedule/2026"},
    {"team": "Stevenson", "gender": "Men", "url": "https://gomustangsports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Stevenson", "gender": "Women", "url": "https://gomustangsports.com/sports/womens-soccer/schedule/2026"},
]

TEAM_ALIASES = {
    "maryland": "Maryland", "university of maryland": "Maryland", "maryland terrapins": "Maryland",
    "navy": "Navy", "naval academy": "Navy", "united states naval academy": "Navy",
    "johns hopkins": "Johns Hopkins", "johns hopkins university": "Johns Hopkins",
    "mcdaniel": "McDaniel", "mcdaniel college": "McDaniel",
    "washington college": "Washington College", "washington (md)": "Washington College", "washington md": "Washington College",
    "salisbury": "Salisbury", "salisbury university": "Salisbury",
    "umbc": "UMBC", "university of maryland baltimore county": "UMBC",
    "stevenson": "Stevenson", "stevenson university": "Stevenson",
    "hood": "Hood", "hood college": "Hood", "hood university": "Hood",
    "notre dame (md)": "Notre Dame (MD)", "notre dame of maryland": "Notre Dame (MD)",
    "mount st. mary's": "Mount St. Mary's", "mount st marys": "Mount St. Mary's", "mount st. marys": "Mount St. Mary's", "mount saint mary": "Mount St. Mary's", "mount saint marys": "Mount St. Mary's",
    "franklin & marshall": "Franklin & Marshall", "franklin and marshall": "Franklin & Marshall",
    "st johns": "St. John's", "st. johns": "St. John's",
    "st marys": "St. Mary's", "st. marys": "St. Mary's", "st. mary's": "St. Mary's", "saint marys": "St. Mary's",
    "university at albany": "UAlbany", "albany": "UAlbany", "ualbany": "UAlbany",
    "university of vermont": "Vermont", "vermont": "Vermont",
    "boston u": "Boston University", "boston university": "Boston University",
    "university of delaware": "Delaware", "delaware": "Delaware",
    "university of new hampshire": "New Hampshire", "new hampshire": "New Hampshire",
    "university of massachusetts lowell": "UMass Lowell", "umass lowell": "UMass Lowell",
    "university of mary washington": "Mary Washington", "mary washington": "Mary Washington",
    "york college of pennsylvania": "York (PA)", "york pa": "York (PA)", "york (pa)": "York (PA)", "york": "York (PA)",
    "american": "American", "american university": "American",
    "catholic": "Catholic", "catholic university": "Catholic",
    "towson": "Towson", "towson university": "Towson",
    "loyola": "Loyola", "loyola university maryland": "Loyola", "loyola (md)": "Loyola",
    "elizabethtown": "Elizabethtown", "elizabethtown college": "Elizabethtown",
    "gallaudet": "Gallaudet", "gallaudet university": "Gallaudet",
    "delaware valley": "Delaware Valley", "delaware valley university": "Delaware Valley",
    "shenandoah": "Shenandoah", "shenandoah university": "Shenandoah",
    "carlow": "Carlow", "carlow university": "Carlow",
    "robert morris": "Robert Morris", "robert morris university": "Robert Morris",
    "longwood": "Longwood", "longwood university": "Longwood",
    "messiah": "Messiah", "messiah university": "Messiah",
    "eastern": "Eastern", "eastern university": "Eastern",
    "neumann": "Neumann", "neumann university": "Neumann",
    "albright": "Albright", "albright college": "Albright",
    "widener": "Widener", "widener university": "Widener",
    "ursinus": "Ursinus", "ursinus college": "Ursinus",
    "muhlenberg": "Muhlenberg", "muhlenberg college": "Muhlenberg",
    "dickinson": "Dickinson", "dickinson college": "Dickinson",
    "north carolina wesleyan": "NC Wesleyan", "nc wesleyan": "NC Wesleyan",
    "saint peter s": "Saint Peter's", "saint peters": "Saint Peter's", "st peters": "Saint Peter's",
    "frostburg state": "Frostburg State", "frostburg state university": "Frostburg State",
    "goucher": "Goucher", "goucher college": "Goucher",
    "cairn": "Cairn", "cairn university": "Cairn",
    "marywood": "Marywood", "marywood university": "Marywood",
    "penn state brandywine": "Penn State Brandywine", "penn st brandywine": "Penn State Brandywine",
    "penn state harrisburg": "Penn State Harrisburg", "penn st harrisburg": "Penn State Harrisburg",
    "penn state abington": "Penn State Abington", "penn st abington": "Penn State Abington",
    "penn state berks": "Penn State Berks", "penn st berks": "Penn State Berks",
}

STATUS_ALIASES = {
    "canceled": "Canceled", "cancelled": "Canceled", "no contest": "No Contest",
    "postponed": "Postponed", "suspended": "Suspended", "forfeit": "Forfeit", "tba": "Scheduled",
}
