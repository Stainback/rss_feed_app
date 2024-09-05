import os.path

TIMER_REFRESH = 60      # in seconds

DB = "app_db.sqlite"

FONT = "UbuntuMono-Regular.ttf"
FONT_FAMILY = "Ubuntu Mono"
FONT_SIZE = 16

STYLES = "styles.css"

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, "db", DB)
FONT_PATH = os.path.join(ROOT, "fonts", FONT)
STYLES_PATH = os.path.join(ROOT, "css", STYLES)

TIMEZONE = "UTC"
