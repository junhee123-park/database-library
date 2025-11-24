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
def get_correct_words(limit=None, db_path='braille.db'):
    """correct_words에서 단어 목록만 가져오기 (시간 제거, limit은 위치 인자 가능)"""

    # limit이 숫자로 들어온 경우 (예: get_correct_words(3))
    # 또는 limit=3 처럼 들어온 경우도 처리
    if isinstance(limit, str) and limit.isdigit():
        limit = int(limit)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        query = "SELECT word FROM correct_words ORDER BY id DESC"

        if isinstance(limit, int):
            query += f" LIMIT {limit}"

        cur.execute(query)
        rows = cur.fetchall()  # [(word,), (word,), ...]

        return [row[0] for row in rows]

def get_wrong_words(limit=None, db_path='braille.db'):
    """wrong_words에서 단어 목록만 가져오기 (시간 제거, limit은 위치 인자 가능)"""

    # limit이 "3"처럼 문자열로 들어오면 숫자로 변환
    if isinstance(limit, str) and limit.isdigit():
        limit = int(limit)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        query = "SELECT word FROM wrong_words ORDER BY id DESC"

        # limit이 숫자로 주어진 경우에만 LIMIT 추가
        if isinstance(limit, int):
            query += f" LIMIT {limit}"

        cur.execute(query)
        rows = cur.fetchall()  # [(word,), (word,), ...]

        return [row[0] for row in rows]


def reset_correct_words():
    conn = sqlite3.connect("braille.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM correct_words")
    conn.commit()
    conn.close()
    print("✅ correct_words 테이블이 초기화되었습니다.")
def reset_wrong_words():
    conn = sqlite3.connect("braille.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM wrong_words")
    conn.commit()
    conn.close()
    print("❗ wrong_words 테이블이 초기화되었습니다.")
