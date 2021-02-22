from mysql import connector
#pip install mysql-connector-python
from local_config import db_config
from emojipedia import Emojipedia

# ------- DATABASE SETUP -------

print('Initializing Database Connection')

db_conn = connector.connect(
    user=db_config['user'],
    host=db_config['host'],
    password=db_config['password'],
    database=db_config['database'],
    use_unicode=True,
    charset="utf8mb4"
)

cursor = db_conn.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

with open('Output/method2_insert_emoji.sql', 'w', encoding='utf-8') as db_file:

    # ------- SCRAPE EMOJI -------

    print("Scraping Emoji by Emojipedia.all()")
    scraped_emoji = Emojipedia.all()

    emoji_id = 1

    # ------- PERSIST EMOJI & UNICODE -------
    print("Persisting Emoji")
    for current_emoji in scraped_emoji:
        # not everything kicked back is actually an emoji, double checking
        try:
            image_url = current_emoji.platforms[0].image_url
            cur_emoji_unicode = []
            for unicode in current_emoji.codepoints:
                cur_emoji_unicode.append(unicode)
            if len(cur_emoji_unicode) == 0:
                continue
        except:
            continue

        # Emoji Persistence
        emoji_dict = {
            'id': emoji_id,
            'name': current_emoji.title,
            'url': image_url,
            'emoji': current_emoji.character
        }

        insert_emoji_query = ("INSERT INTO emoji "
                              "(emoji_id, name, image_url, emoji) "
                              "VALUES (%(id)s, %(name)s, %(url)s, %(emoji)s);")

        cursor.execute(insert_emoji_query, emoji_dict)
        print(cursor.statement, file=db_file)

        # Unicode Persistence
        for unicode in cur_emoji_unicode:
            unicode_dict = {
                'unicode': unicode,
                'emoji_id': emoji_id
            }
            insert_emoji_unicode_query = ("INSERT INTO emoji_unicode "
                                          "(unicode, emoji_id) "
                                          "VALUES (%(unicode)s, %(emoji_id)s);")

            cursor.execute(insert_emoji_unicode_query, unicode_dict)
            print(cursor.statement, file=db_file)

        emoji_id += 1

    db_conn.commit()

print('Closing The Connection')
db_conn.close()
