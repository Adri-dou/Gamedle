import pandas as pd
import ast

def safe_literal_eval(data):
    """Safely evaluate string containing lists or return as list"""
    if pd.isna(data):
        return []
    if isinstance(data, list):
        return data
    try:
        if data.startswith('[') and data.endswith(']'):
            return ast.literal_eval(data)
        elif ',' in data:
            return [x.strip() for x in data.split(',')]
        return [data.strip()]
    except (ValueError, SyntaxError, AttributeError):
        return []

def clean_text(text):
    """Clean text for SQL insertion"""
    if pd.isna(text):
        return None
    return str(text).replace("'", "''").strip()

# Read CSV files
details_df = pd.read_csv('details.csv', sep=',', on_bad_lines='skip')
rating_df = pd.read_csv('ratings.csv', sep=',', on_bad_lines='skip')

# Merge datasets on game ID
merged_df = pd.merge(details_df, rating_df, on='id', suffixes=('', '_y'))

# Initialize data structures
publishers = {}
publisher_id = 1
contributions = {'Design', 'Art'}
categories = set()
mechanics = set()
creators = {}
creator_id = 1
created_pairs = set()

# SQL statements
insertions = {
    'contribution': ["INSERT INTO Contribution (sector) VALUES ('Design');",
                    "INSERT INTO Contribution (sector) VALUES ('Art');"],
    'publisher': [],
    'category': [],
    'mechanic': [],
    'creator': [],
    'game': [],
    'is_categorised_as': [],
    'has_mechanics': [],
    'created': []
}

# Process each game row
for _, row in merged_df.iterrows():
    game_id = row['id']
    
    # --- Publishers ---
    pub_names = safe_literal_eval(row.get('boardgamepublisher'))
    if pub_names:
        pub_name = clean_text(pub_names[0])
        if pub_name and pub_name not in publishers:
            publishers[pub_name] = publisher_id
            insertions['publisher'].append(
                f"INSERT INTO Publisher (publisher_id, name) VALUES ({publisher_id}, '{pub_name}');"
            )
            publisher_id += 1
        game_pub_id = publishers.get(pub_name, 'NULL')
    else:
        game_pub_id = 'NULL'
    
    # --- Creators ---
    designers = safe_literal_eval(row.get('boardgamedesigner'))
    artists = safe_literal_eval(row.get('boardgameartist'))
    
    for name in designers + artists:
        name = clean_text(name)
        if not name:
            continue
            
        parts = name.split(' ', 1)
        first = parts[0] if len(parts) > 0 else ''
        last = parts[1] if len(parts) > 1 else ''
        sector = 'Design' if name in designers else 'Art'
        
        key = (first, last, sector)
        if key not in creators:
            creators[key] = creator_id
            insertions['creator'].append(
                f"INSERT INTO Creator (creator_id, firstname, surname, sector) "
                f"VALUES ({creator_id}, '{first}', '{last}', '{sector}');"
            )
            creator_id += 1
        
        # Avoiding duplication in table created
        pair = (game_id, creators[key])
        if pair not in created_pairs:
            created_pairs.add(pair)
            insertions['created'].append(
                f"INSERT INTO created (game_id, creator_id) VALUES ({game_id}, {creators[key]});"
            )

    # --- Categories ---
    categories_list = safe_literal_eval(row.get('boardgamecategory'))
    for category in categories_list:
        category = clean_text(category)
        if not category:
            continue
            
        if category not in categories:
            categories.add(category)
            insertions['category'].append(
                f"INSERT INTO Category (category_name) VALUES ('{category}');"
            )
        
        insertions['is_categorised_as'].append(
            f"INSERT INTO is_categorised_as (game_id, category_name) VALUES ({game_id}, '{category}');"
        )
    
    # --- Mechanics ---
    mechanics_list = safe_literal_eval(row.get('boardgamemechanic'))
    for mechanic in mechanics_list:
        mechanic = clean_text(mechanic)
        if not mechanic:
            continue
            
        if mechanic not in mechanics:
            mechanics.add(mechanic)
            insertions['mechanic'].append(
                f"INSERT INTO Mechanic (mechanic_type) VALUES ('{mechanic}');"
            )
        
        insertions['has_mechanics'].append(
            f"INSERT INTO has_mechanics (game_id, mechanic_type) VALUES ({game_id}, '{mechanic}');"
        )
    
    # --- Game ---
    name = clean_text(row.get('name', 'Unknown'))
    desc = clean_text(row.get('description', ''))
    
    # Handle numeric values with defaults
    min_age = int(row['minage']) if pd.notna(row.get('minage')) else 0
    min_players = int(row['minplayers']) if pd.notna(row.get('minplayers')) else 1
    max_players = int(row['maxplayers']) if pd.notna(row.get('maxplayers')) else min_players
    playing_time = int(row['playingtime']) if pd.notna(row.get('playingtime')) else 30
    ranking = int(row['rank']) if pd.notna(row.get('rank')) else 9999
    
    # Handle year and time formatting
    year = row['yearpublished']
    year_sql = 'NULL' if pd.notna(year) and int(year) < 0 else f"'{int(year)}-01-01'"
    time_sql = f"'{playing_time // 60:02d}:{playing_time % 60:02d}:00'"
    
    insertions['game'].append(
        f"INSERT INTO Game (game_id, minAge, minPlayer, ranking, maxPlayer, yearPublished, name, description, playingTime, publisher_id) "
        f"VALUES ({game_id}, {min_age}, {min_players}, {ranking}, {max_players}, {year_sql}, '{name}', '{desc}', {time_sql}, {game_pub_id});"
    )

# Write SQL file with proper order
with open('insertion-file.sql', 'w', encoding='utf-8') as f:
    # Write headers
    f.write("-- SQL INSERTIONS FOR GAMEDLE DATABASE\n")
    f.write(f"-- Generated from {len(merged_df)} games\n\n")
    
    # Write tables in correct dependency order
    f.write("-- CONTRIBUTION TYPES\n")
    f.write('\n'.join(insertions['contribution']) + '\n\n')
    
    f.write("-- PUBLISHERS\n")
    f.write('\n'.join(insertions['publisher']) + '\n\n')
    
    f.write("-- CATEGORIES\n")
    f.write('\n'.join(insertions['category']) + '\n\n')
    
    f.write("-- MECHANICS\n")
    f.write('\n'.join(insertions['mechanic']) + '\n\n')
    
    f.write("-- CREATORS\n")
    f.write('\n'.join(insertions['creator']) + '\n\n')
    
    f.write("-- GAMES\n")
    f.write('\n'.join(insertions['game']) + '\n\n')
    
    f.write("-- GAME CATEGORIES\n")
    f.write('\n'.join(insertions['is_categorised_as']) + '\n\n')
    
    f.write("-- GAME MECHANICS\n")
    f.write('\n'.join(insertions['has_mechanics']) + '\n\n')
    
    f.write("-- CREATOR CONTRIBUTIONS\n")
    f.write('\n'.join(insertions['created']) + '\n\n')
    
    f.write("-- END OF FILE\n")

# Print summary
print(f"GENERATION COMPLETE\n"
      f"Games processed: {len(merged_df)}\n"
      f"Publishers: {len(publishers)}\n"
      f"Categories: {len(categories)}\n"
      f"Mechanics: {len(mechanics)}\n"
      f"Creators: {len(creators)}\n"
      f"Game entries: {len(insertions['game'])}\n"
      f"Category assignments: {len(insertions['is_categorised_as'])}\n"
      f"Mechanic assignments: {len(insertions['has_mechanics'])}\n"
      f"Creator credits: {len(insertions['created'])}")