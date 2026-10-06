from dataclasses import dataclass

@dataclass(frozen=True)
class Source:
    team: str
    gender: str
    url: str

# Authoritative project scope: 16 Maryland colleges / 31 NCAA soccer teams.
SOURCES = [
    Source("Maryland", "Men", "https://umterps.com/sports/mens-soccer/schedule/text"),
    Source("Maryland", "Women", "https://umterps.com/sports/womens-soccer/schedule/text"),
    Source("UMBC", "Men", "https://umbcretrievers.com/sports/mens-soccer/schedule/2026"),
    Source("UMBC", "Women", "https://umbcretrievers.com/sports/womens-soccer/schedule/2026"),
    Source("Mount St. Mary's", "Men", "https://mountathletics.com/sports/mens-soccer/schedule/2026"),
    Source("Mount St. Mary's", "Women", "https://mountathletics.com/sports/womens-soccer/schedule/2026"),
    Source("Loyola", "Men", "https://loyolagreyhounds.com/sports/mens-soccer/schedule/2026"),
    Source("Loyola", "Women", "https://loyolagreyhounds.com/sports/womens-soccer/schedule/2026"),
    Source("Navy", "Men", "https://navysports.com/sports/mens-soccer/schedule/2026"),
    Source("Navy", "Women", "https://navysports.com/sports/womens-soccer/schedule/2026"),
    Source("Towson", "Women", "https://towsontigers.com/sports/womens-soccer/schedule/2026"),
    Source("Frostburg State", "Men", "https://frostburgsports.com/sports/mens-soccer/schedule/2026"),
    Source("Frostburg State", "Women", "https://frostburgsports.com/sports/womens-soccer/schedule/2026"),
    Source("Goucher", "Men", "https://athletics.goucher.edu/sports/msoc/2026-27/schedule"),
    Source("Goucher", "Women", "https://athletics.goucher.edu/sports/wsoc/2026-27/schedule"),
    Source("Hood", "Men", "https://hoodathletics.com/sports/mens-soccer/schedule/2026"),
    Source("Hood", "Women", "https://hoodathletics.com/sports/womens-soccer/schedule/2026"),
    Source("Johns Hopkins", "Men", "https://hopkinssports.com/sports/mens-soccer/schedule/2026"),
    Source("Johns Hopkins", "Women", "https://hopkinssports.com/sports/womens-soccer/schedule/2026"),
    Source("McDaniel", "Men", "https://mcdanielathletics.com/sports/mens-soccer/schedule/2026"),
    Source("McDaniel", "Women", "https://mcdanielathletics.com/sports/womens-soccer/schedule/2026"),
    Source("Notre Dame (MD)", "Men", "https://notredamegators.com/sports/mens-soccer/schedule/2026"),
    Source("Notre Dame (MD)", "Women", "https://notredamegators.com/sports/womens-soccer/schedule/2026"),
    Source("Salisbury", "Men", "https://suseagulls.com/sports/mens-soccer/schedule/2026"),
    Source("Salisbury", "Women", "https://suseagulls.com/sports/womens-soccer/schedule/2026"),
    Source("St. Mary's", "Men", "https://smcmathletics.com/sports/mens-soccer/schedule/2026"),
    Source("St. Mary's", "Women", "https://smcmathletics.com/sports/womens-soccer/schedule/2026"),
    Source("Stevenson", "Men", "https://gomustangsports.com/sports/mens-soccer/schedule/2026"),
    Source("Stevenson", "Women", "https://gomustangsports.com/sports/womens-soccer/schedule/2026"),
    Source("Washington College", "Men", "https://washcollsports.com/sports/mens-soccer/schedule/2026"),
    Source("Washington College", "Women", "https://washcollsports.com/sports/womens-soccer/schedule/2026"),
]

TEAM_ALIASES = {
    "maryland": "maryland",
    "navy": "navy",
    "johns hopkins": "johns hopkins",
    "mcdaniel": "mcdaniel",
    "washington college": "washington college",
    "salisbury": "salisbury",
    "umbc": "umbc",
    "university of maryland baltimore county": "umbc",
    "stevenson": "stevenson",
    "hood": "hood",
    "notre dame md": "notre dame md",
    "mount st marys": "mount st marys",
    "catholic": "catholic",
    "franklin marshall": "franklin marshall",
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
