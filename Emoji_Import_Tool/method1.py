from mysql import connector
#pip install mysql-connector-python
from local_config import db_config
from emoji_data import UnicodeEmojiData
from emojipedia import Emojipedia
from emojipedia import emoji

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

with open('Output/method1_insert_emoji.sql', 'w', encoding='utf-8') as db_file:
    # ------- EMOJI VERSIONS -------

    print("Gathering Unicode Versions")

    emoji_version_list = []
    num_versions = len(UnicodeEmojiData.EMOJI_VERSIONS)
    emoji_version_index = 1

    for i in range(0, num_versions):
        version, name = UnicodeEmojiData.EMOJI_VERSIONS[i]
        version_url_ext = name.replace(' ', '-').lower()
        cur_dict = {'id': emoji_version_index,
                    'version': version,
                    'name': name,
                    'url': version_url_ext}
        emoji_version_list.append(cur_dict)
        emoji_version_index += 1

    # ------- SCRAPE EMOJI -------

    print("Scraping Emoji by Unicode Versions")

    emoji_per_version = []

    # This loop scrapes emoji through by way of unicode versions. It passes a unicode version (e.g., unicode-1.1) to
    # Emojipedia's _get_page method which then scrapes emojipedia.org and parses through the html to find emoji.
    #
    # For an example of the data that is scraped: https://emojipedia.org/unicode-1.1/
    for emoji_version in emoji_version_list:

        soup = Emojipedia._get_page(emoji_version["url"])
        emoji_found = []

        emoji_lists = soup.find('div', {'class': 'content'}).find_all('ul')
        for emoji_list in emoji_lists:
            for emoji_entry in emoji_list.find_all('li'):
                if emoji_entry.find('span', {'class': 'emoji'}):
                    emoji_link = emoji_entry.find('a')
                    emoji_text = emoji_link.text.split(' ')

                    e = emoji.Emoji(url=emoji_link['href'])
                    e._character, e._title = emoji_text[0], ' '.join(emoji_text[1:])
                    emoji_found.append(e)

        emoji_per_version.append((emoji_version["id"], emoji_found))

    # ------- PERSIST EMOJI & UNICODE -------

    print("Persisting Emoji by Unicode Versions")
    emoji_id = 1
    for current_emoji_list in emoji_per_version:
        print(f"Processing Emoji from Version: {current_emoji_list[0]}")
        for current_emoji in current_emoji_list[1]:
            # not everything kicked back is actually an emoji, double checking
            try:
                image_url = current_emoji.platforms[0].image_url
                cur_emoji_unicode = []
                for unicode in current_emoji.codepoints:
                    cur_emoji_unicode.append(unicode)
                if len(cur_emoji_unicode) == 0:
                    continue
            except Exception:
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

        # Commit and move on to the next set of emoji
        db_conn.commit()
        print(f"Cumulative Processed After Version {current_emoji_list[0]}: {emoji_id}")

print('Closing The Connection')
db_conn.close()
