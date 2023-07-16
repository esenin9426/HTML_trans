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

CREATE ROLE parser_user LOGIN PASSWORD 'parser_user';
CREATE ROLE translator LOGIN PASSWORD 'translator';

GRANT ALL on public.user_url TO parser_user
GRANT ALL on public.url_words TO parser_user
GRANT select  on public.url_words TO translator
GRANT ALL on public.words_trsl TO translator

"""