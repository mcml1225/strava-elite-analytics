"""
Database of elite athletes with their Strava profile URLs and metadata.
Source: Strava official article (July 2024)
"""

# Complete athlete database with 26 elite athletes across 6 disciplines
ATHLETES_DB = {
    # ==================== TRIATHLON (5 athletes) ====================
    "Matthew Hauser": {
        "strava_id": None,
        "strava_url": None,
        "discipline": "triathlon",
        "birth_year": 1998,
        "country": "Australia",
        "profile_type": "pro"
    },
    "Jeanne Lehair": {
        "strava_id": "20995449",
        "strava_url": "https://www.strava.com/athletes/20995449",
        "discipline": "triathlon",
        "birth_year": 1996,
        "country": "Luxembourg",
        "profile_type": "pro"
    },
    "Kristian Blummenfelt": {
        "strava_id": None,
        "strava_url": None,
        "discipline": "triathlon",
        "birth_year": 1994,
        "country": "Norway",
        "profile_type": "pro"
    },
    "Rachel Klamer": {
        "strava_id": None,
        "strava_url": None,
        "discipline": "triathlon",
        "birth_year": 1990,
        "country": "Netherlands",
        "profile_type": "pro"
    },
    "Alex Yee": {
        "strava_id": "21079580",
        "strava_url": "https://www.strava.com/athletes/21079580",
        "discipline": "triathlon",
        "birth_year": 1998,
        "country": "Great Britain",
        "profile_type": "pro"
    },

    # ==================== MARATHON (5 athletes) ====================
    "Gerda Steyn": {
        "strava_id": "17233801",
        "strava_url": "https://www.strava.com/pros/17233801",
        "discipline": "marathon",
        "birth_year": 1990,
        "country": "South Africa",
        "profile_type": "pro"
    },
    "Conner Mantz": {
        "strava_id": "33993248",
        "strava_url": "https://www.strava.com/pros/33993248",
        "discipline": "marathon",
        "birth_year": 1996,
        "country": "USA",
        "profile_type": "pro"
    },
    "Charlotte Purdue": {
        "strava_id": "4483415",
        "strava_url": "https://www.strava.com/pros/4483415",
        "discipline": "marathon",
        "birth_year": 1991,
        "country": "Great Britain",
        "profile_type": "pro"
    },
    "Clayton Young": {
        "strava_id": "23295862",
        "strava_url": "https://www.strava.com/pros/23295862",
        "discipline": "marathon",
        "birth_year": 1993,
        "country": "USA",
        "profile_type": "pro"
    },
    "Malindi Elmore": {
        "strava_id": "1861424",
        "strava_url": "https://www.strava.com/pros/1861424",
        "discipline": "marathon",
        "birth_year": 1980,
        "country": "Canada",
        "profile_type": "pro"
    },

    # ==================== ROAD CYCLING (4 athletes) ====================
    "Wout van Aert": {
        "strava_id": "189040",
        "strava_url": "https://www.strava.com/pros/189040",
        "discipline": "cycling",
        "birth_year": 1994,
        "country": "Belgium",
        "profile_type": "pro"
    },
    "Demi Vollering": {
        "strava_id": "16080090",
        "strava_url": "https://www.strava.com/pros/16080090",
        "discipline": "cycling",
        "birth_year": 1996,
        "country": "Netherlands",
        "profile_type": "pro"
    },
    "Remco Evenepoel": {
        "strava_id": "23069503",
        "strava_url": "https://www.strava.com/pros/23069503",
        "discipline": "cycling",
        "birth_year": 2000,
        "country": "Belgium",
        "profile_type": "pro"
    },
    "Marianne Vos": {
        "strava_id": "4196733",
        "strava_url": "https://www.strava.com/pros/4196733",
        "discipline": "cycling",
        "birth_year": 1987,
        "country": "Netherlands",
        "profile_type": "pro"
    },

    # ==================== TRACK & FIELD (5 athletes) ====================
    "Lizzie Bird": {
        "strava_id": "11686342",
        "strava_url": "https://www.strava.com/pros/11686342",
        "discipline": "track_field",
        "birth_year": 1994,
        "country": "Great Britain",
        "profile_type": "pro"
    },
    "Thierry Ndikumwenayo": {
        "strava_id": "80675140",
        "strava_url": "https://www.strava.com/pros/80675140",
        "discipline": "track_field",
        "birth_year": 1997,
        "country": "Spain",
        "profile_type": "pro"
    },
    "Marisa Howard": {
        "strava_id": "43684184",
        "strava_url": "https://www.strava.com/pros/43684184",
        "discipline": "track_field",
        "birth_year": 1992,
        "country": "USA",
        "profile_type": "pro"
    },
    "Matt Wilkinson": {
        "strava_id": "52485333",
        "strava_url": "https://www.strava.com/pros/52485333",
        "discipline": "track_field",
        "birth_year": 1999,
        "country": "USA",
        "profile_type": "pro"
    },
    "Corentin Le Clezio": {
        "strava_id": "23682243",
        "strava_url": "https://www.strava.com/pros/23682243",
        "discipline": "track_field",
        "birth_year": 1999,
        "country": "France",
        "profile_type": "pro"
    },

    # ==================== MOUNTAIN BIKE (3 athletes) ====================
    "Anne Terpstra": {
        "strava_id": "2976850",
        "strava_url": "https://www.strava.com/pros/2976850",
        "discipline": "mtb",
        "birth_year": 1991,
        "country": "Netherlands",
        "profile_type": "pro"
    },
    "Jordan Sarrou": {
        "strava_id": "1887858",
        "strava_url": "https://www.strava.com/pros/1887858",
        "discipline": "mtb",
        "birth_year": 1992,
        "country": "France",
        "profile_type": "pro"
    },
    "Puck Pieterse": {
        "strava_id": "13755668",
        "strava_url": "https://www.strava.com/pros/13755668",
        "discipline": "mtb",
        "birth_year": 2002,
        "country": "Netherlands",
        "profile_type": "pro"
    },

    # ==================== OTHER SPORTS (4 athletes) ====================
    "Joan Duru": {
        "strava_id": "5127375",
        "strava_url": "https://www.strava.com/pros/5127375",
        "discipline": "surfing",
        "birth_year": 1989,
        "country": "France",
        "profile_type": "pro"
    },
    "Johanne Defay": {
        "strava_id": "24471084",
        "strava_url": "https://www.strava.com/athletes/24471084",
        "discipline": "surfing",
        "birth_year": 1993,
        "country": "France",
        "profile_type": "pro"
    },
    "Jonas Ecker": {
        "strava_id": "15697853",
        "strava_url": "https://www.strava.com/pros/15697853",
        "discipline": "canoeing",
        "birth_year": 2001,
        "country": "USA",
        "profile_type": "pro"
    },
    "Hugo Beurey": {
        "strava_id": "133158846",
        "strava_url": "https://www.strava.com/pros/133158846",
        "discipline": "rowing",
        "birth_year": 1998,
        "country": "France",
        "profile_type": "pro"
    }
}


