################################################################################
# Adds new fulltext articles to DB
# Matches articles to those that exist with metadata already in DB
################################################################################

import boston_globe,DB_manager

db = connectToCouch
latestArticles = boston_globe.fetch_latest_fulltext_from_FTP(db)
db.save_all_full_text(latestArticles)