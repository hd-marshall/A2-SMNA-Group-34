import csv
import pandas as pd
import requests
import re
from typing import List, Dict, Tuple

def create_met_gala_csv(output_file='met_gala_attendees.csv'):
    """Create a CSV with Met Gala attendees, years, and genders."""
    # Prepare data
    data = []
    
    # Add 2022 attendees
    for attendee in attendees2022:
        data.append({
            'Name': attendee,
            'Year': 2022,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2023 attendees
    for attendee in attendees2023:
        data.append({
            'Name': attendee,
            'Year': 2023,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2024 attendees
    for attendee in attendees2024:
        data.append({
            'Name': attendee,
            'Year': 2024,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2025 attendees
    for attendee in attendees2025:
        data.append({
            'Name': attendee,
            'Year': 2025,
            'Gender': determine_gender(attendee)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print(f"CSV file created successfully: {output_file}")
    print(f"Total entries: {len(data)}")
    print(f"2022 entries: {len(attendees2022)}")
    print(f"2023 entries: {len(attendees2023)}")
    print(f"2024 entries: {len(attendees2024)}")
    print(f"2025 entries: {len(attendees2025)}")
    
    # Display summary of gender distribution
    gender_counts = df['Gender'].value_counts()
    print("\nGender Distribution:")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")
    
    return df

# extract 2021 data
attendees2021 = [
    "Billie Eilish", "A$AP Rocky", "Rihanna", "Jennifer Lopez", "Lil Nas X", 
    "Lorde", "Timothée Chalamet", "Iman", "Kaia Gerber", "Kendall Jenner", 
    "Zoë Kravitz", "Gigi Hadid", "Maisie Williams", "Jennifer Hudson", "Emily Ratajkowski", 
    "Emily Blunt", "Ciara", "Megan Fox", "Lily-Rose Depp", "Shawn Mendes", 
    "Camilla Cabello", "Justin Bieber", "Hailey Bieber", "Kim Kardashian", "Rosé", 
    "Carey Mulligan", "Kristen Stewart", "Gemma Chan", "Yara Shahidi", "Normani", 
    "Olivia Rodrigo", "Lupita Nyong'o", "Grimes", "Brooklyn Beckham", "Nicola Peltz", 
    "Naomi Osaka", "Emma Chamberlain", "Keke Palmer", "Karlie Kloss", "Wes Gordon", 
    "Hailee Steinfeld", "Megan Thee Stallion", "Tracee Ellis Ross", "Eiza González", 
    "Dan Levy", "Tom Ford", "Ella Emhoff", "Lili Reinhart", "Barbie Ferreira", 
    "Anok Yai", "Ilana Glazer", "Zoey Deutch", "Saweetie", "Julia Garner", 
    "Evan Mock", "Kit Harington", "Rose Leslie", "Taraji P. Henson", "Troye Sivan", 
    "Serena Williams", "Alexis Ohanian", "Rachel Smith", "Adrien Brody", "Georgina Chapman", 
    "Anna Wintour", "Elliot Page", "Madison Beer", "Carolyn B. Maloney", "Amanda Gorman", 
    "Eva Chen", "Alicia Quarles", "Finneas", "Bee Carrozzini", "Adam Mosseri", 
    "Monica Mosseri", "Nia Dennis", "Charles Shaffer", "Elizabeth Cordry Shaffer", "Julia Carey", 
    "James Corden", "Sophia Roe", "Leon Bridges", "Valentina Sampaio", "Storm Reid", 
    "Chance the Rapper", "Kirsten Corley", "Jordan Roth", "Zac Posen", "Debbie Harry", 
    "Ben Platt", "Kim Petras", "Mj Rodriguez", "Nikkie de Jager", "Irina Shayk", 
    "Addison Rae", "Pete Davidson", "Channing Tatum", "Rachel Zegler", "Cynthia Erivo", 
    "Diane von Furstenberg", "Lourdes Leon", "Donatella Versace", "Megan Rapinoe", "Precious Lee", 
    "Chloe Fineman", "Kris Jenner", "Mary J. Blige", "Imaan Hammam", "Gillian Anderson", 
    "Dominic Cooper", "Frank Ocean", "Taylor Hill", "Jordan Alexander", "Alexandria Ocasio-Cortez", 
    "Aurora James", "Mindy Kaling", "Virgil Abloh", "Sienna Miller", "Taika Waititi", 
    "Rita Ora", "Gabrielle Union", "Claire Danes", "Hugh Dancy", "Chloe Bailey", 
    "Halle Bailey", "Alicia Keys", "Sharon Stone", "Winnie Harlow", "Kate Hudson", 
    "Tessa Thompson", "Cara Delevingne", "Vittoria Ceretti", "Hunter Schafer", "Laura Harrier", 
    "Diane Kruger", "Whoopi Goldberg", "Janet Mock", "Lily Aldridge", "Paloma Elsesser", 
    "Adut Akech", "Sunisa Lee", "Isabelle Huppert", "Aldis Hodge", "Alton Mason",
    "Maluma"
]

# Extract 2022 attendees from the provided document
attendees2022 = [
    "Blake Lively", "Pete Davidson", "Kim Kardashian", "Bella Hadid", "Gigi Hadid",
    "Hailey Bieber", "Billie Eilish", "Kaia Gerber", "Kylie Jenner", "Simone Ashley",
    "Kendall Jenner", "Olivia Rodrigo", "Emily Ratajkowski", "Dakota Johnson", "Ryan Reynolds",
    "Joe Jonas", "Sophie Turner", "Emma Stone", "Eiza González", "Carey Mulligan",
    "Cardi B", "Cara Delevingne", "Gemma Chan", "Sarah Jessica Parker", "Sydney Sweeney",
    "Maude Apatow", "Phoebe Dynevor", "Hoyeon Jung", "Julianne Moore", "Chloë Grace Moretz",
    "Glenn Close", "Cynthia Erivo", "Alexa Chung", "Lizzo", "Claire Danes",
    "Hugh Dancy", "Camila Mendes", "Alexandre Mattiussi", "Vanessa Hudgens", "Nicola Coughlan",
    "Emma Chamberlain", "Miranda Kerr", "Anna Wintour", "Brooklyn Beckham", "Nicola Peltz Beckham",
    "Jessica Chastain", "Janelle Monáe", "Gwen Stefani", "Camila Cabello", "Michelle Yeoh",
    "Shawn Mendes", "Daisy Edgar-Jones", "Amy Schumer", "Jeremy Scott", "Ariana DeBose",
    "Tessa Thompson", "Austin Butler", "Mindy Kaling", "Kacey Musgraves", "Adrien Brody",
    "Georgina Chapman", "Sebastian Stan", "Joan Smalls", "Evan Mock", "Ashley Park",
    "Amber Valletta", "Winnie Harlow", "Vanessa Nadal", "Lin-Manuel Miranda", "Venus Williams",
    "Hillary Clinton", "Paloma Elsesser", "Anderson Paak", "Ansel Elgort", "Laura Harrier",
    "Tommy Dorfman", "Quannah Chasinghorse", "Priscilla Presley", "Ben Winston", "Meredith Winston",
    "Francesco Carrozzini", "Bee Carrozzini", "Wendi Murdoch", "La La Anthony", "Hamish Bowles",
    "Autumn de Wilde", "Janicza Bravo", "Mark Guiducci", "Allie Michler", "Fabiola Beracasa Beckman",
    "Lisa Love", "Willow Lindley", "Eaddy Kiernan", "Steve Newhouse", "Gina Sanders",
    "Elizabeth Schaffer", "Amirah Kassem", "Adrienne Adams", "Caroline Wozniacki", "Annie Leibovitz",
    "Samuelle Leibovitz", "Lisa Airan", "Tom Ford", "Isabelle Boemeke", "Joe Gebbia",
    "Alicia Keys", "Paapa Essiedu", "Charlotte Tilbury", "Chloe Kim", "Jordan Roth",
    "Renée Elise Goldsberry", "Renate Reinsve", "Kodi Smit-McPhee", "Bradley Cooper", "Phoebe Bridgers",
    "Kris Jenner", "Precious Lee", "Rachel Brosnahan", "Megan Thee Stallion", "Caroline Trentini",
    "Sabrina Carpenter", "Shalom Harlow", "Danai Gurira", "Taylor Hill", "Madelaine Petsch",
    "Kiki Layne", "Lenny Kravitz", "Normani", "Regé-Jean Page", "Future",
    "Sigourney Weaver", "Naomi Campbell", "Irina Shayk", "Dove Cameron", "Chloe Bailey",
    "Lily Aldridge", "Jasmine Tookes", "Addison Rae", "Maisie Williams", "SZA",
    "Awkwafina", "Rachel Smith", "Emma Corrin", "Nicki Minaj"
]

# Extract 2023 attendees from the provided document
attendees2023 = [
    "A$AP Rocky", "Rihanna", "Kim Kardashian", "Kendall Jenner", "Kylie Jenner",
    "Jennifer Lopez", "Jared Leto", "Lil Nas X", "Florence Pugh", "Bad Bunny",
    "Pedro Pascal", "Anne Hathaway", "Jenna Ortega", "Serena Williams", "Alexis Ohanian",
    "Barry Keoghan", "Ke Huy Quan", "Amanda Seyfried", "Erykah Badu", "Lily Collins",
    "Olivia Rodrigo", "Teyana Taylor", "Keke Palmer", "Doja Cat", "Salma Hayek",
    "Brian Tyree Henry", "Jessica Chastain", "Michaela Coel", "Halle Bailey", "Irina Shayk",
    "Jonathan Groff", "Kate Moss", "Margot Robbie", "Naomi Campbell", "Ice Spice",
    "Gisele Bündchen", "Ariana DeBose", "Quinta Brunson", "Anok Yai", "Philippa Soo",
    "David Byrne", "Nicole Kidman", "Emily Ratajkowski", "Josh Groban", "Natalie McQueen",
    "Phoebe Bridgers", "Rita Ora", "Penélope Cruz", "Emma Chamberlain", "Dua Lipa",
    "Kate Hudson", "Gigi Hadid", "Elle Fanning", "Hugh Jackman", "Janelle Monae",
    "Emily Blunt", "Lily James", "Pete Davidson", "Michelle Yeoh", "Nick Jonas",
    "Priyanka Chopra", "Simu Liu", "Glenn Close", "Naomi Ackie", "Ashley Park",
    "Maluma", "Camila Morrone", "Mindy Kaling", "Roger Federer", "Anna Wintour"
]

# Extract 2025 attendees from the JavaScript data
attendees2025 = [
  "Pharrell Williams", "Lewis Hamilton", "Colman Domingo", "A$AP Rocky", "Debbie Allen", 
  "Norman Nixon", "Pamela Anderson", "André 3000", "La La Anthony", "Babyface", 
  "Bad Bunny", "Halle Bailey", "Monica Barbaro", "Halle Berry", "Hailey Bieber", 
  "Simone Biles", "Mary J. Blige", "Stella McCartney", "Adrien Brody", "Georgina Chapman", 
  "Rachel Brosnahan", "Quinta Brunson", "Cardi B", "Sabrina Carpenter", "Emma Chamberlain", 
  "Charli XCX", "James Corden", "Julia Carey", "Miley Cyrus", "Dapper Dan", 
  "Andra Day", "Lana Del Rey", "Alessandro Michele", "Doechii", "Doja Cat", 
  "Raúl Domingo", "Ayo Edebiri", "Tracee Ellis Ross", "Cynthia Erivo", "Walton Goggins", 
  "Whoopi Goldberg", "Jeff Goldblum", "Gigi Hadid", "Zuri Hall", "Laura Harrier", 
  "Anne Hathaway", "Maya Hawke", "Lauryn Hill", "Damson Idris", "Kendall Jenner", 
  "Kylie Jenner", "Coco Jones", "Radhika Jones", "Nick Jonas", "Priyanka Chopra Jonas", 
  "Colin Kaepernick", "Nessa Diab", "Mindy Kaling", "Kim Kardashian", "Barry Keoghan", 
  "Alicia Keys", "Swizz Beatz", "Nicole Kidman", "Regina King", "Karlie Kloss", 
  "Christian Latchman", "Dua Lipa", "Lizzo", "Lorde", "Madonna", 
  "Audra McDonald", "Megan Thee Stallion", "Nicki Minaj", "Janelle Monáe", "Demi Moore", 
  "Alex Newell", "Ego Nwodim", "Kwame Onwuachi", "Regé-Jean Page", "Keke Palmer", 
  "Natasha Lyonne", "Jeremy Pope", "Gina Alice Redlinger", "Sofia Richie", "Rihanna", 
  "Chappell Roan", "Rosalía", "Jordan Roth", "Diana Ross", "Evan Ross", 
  "Zoë Saldaña", "Anna Sawai", "Nicole Scherzinger", "Andrew Scott", "Jonathan Simkhai", 
  "Kerry Washington", "Shakira", "Sadie Sink", "Sam Smith", "Sarah Snook", 
  "Breanna Stewart", "Sydney Sweeney", "Teyana Taylor", "Tramell Tillman", "Dwyane Wade", 
  "Gabrielle Union", "Suki Waterhouse", "Jeremy Allen White", "Helen Lasichanh", "Serena Williams", 
  "Anna Wintour", "Aimee Lou Wood", "Patrick Schwarzenegger", "Zendaya", "LeBron James",
  "Ugbad Abdi", "Huma Abedin", "Haider Ackermann", "Adrienne E. Adams", "Joseph J. Adams",
  "Kiara Advani", "Adut Akech", "Isha Ambani", "J Balvin", "Valentina Ferrer",
  "Saquon Barkley", "Angela Bassett", "Jon Batiste", "Pietro Beccari", "Elisabetta Beccari",
  "Tyson Beckford", "Oswald Boateng", "Hanna Hultberg", "Andreew Bolton", "Hamish Bowles",
  "Burna Boy", "Ev Bravado", "Janicza Bravo", "Gale A. Brewer", "Leon Bridges",
  "Thom Browne", "Tory Burch", "Bee Carrozzini", "Francesco Carrozzini", "Ruth E. Carter",
  "Charlie Casely-Hayford", "Jordan Casteel", "Central Cee", "Miles Chamley-Watson", "Chance the Rapper"
]

# Extract 2024 attendees
attendees2024 = [
  "Zendaya", "Cardi B", "Nicki Minaj", "Camila Cabello", "Donatella Versace", "Andrew Scott", 
  "Jude Law", "Kylie Jenner", "Nicole Kidman", "Keith Urban", "FKA Twigs", "Willow Smith", 
  "Jaden Smith", "Taraji P. Henson", "Elizabeth Debicki", "Charlie Hunnam", "Kieran Culkin", 
  "Jazz Charton", "Awkwafina", "Usher", "Chase Stokes", "Kelsea Ballerini", "Sydney Sweeney", 
  "Michelle Yeoh", "Sabrina Carpenter", "Dwyane Wade", "Gabrielle Union", "Shakira", 
  "Cara Delevingne", "Ed Sheeran", "Dua Lipa", "Lil Nas X", "Rachel Zegler", "Meg Ryan", 
  "Kerry Washington", "Demi Lovato", "Phoebe Dynevor", "Naomi Watts", "Lana Del Rey", 
  "Kim Kardashian", "Lily Gladstone", "Serena Williams", "Kendall Jenner", "Pamela Anderson", 
  "Adrien Brody", "Georgina Chapman", "Queen Latifah", "Karol G", "Sam Smith", "Janelle Monáe",
  "Keke Palmer", "Ariana Grande", "Cynthia Erivo", "Riley Keough", "Charli XCX", "Troye Sivan",
  "Amanda Gorman", "Jodie Turner-Smith", "Barry Keoghan", "Doja Cat", "Brie Larson",
  "Amanda Seyfried", "Da'Vine Joy Randolph", "Jeff Goldblum", "Elle Fanning", "Demi Moore",
  "Hugh Jackman", "Dove Cameron", "Penelope Cruz", "Kylie Minogue", "Emma Wall", "Jeremy Strong",
  "Nicholas Galitzine", "Kris Jenner", "Corey Gamble", "Jessica Biel", "Sarah Jessica Parker",
  "Andy Cohen", "Greta Lee", "Uma Thurman", "Ambika Mod", "Stray Kids", "Jon Batiste"
]

def determine_gender(name: str) -> str:
    """
    Function to determine gender based on name.
    This uses common naming conventions and a predefined list of celebrities.
    
    For a production version, you would use a more robust API or database.
    """
    # Dictionary of known celebrities and their genders
    known_celebrities = {
        # Male celebrities
        "Pharrell Williams": "Male", "Lewis Hamilton": "Male", "Colman Domingo": "Male",
        "A$AP Rocky": "Male", "Norman Nixon": "Male", "André 3000": "Male",
        "Babyface": "Male", "Bad Bunny": "Male", "Adrien Brody": "Male",
        "James Corden": "Male", "Dapper Dan": "Male", "Alessandro Michele": "Male",
        "Walton Goggins": "Male", "Jeff Goldblum": "Male", "Damson Idris": "Male",
        "Nick Jonas": "Male", "Colin Kaepernick": "Male", "Barry Keoghan": "Male",
        "Swizz Beatz": "Male", "Christian Latchman": "Male", "Jeremy Pope": "Male",
        "Jordan Roth": "Male", "Evan Ross": "Male", "Andrew Scott": "Male",
        "Sam Smith": "Non-binary", "Tramell Tillman": "Male", "Dwyane Wade": "Male", 
        "Jeremy Allen White": "Male", "Patrick Schwarzenegger": "Male", "LeBron James": "Male",
        "Jude Law": "Male", "Keith Urban": "Male", "Jaden Smith": "Male",
        "Charlie Hunnam": "Male", "Kieran Culkin": "Male", "Usher": "Male",
        "Chase Stokes": "Male", "Ed Sheeran": "Male", "Lil Nas X": "Male",
        "Troye Sivan": "Male", "Hugh Jackman": "Male", "Jeremy Strong": "Male",
        "Nicholas Galitzine": "Male", "Corey Gamble": "Male", "Andy Cohen": "Male",
        "Jon Batiste": "Male", "Haider Ackermann": "Male", "Joseph J. Adams": "Male",
        "J Balvin": "Male", "Saquon Barkley": "Male", "Tyson Beckford": "Male",
        "Oswald Boateng": "Male", "Andreew Bolton": "Male", "Hamish Bowles": "Male",
        "Burna Boy": "Male", "Ev Bravado": "Male", "Leon Bridges": "Male",
        "Thom Browne": "Male", "Francesco Carrozzini": "Male", "Charlie Casely-Hayford": "Male",
        "Central Cee": "Male", "Miles Chamley-Watson": "Male", "Chance the Rapper": "Male",
        "Pedro Pascal": "Male", "Alexis Ohanian": "Male", "Ke Huy Quan": "Male",
        "Brian Tyree Henry": "Male", "Jonathan Groff": "Male", "David Byrne": "Male",
        "Josh Groban": "Male", "Pete Davidson": "Male", "Simu Liu": "Male",
        "Maluma": "Male", "Roger Federer": "Male", "Ryan Reynolds": "Male",
        "Joe Jonas": "Male", "Hugh Dancy": "Male", "Alexandre Mattiussi": "Male",
        "Brooklyn Beckham": "Male", "Jeremy Scott": "Male", "Austin Butler": "Male",
        "Sebastian Stan": "Male", "Evan Mock": "Male", "Lin-Manuel Miranda": "Male",
        "Anderson Paak": "Male", "Ansel Elgort": "Male", "Ben Winston": "Male",
        "Mark Guiducci": "Male", "Steve Newhouse": "Male", "Tom Ford": "Male",
        "Joe Gebbia": "Male", "Paapa Essiedu": "Male", "Kodi Smit-McPhee": "Male",
        "Bradley Cooper": "Male", "Lenny Kravitz": "Male", "Regé-Jean Page": "Male",
        "Future": "Male", "Shawn Mendes": "Male",
        
        # Female celebrities
        "Debbie Allen": "Female", "Pamela Anderson": "Female", "La La Anthony": "Female",
        "Halle Bailey": "Female", "Monica Barbaro": "Female", "Halle Berry": "Female",
        "Hailey Bieber": "Female", "Simone Biles": "Female", "Mary J. Blige": "Female",
        "Stella McCartney": "Female", "Georgina Chapman": "Female", "Rachel Brosnahan": "Female",
        "Quinta Brunson": "Female", "Cardi B": "Female", "Sabrina Carpenter": "Female",
        "Emma Chamberlain": "Female", "Charli XCX": "Female", "Julia Carey": "Female",
        "Miley Cyrus": "Female", "Andra Day": "Female", "Lana Del Rey": "Female",
        "Doechii": "Female", "Doja Cat": "Female", "Ayo Edebiri": "Female",
        "Tracee Ellis Ross": "Female", "Cynthia Erivo": "Female", "Whoopi Goldberg": "Female",
        "Gigi Hadid": "Female", "Zuri Hall": "Female", "Laura Harrier": "Female",
        "Anne Hathaway": "Female", "Maya Hawke": "Female", "Lauryn Hill": "Female",
        "Kendall Jenner": "Female", "Kylie Jenner": "Female", "Coco Jones": "Female",
        "Radhika Jones": "Female", "Priyanka Chopra Jonas": "Female", "Nessa Diab": "Female",
        "Mindy Kaling": "Female", "Kim Kardashian": "Female", "Alicia Keys": "Female",
        "Nicole Kidman": "Female", "Regina King": "Female", "Karlie Kloss": "Female",
        "Dua Lipa": "Female", "Lizzo": "Female", "Lorde": "Female",
        "Madonna": "Female", "Audra McDonald": "Female", "Megan Thee Stallion": "Female",
        "Nicki Minaj": "Female", "Janelle Monáe": "Female", "Demi Moore": "Female",
        "Alex Newell": "Non-binary", "Ego Nwodim": "Female", "Keke Palmer": "Female",
        "Natasha Lyonne": "Female", "Gina Alice Redlinger": "Female", "Sofia Richie": "Female",
        "Rihanna": "Female", "Chappell Roan": "Female", "Rosalía": "Female",
        "Diana Ross": "Female", "Zoë Saldaña": "Female", "Anna Sawai": "Female",
        "Nicole Scherzinger": "Female", "Kerry Washington": "Female", "Shakira": "Female",
        "Sadie Sink": "Female", "Sarah Snook": "Female", "Breanna Stewart": "Female",
        "Sydney Sweeney": "Female", "Teyana Taylor": "Female", "Gabrielle Union": "Female",
        "Suki Waterhouse": "Female", "Helen Lasichanh": "Female", "Serena Williams": "Female",
        "Anna Wintour": "Female", "Aimee Lou Wood": "Female", "Zendaya": "Female",
        "Camila Cabello": "Female", "Donatella Versace": "Female", "FKA Twigs": "Female",
        "Willow Smith": "Female", "Taraji P. Henson": "Female", "Elizabeth Debicki": "Female",
        "Jazz Charton": "Female", "Awkwafina": "Female", "Kelsea Ballerini": "Female",
        "Michelle Yeoh": "Female", "Cara Delevingne": "Female", "Rachel Zegler": "Female",
        "Meg Ryan": "Female", "Demi Lovato": "Female", "Phoebe Dynevor": "Female",
        "Naomi Watts": "Female", "Lily Gladstone": "Female", "Queen Latifah": "Female",
        "Karol G": "Female", "Ariana Grande": "Female", "Riley Keough": "Female",
        "Amanda Gorman": "Female", "Jodie Turner-Smith": "Female", "Brie Larson": "Female",
        "Amanda Seyfried": "Female", "Da'Vine Joy Randolph": "Female", "Elle Fanning": "Female",
        "Dove Cameron": "Female", "Penelope Cruz": "Female", "Kylie Minogue": "Female",
        "Emma Wall": "Female", "Kris Jenner": "Female", "Jessica Biel": "Female",
        "Sarah Jessica Parker": "Female", "Greta Lee": "Female", "Uma Thurman": "Female",
        "Ambika Mod": "Female", "Ugbad Abdi": "Female", "Huma Abedin": "Female",
        "Adrienne E. Adams": "Female", "Kiara Advani": "Female", "Adut Akech": "Female",
        "Isha Ambani": "Female", "Valentina Ferrer": "Female", "Angela Bassett": "Female",
        "Elisabetta Beccari": "Female", "Hanna Hultberg": "Female", "Janicza Bravo": "Female",
        "Gale A. Brewer": "Female", "Tory Burch": "Female", "Bee Carrozzini": "Female",
        "Ruth E. Carter": "Female", "Jordan Casteel": "Female", "Jennifer Lopez": "Female",
        "Florence Pugh": "Female", "Jenna Ortega": "Female", "Erykah Badu": "Female",
        "Lily Collins": "Female", "Olivia Rodrigo": "Female", "Salma Hayek": "Female",
        "Jessica Chastain": "Female", "Michaela Coel": "Female", "Irina Shayk": "Female",
        "Kate Moss": "Female", "Margot Robbie": "Female", "Naomi Campbell": "Female",
        "Ice Spice": "Female", "Gisele Bündchen": "Female", "Ariana DeBose": "Female",
        "Anok Yai": "Female", "Philippa Soo": "Female", "Emily Ratajkowski": "Female",
        "Natalie McQueen": "Female", "Phoebe Bridgers": "Female", "Rita Ora": "Female",
        "Penélope Cruz": "Female", "Kate Hudson": "Female", "Emily Blunt": "Female",
        "Lily James": "Female", "Glenn Close": "Female", "Naomi Ackie": "Female",
        "Ashley Park": "Female", "Camila Morrone": "Female", "Priyanka Chopra": "Female",
        "Blake Lively": "Female", "Bella Hadid": "Female", "Kaia Gerber": "Female",
        "Simone Ashley": "Female", "Dakota Johnson": "Female", "Sophie Turner": "Female",
        "Emma Stone": "Female", "Eiza González": "Female", "Carey Mulligan": "Female",
        "Gemma Chan": "Female", "Maude Apatow": "Female", "Hoyeon Jung": "Female",
        "Julianne Moore": "Female", "Chloë Grace Moretz": "Female", "Alexa Chung": "Female",
        "Claire Danes": "Female", "Camila Mendes": "Female", "Vanessa Hudgens": "Female",
        "Nicola Coughlan": "Female", "Miranda Kerr": "Female", "Nicola Peltz Beckham": "Female",
        "Gwen Stefani": "Female", "Daisy Edgar-Jones": "Female", "Amy Schumer": "Female",
        "Tessa Thompson": "Female", "Kacey Musgraves": "Female", "Joan Smalls": "Female",
        "Amber Valletta": "Female", "Winnie Harlow": "Female", "Vanessa Nadal": "Female",
        "Venus Williams": "Female", "Hillary Clinton": "Female", "Paloma Elsesser": "Female",
        "Tommy Dorfman": "Non-binary", "Quannah Chasinghorse": "Female", "Priscilla Presley": "Female",
        "Meredith Winston": "Female", "Wendi Murdoch": "Female", "Allie Michler": "Female",
        "Fabiola Beracasa Beckman": "Female", "Lisa Love": "Female", "Willow Lindley": "Female",
        "Eaddy Kiernan": "Female", "Gina Sanders": "Female", "Elizabeth Schaffer": "Female",
        "Amirah Kassem": "Female", "Adrienne Adams": "Female", "Caroline Wozniacki": "Female",
        "Annie Leibovitz": "Female", "Samuelle Leibovitz": "Female", "Lisa Airan": "Female",
        "Isabelle Boemeke": "Female", "Charlotte Tilbury": "Female", "Chloe Kim": "Female",
        "Renée Elise Goldsberry": "Female", "Renate Reinsve": "Female", "Precious Lee": "Female",
        "Caroline Trentini": "Female", "Shalom Harlow": "Female", "Danai Gurira": "Female",
        "Taylor Hill": "Female", "Madelaine Petsch": "Female", "Kiki Layne": "Female",
        "Normani": "Female", "Sigourney Weaver": "Female", "Chloe Bailey": "Female",
        "Lily Aldridge": "Female", "Jasmine Tookes": "Female", "Addison Rae": "Female",
        "Maisie Williams": "Female", "SZA": "Female", "Rachel Smith": "Female", 
        "Emma Corrin": "Non-binary",
        
        # Groups
        "Stray Kids": "Group"
    }

    # Additional gender dictionary entries for 2021 Met Gala attendees
    additional_gender_entries = {
        # Male celebrities
        "Timothée Chalamet": "Male",
        "Justin Bieber": "Male", 
        "Dan Levy": "Male",
        "Kit Harington": "Male",
        "Finneas": "Male",
        "Adam Mosseri": "Male",
        "Charles Shaffer": "Male",
        "Chance the Rapper": "Male",
        "Zac Posen": "Male",
        "Ben Platt": "Male",
        "Channing Tatum": "Male",
        "Dominic Cooper": "Male",
        "Frank Ocean": "Male",
        "Virgil Abloh": "Male",
        "Taika Waititi": "Male",
        "Aldis Hodge": "Male",
        "Alton Mason": "Male",
        "Maluma": "Male",
        
        # Female celebrities
        "Iman": "Female",
        "Zoë Kravitz": "Female",
        "Jennifer Hudson": "Female",
        "Ciara": "Female",
        "Megan Fox": "Female",
        "Lily-Rose Depp": "Female",
        "Rosé": "Female",
        "Kristen Stewart": "Female",
        "Yara Shahidi": "Female",
        "Lupita Nyong'o": "Female",
        "Grimes": "Female",
        "Hailee Steinfeld": "Female",
        "Ella Emhoff": "Female",
        "Lili Reinhart": "Female",
        "Barbie Ferreira": "Female",
        "Ilana Glazer": "Female",
        "Zoey Deutch": "Female",
        "Saweetie": "Female",
        "Julia Garner": "Female",
        "Rose Leslie": "Female",
        "Madison Beer": "Female",
        "Carolyn B. Maloney": "Female",
        "Eva Chen": "Female",
        "Alicia Quarles": "Female",
        "Monica Mosseri": "Female",
        "Nia Dennis": "Female", 
        "Elizabeth Cordry Shaffer": "Female",
        "Sophia Roe": "Female",
        "Valentina Sampaio": "Female",
        "Storm Reid": "Female",
        "Kirsten Corley": "Female",
        "Debbie Harry": "Female",
        "Kim Petras": "Female",
        "Mj Rodriguez": "Female",
        "Nikkie de Jager": "Female",
        "Lourdes Leon": "Female",
        "Megan Rapinoe": "Female",
        "Chloe Fineman": "Female",
        "Imaan Hammam": "Female",
        "Gillian Anderson": "Female",
        "Jordan Alexander": "Female",
        "Alexandria Ocasio-Cortez": "Female",
        "Aurora James": "Female",
        "Vittoria Ceretti": "Female",
        "Hunter Schafer": "Female",
        "Diane Kruger": "Female",
        "Janet Mock": "Female",
        "Sunisa Lee": "Female",
        "Isabelle Huppert": "Female",
        
        # Non-binary celebrities
        "Elliot Page": "Non-binary"
    }
    
    # Check if celebrity is in the known list
    if name in known_celebrities:
        return known_celebrities[name]
    
    if name in additional_gender_entries:
        return additional_gender_entries[name]
    
    # For names not in the list, we'll make a simple guess based on common naming patterns
    # This is not accurate for all cases and would need to be improved for production use
    if name.split()[-1] in ["Jr.", "Sr.", "III", "IV"]:
        return "Male"
    
    # Default to "Unknown" if we can't determine
    return "Unknown"

def create_met_gala_csv(output_file='met_gala_attendees.csv'):
    """Create a CSV with Met Gala attendees, years, and genders."""

    # Prepare data
    data = []

    # Add 2021 attendees
    for attendee in attendees2021:
        data.append({
            'Name': attendee,
            'Year': 2021,
            'Gender': determine_gender(attendee)
        })

    # Add 2022 attendees
    for attendee in attendees2022:
        data.append({
            'Name': attendee,
            'Year': 2022,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2023 attendees
    for attendee in attendees2023:
        data.append({
            'Name': attendee,
            'Year': 2023,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2024 attendees
    for attendee in attendees2024:
        data.append({
            'Name': attendee,
            'Year': 2024,
            'Gender': determine_gender(attendee)
        })
    
    # Add 2025 attendees
    for attendee in attendees2025:
        data.append({
            'Name': attendee,
            'Year': 2025,
            'Gender': determine_gender(attendee)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print(f"CSV file created successfully: {output_file}")
    print(f"Total entries: {len(data)}")
    print(f"2023 entries: {len(attendees2023)}")
    print(f"2024 entries: {len(attendees2024)}")
    print(f"2025 entries: {len(attendees2025)}")
    
    # Display summary of gender distribution
    gender_counts = df['Gender'].value_counts()
    print("\nGender Distribution:")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")
    
    return df

# Execute the function to create the CSV
if __name__ == "__main__":
    df = create_met_gala_csv()
    
    # Display a sample of the data
    print("\nSample of CSV data:")
    print(df.head(10))
    
    # Display some statistics
    years = df['Year'].unique()
    print("\nYears covered in the dataset:", sorted(years))
    
    # Count unique attendees across all years
    unique_attendees = df['Name'].nunique()
    print(f"\nTotal unique attendees across all years: {unique_attendees}")
    
    # Find attendees who appeared in multiple years
    attendee_counts = df['Name'].value_counts()
    multiple_years = attendee_counts[attendee_counts > 1]
    
    if len(multiple_years) > 0:
        print(f"\nAttendees who appeared in multiple years: {len(multiple_years)}")
        print("Examples of recurring attendees:")
        for name, count in multiple_years.head(10).items():
            years_attended = df[df['Name'] == name]['Year'].tolist()
            print(f"  - {name}: {count} appearances ({', '.join(map(str, sorted(years_attended)))})")