def get_athletes_by_discipline(discipline=None):
    """
    Get athletes filtered by discipline.
    
    Parameters:
    -----------
    discipline : str, optional
        Filter by discipline (e.g., 'marathon', 'cycling', 'triathlon')
    
    Returns:
    --------
    dict : Filtered dictionary of athletes
    """
    if discipline:
        return {name: data for name, data in ATHLETES_DB.items() 
                if data["discipline"] == discipline}
    return ATHLETES_DB


def get_active_athletes(require_strava_id=True):
    """
    Get athletes that have Strava IDs (active profiles).
    
    Parameters:
    -----------
    require_strava_id : bool, default True
        If True, only return athletes with non-None strava_id
    
    Returns:
    --------
    dict : Filtered dictionary of active athletes
    """
    if require_strava_id:
        return {name: data for name, data in ATHLETES_DB.items() 
                if data["strava_id"] is not None}
    return ATHLETES_DB


def get_athlete_ids():
    """
    Get dictionary of athlete names to Strava IDs.
    
    Returns:
    --------
    dict : {athlete_name: strava_id}
    """
    return {name: data["strava_id"] for name, data in ATHLETES_DB.items() 
            if data["strava_id"] is not None}


def get_discipline_summary():
    """
    Get summary count of athletes by discipline.
    
    Returns:
    --------
    pandas.DataFrame : Summary table
    """
    import pandas as pd
    disciplines = [data["discipline"] for data in ATHLETES_DB.values()]
    df = pd.Series(disciplines).value_counts().reset_index()
    df.columns = ["Discipline", "Count"]
    return df