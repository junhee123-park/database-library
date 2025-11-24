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
        raise ValueError("category는 초성/중성/종성/숫자만 가능")

    table_name, col = table_map[category]
    cur.execute(f"SELECT dot_pattern FROM {table_name} WHERE {col}=?", (char,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    dot_pattern = row[0].strip()

    # 셀 분리
    cells = dot_pattern.split()

    # prefix (1셀 전용)
    prefix_map = {"초성":"1", "중성":"2", "종성":"3", "숫자":"4"}
    prefix = prefix_map[category]

    # --- 1셀 (12자리) ---
    if len(cells) == 1:
        cell = cells[0]
        result = ""
        for bit in cell:
            if bit == "0":
                result += prefix + "0"
            else:
                result += prefix + "1"
        return result

    # --- 2셀 (24자리) ---
    elif len(cells) == 2:
        cell1, cell2 = cells
        result = ""

        # 첫 번째 셀: 1x
        for bit in cell1:
            result += "11" if bit == "1" else "10"

        # 두 번째 셀: 2x
        for bit in cell2:
            result += "21" if bit == "1" else "20"

        return result

    else:
        raise ValueError("점자 모듈이 1개 또는 2개여야 합니다.")



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

def get_symbol_list(category, db_path='braille.db'):
    """초성, 중성, 종성, 숫자 리스트를 DB에서 불러오기"""
    table_map = {
        "초성": ("braille_initial", "consonant"),
        "중성": ("braille_medial", "vowel"),
        "종성": ("braille_final", "consonant"),
        "숫자": ("braille_number", "number")
    }

    if category not in table_map:
        raise ValueError("❌ category는 '초성', '중성', '종성', '숫자' 중 하나여야 합니다.")

    table, col = table_map[category]
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {col} FROM {table}")
        result = [row[0] for row in cur.fetchall()]
    return result
