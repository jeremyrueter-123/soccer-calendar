"""Configuration for the Maryland Soccer Calendar auditor."""

CALENDAR_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/"
    "pub?gid=924645803&single=true&output=csv"
)

# First-wave schools. Add additional official sources only after their parser
# output has been spot-checked.
SOURCES = [
    {"team": "Navy", "gender": "Men", "url": "https://navysports.com/sports/mens-soccer/schedule/2026"},
    {"team": "UMBC", "gender": "Men", "url": "https://umbcretrievers.com/sports/mens-soccer/schedule/2026"},
    {"team": "Johns Hopkins", "gender": "Men", "url": "https://hopkinssports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Washington College", "gender": "Men", "url": "https://washcollsports.com/sports/mens-soccer/schedule/2026"},
    {"team": "Salisbury", "gender": "Men", "url": "https://suseagulls.com/sports/mens-soccer/schedule/2026"},
    {"team": "Stevenson", "gender": "Men", "url": "https://gomustangsports.com/sports/mens-soccer/schedule/2026"},
    {"team": "McDaniel", "gender": "Men", "url": "https://mcdanielathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "Hood", "gender": "Men", "url": "https://hoodcollegeblazers.com/sports/mens-soccer/schedule/2026"},
    {"team": "Notre Dame (MD)", "gender": "Men", "url": "https://notredamegators.com/sports/mens-soccer/schedule/2026"},
    {"team": "Mount St. Mary's", "gender": "Men", "url": "https://mountathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "Catholic", "gender": "Men", "url": "https://catholicathletics.com/sports/mens-soccer/schedule/2026"},
    {"team": "UMBC", "gender": "Women", "url": "https://umbcretrievers.com/sports/womens-soccer/schedule/2026"},
    {"team": "Notre Dame (MD)", "gender": "Women", "url": "https://notredamegators.com/sports/womens-soccer/schedule/2026"},
    {"team": "Mount St. Mary's", "gender": "Women", "url": "https://mountathletics.com/sports/womens-soccer/schedule/2026"},
    {"team": "Washington College", "gender": "Women", "url": "https://washcollsports.com/sports/womens-soccer/schedule/2026"},
]

TEAM_ALIASES = {
    "maryland": "Maryland",
    "university of maryland": "Maryland",
    "maryland terrapins": "Maryland",
    "navy": "Navy",
    "naval academy": "Navy",
    "johns hopkins": "Johns Hopkins",
    "johns hopkins university": "Johns Hopkins",
    "mcdaniel": "McDaniel",
    "mcdaniel college": "McDaniel",
    "washington college": "Washington College",
    "washington (md)": "Washington College",
    "salisbury": "Salisbury",
    "salisbury university": "Salisbury",
    "umbc": "UMBC",
    "university of maryland baltimore county": "UMBC",
    "stevenson": "Stevenson",
    "hood": "Hood",
    "hood college": "Hood",
    "notre dame (md)": "Notre Dame (MD)",
    "notre dame of maryland": "Notre Dame (MD)",
    "mount st. mary's": "Mount St. Mary's",
    "mount st marys": "Mount St. Mary's",
    "mount st. marys": "Mount St. Mary's",
    "catholic": "Catholic",
    "catholic university": "Catholic",
    "franklin & marshall": "Franklin & Marshall",
    "franklin and marshall": "Franklin & Marshall",
    "st johns": "St. John's",
    "st marys": "St. Mary's",
    "university at albany": "Albany",
    "albany": "Albany",
    "university of vermont": "Vermont",
    "vermont": "Vermont",
    "boston u": "Boston University",
    "boston university": "Boston University",
    "university of delaware": "Delaware",
    "delaware": "Delaware",
    "university of new hampshire": "New Hampshire",
    "new hampshire": "New Hampshire",
    "university of massachusetts lowell": "UMass Lowell",
    "umass lowell": "UMass Lowell",
    "university at albany": "UAlbany",
    "ualbany": "UAlbany",
    "university of mary washington": "Mary Washington",
    "mary washington": "Mary Washington",
    "washington md": "Washington College",
    "washington": "Washington College",
    "york college of pennsylvania": "York (PA)",
    "york pa": "York (PA)",
}

STATUS_ALIASES = {
    "canceled": "Canceled",
    "cancelled": "Canceled",
    "no contest": "No Contest",
    "postponed": "Postponed",
    "suspended": "Suspended",
    "forfeit": "Forfeit",
    "tba": "Scheduled",
}
