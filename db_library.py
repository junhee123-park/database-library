
#이게 문자열 101010101010 형태로 나오는 함수
import sqlite3

def get_braille(category, char):
conn = sqlite3.connect('braille.db')
cur = conn.cursor()

table_map = {
    "초성": ("braille_initial", "consonant"),
    "중성": ("braille_medial", "vowel"),
    "종성": ("braille_final", "consonant"),
    "숫자": ("braille_number", "number")
}

if category not in table_map:
    conn.close()
    raise ValueError("❌ category는 '초성', '중성', '종성', '숫자' 중 하나여야 합니다.")

table_name, col_name = table_map[category]
cur.execute(f"SELECT dot_pattern FROM {table_name} WHERE {col_name}=?", (char,))
result = cur.fetchone()
conn.close()

if not result:
    return None

dot_pattern = result[0].strip()

# --- 숫자일 경우 (모듈 2개, 12자리 문자열) ---
if category == "숫자":
    patterns = dot_pattern.split()  # ['010111', '100000']
    if len(patterns) != 2:
        raise ValueError("❌ 숫자 패턴은 두 개의 6점 패턴으로 구성되어야 합니다.")
    result_str = ""
    # 첫 번째 모듈 (1)
    for bit in patterns[0].ljust(6, "0"):
        result_str += "1" + bit
    # 두 번째 모듈 (2)
    for bit in patterns[1].ljust(6, "0"):
        result_str += "2" + bit
    return result_str  # 예: "101011101111210000100000"

# --- 초성/중성/종성 (6점 패턴) ---
prefix = {"초성": "1", "중성": "2", "종성": "3"}[category]
dot_pattern = dot_pattern.ljust(6, "0")[:6]

result_str = ""
for bit in dot_pattern:
    result_str += prefix + bit

return result_str

def add_correct_word(word, db_path='braille.db'):
    """맞힌 단어(음절)를 correct_words 테이블에 추가"""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO correct_words (word) VALUES (?)", (word,))
        conn.commit()

def add_wrong_word(word, db_path='braille.db'):
    """틀린 단어(음절)를 wrong_words 테이블에 추가"""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO wrong_words (word) VALUES (?)", (word,))
        conn.commit()
def get_correct_words(db_path='braille.db', limit=None):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        query = "SELECT word, timestamp FROM correct_words ORDER BY id DESC"
        if limit:
            query += f" LIMIT {limit}"
        cur.execute(query)
        return cur.fetchall()  # [(word, timestamp), (word, timestamp), ...]


def get_wrong_words(db_path='braille.db', limit=None):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        query = "SELECT word, timestamp FROM wrong_words ORDER BY id DESC"
        if limit:
            query += f" LIMIT {limit}"
        cur.execute(query)
        return cur.fetchall()
#사용예시:
#print(get_braille("초성","ㄱ"))
# 사용자가 '한'이라는 단어를 맞힘
#add_correct_word('한')

# 사용자가 '가'를 틀림
#add_wrong_word('가')
