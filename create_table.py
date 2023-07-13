user_tabe = """
CREATE table if not exists user_info (
    date TIMESTAMP default CURRENT_TIMESTAMP,
    user_id INTEGER,
    username VARCHAR(50),
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    message VARCHAR(100)
);

CREATE table if not exists user_url (
    date TIMESTAMP default CURRENT_TIMESTAMP,
    user_id INTEGER,
    url VARCHAR(100),
    parsed bool
);

CREATE table if not exists url_words (
    date TIMESTAMP default CURRENT_TIMESTAMP,
    user_id INTEGER,
    url VARCHAR(100),
    word VARCHAR(100)
);
CREATE table if not exists words_trsl (
    word VARCHAR(100),
    trsl VARCHAR(100)
);
"""