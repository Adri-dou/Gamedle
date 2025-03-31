import pandas as pd
import ast

# Read CSV files
details_df = pd.read_csv('detail.csv', sep=',', on_bad_lines='skip')
rating_df = pd.read_csv('rating.csv', sep=',', on_bad_lines='skip')

# Merge datasets on game ID
merged_df = pd.merge(details_df, rating_df, on='id', suffixes=('', '_y'))

# Initialize data structures to track entries
publishers = {}
publisher_id = 1
contributions = {'Design', 'Art'}  # Predefined sectors for Contribution
categories = set()
mechanics = set()
creators = {}
creator_id = 1

# SQL statements lists
insertions = {
    'contribution': [],
    'publisher': [],
    'category': [],
    'mechanic': [],
    'creator': [],
    'game': [],
    'is_categorised_as': [],
    'has_mechanics': [],
    'created': []
}

# Add Contribution entries
for sector in contributions:
    insertions['contribution'].append(f"INSERT INTO Contribution (sector) VALUES ('{sector}');")

# Process each game row
for _, row in merged_df.iterrows():
    game_id = row['id']
    
    # --- Publishers ---
    pub_names = ast.literal_eval(row['boardgamepublisher'])
    if pub_names:
        pub_name = pub_names[0].replace("'", "''")
        if pub_name not in publishers:
            publishers[pub_name] = publisher_id
            insertions['publisher'].append(
                f"INSERT INTO Publisher (publisher_id, name) VALUES ({publisher_id}, '{pub_name}');"
            )
            publisher_id += 1
        game_pub_id = publishers[pub_name]
    else:
        game_pub_id = 'NULL'  # Handle missing publisher
    
    # --- Creators (Designers & Artists) ---
    designers = ast.literal_eval(row['boardgamedesigner'])
    artists = ast.literal_eval(row['boardgameartist'])
    for name in designers + artists:
        # Split name into firstname and surname
        parts = name.replace("'", "''").split(' ', 1)
        first = parts[0] if len(parts) > 0 else ''
        last = parts[1] if len(parts) > 1 else ''
        sector = 'Design' if name in designers else 'Art'
        
        # Add creator if new
        key = (first, last, sector)
        if key not in creators:
            creators[key] = creator_id
            insertions['creator'].append(
                f"INSERT INTO Creator (creator_id, firstname, surname, sector) "
                f"VALUES ({creator_id}, '{first}', '{last}', '{sector}');"
            )
            creator_id += 1
        # Link to created table
        insertions['created'].append(
            f"INSERT INTO created (game_id, creator_id) VALUES ({game_id}, {creators[key]});"
        )
    
    # --- Categories ---
    for category in ast.literal_eval(row['boardgamecategory']):
        category = category.replace("'", "''")
        if category not in categories:
            categories.add(category)
            insertions['category'].append(f"INSERT INTO Category (category_name) VALUES ('{category}');")
        insertions['is_categorised_as'].append(
            f"INSERT INTO is_categorised_as (game_id, category_name) VALUES ({game_id}, '{category}');"
        )
    
    # --- Mechanics ---
    for mechanic in ast.literal_eval(row['boardgamemechanic']):
        mechanic = mechanic.replace("'", "''")
        if mechanic not in mechanics:
            mechanics.add(mechanic)
            insertions['mechanic'].append(f"INSERT INTO Mechanic (mechanic_type) VALUES ('{mechanic}');")
        insertions['has_mechanics'].append(
            f"INSERT INTO has_mechanics (game_id, mechanic_type) VALUES ({game_id}, '{mechanic}');"
        )
    
    # --- Game ---
    year = f"{row['yearpublished']}-01-01"
    time = f"{row['playingtime'] // 60:02}:{row['playingtime'] % 60:02}:00"
    name = row['name'].replace("'", "''")
    desc = row['description'].replace("'", "''") if pd.notna(row['description']) else ''
    insertions['game'].append(
        f"INSERT INTO Game (game_id, minAge, minPlayer, ranking, maxPlayer, yearPublished, name, description, playingTime, publisher_id) "
        f"VALUES ({game_id}, {row['minage']}, {row['minplayers']}, {row['rank']}, {row['maxplayers']}, "
        f"'{year}', '{name}', '{desc}', '{time}', {game_pub_id});"
    )

# Write all SQL statements in correct order
with open('insertion-file.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(insertions['contribution']) + '\n')
    f.write('\n'.join(insertions['publisher']) + '\n')
    f.write('\n'.join(insertions['category']) + '\n')
    f.write('\n'.join(insertions['mechanic']) + '\n')
    f.write('\n'.join(insertions['creator']) + '\n')
    f.write('\n'.join(insertions['game']) + '\n')
    f.write('\n'.join(insertions['is_categorised_as']) + '\n')
    f.write('\n'.join(insertions['has_mechanics']) + '\n')
    f.write('\n'.join(insertions['created']) + '\n')