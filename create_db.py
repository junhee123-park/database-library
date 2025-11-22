import sqlite3

conn = sqlite3.connect('braille.db')
cur = conn.cursor()

# 1️⃣ 초성 테이블
cur.execute("""
CREATE TABLE IF NOT EXISTS braille_initial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consonant TEXT,
    dot_pattern TEXT,
    description TEXT
)
""")

initials = [
    ('ㄱ', '010000', '초성 ㄱ'),
    ('ㄴ', '110000', '초성 ㄴ'),
    ('ㄷ', '011000', '초성 ㄷ'),
    ('ㄹ', '000100', '초성 ㄹ'),
    ('ㅁ', '100100', '초성 ㅁ'),
    ('ㅂ', '010100', '초성 ㅂ'),
    ('ㅅ', '000001', '초성 ㅅ'),
    ('ㅇ', '000000', '초성 ㅇ'),  # 초성에는 점자가 없음
    ('ㅈ', '010001', '초성 ㅈ'),
    ('ㅊ', '000101', '초성 ㅊ'),
    ('ㅋ', '111000', '초성 ㅋ'),
    ('ㅌ', '101100', '초성 ㅌ'),
    ('ㅍ', '110100', '초성 ㅍ'),
    ('ㅎ', '011100', '초성 ㅎ'),
    ('ㄲ', '000001 010000', '초성 ㄲ'),
    ('ㄸ', '000001 011000', '초성 ㄸ'),
    ('ㅃ', '000001 010100', '초성 ㅃ'),
    ('ㅆ', '000001 000001', '초성 ㅆ'),
    ('ㅉ', '000001 010001', '초성 ㅉ')
    
]
cur.executemany("INSERT INTO braille_initial (consonant, dot_pattern, description) VALUES (?, ?, ?)", initials)

# 2️⃣ 중성 테이블
cur.execute("""
CREATE TABLE IF NOT EXISTS braille_medial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vowel TEXT,
    dot_pattern TEXT,
    description TEXT
)
""")

medials = [
    ('ㅏ', '101001', '모음 ㅏ'),
    ('ㅑ', '010110', '모음 ㅑ'),
    ('ㅓ', '011010', '모음 ㅓ'),
    ('ㅕ', '100101', '모음 ㅕ'),
    ('ㅗ', '100011', '모음 ㅗ'),
    ('ㅛ', '010011', '모음 ㅛ'),
    ('ㅜ', '110010', '모음 ㅜ'),
    ('ㅠ', '110001', '모음 ㅠ'),
    ('ㅡ', '011001', '모음 ㅡ'),
    ('ㅣ', '100110', '모음 ㅣ'),
    ('ㅐ', '101110', '모음 ㅐ'),
    ('ㅔ', '110110', '모음 ㅔ'),
    ('ㅖ', '010010', '모음 ㅖ'),
    ('ㅘ', '101011', '모음 ㅘ'),
    ('ㅚ', '110111', '모음 ㅚ'),
    ('ㅝ', '111010', '모음 ㅝ'),
    ('ㅢ', '011101', '모음 ㅢ'),
    ('ㅒ', '010110 101110','모음 ㅒ')
    ('ㅙ', '101011 101110','모음 ㅙ')
    ('ㅞ', '111010 101110','모음 ㅞ')
    ('ㅟ', '110010 101110','모음 ㅟ')
]
cur.executemany("INSERT INTO braille_medial (vowel, dot_pattern, description) VALUES (?, ?, ?)", medials)

# 3️⃣ 종성 테이블
cur.execute("""
CREATE TABLE IF NOT EXISTS braille_final (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consonant TEXT,
    dot_pattern TEXT,
    description TEXT
)
""")

finals = [
    ('ㄱ', '100000', '종성 ㄱ'),
    ('ㄴ', '001100', '종성 ㄴ'),
    ('ㄷ', '000110', '종성 ㄷ'),
    ('ㄹ', '001000', '종성 ㄹ'),
    ('ㅁ', '001001', '종성 ㅁ'),
    ('ㅂ', '101000', '종성 ㅂ'),
    ('ㅅ', '000010', '종성 ㅅ'),
    ('ㅇ', '001111', '종성 ㅇ'),
    ('ㅈ', '100010', '종성 ㅈ'),
    ('ㅊ', '001010', '종성 ㅊ'),
    ('ㅋ', '001110', '종성 ㅋ'),
    ('ㅌ', '001011', '종성 ㅌ'),
    ('ㅍ', '001101', '종성 ㅍ'),
    ('ㅎ', '000111', '종성 ㅎ'),
    ('ㄲ',  '100000 100000', '종성 ㄲ'),
    ('ㅆ',  '010010', '종성 ㅆ'),
    ('ㄳ',  '100000 000010', '종성ㄳ '),
    ('ㄵ',  '001100 100010', '종성 ㄵ'),
    ('ㄶ',  '001100 000111', '종성 ㄶ'),
    ('ㄺ',  '001000 100000', '종성 ㄺ'),
    ('ㄻ',  '001000 001001', '종성 ㄻ'),
    ('ㄼ',  '001000 101000', '종성 ㄼ'),
    ('ㄽ',  '001000 000010', '종성 ㄽ'),
    ('ㄾ',  '001000 001011', '종성 ㄾ'),
    ('ㄿ',  '001000 001101', '종성 ㄿ'),
    ('ㅀ',  '001000 000111', '종성 ㅀ'),
    ('ㅄ',  '101000 000010', '종성 ㅄ')
]
cur.executemany("INSERT INTO braille_final (consonant, dot_pattern, description) VALUES (?, ?, ?)", finals)

# 4️⃣ 숫자 테이블
cur.execute("""
CREATE TABLE IF NOT EXISTS braille_number (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    dot_pattern TEXT,
    description TEXT
)
""")

numbers = [
    ('1', '010111 100000', '숫자 1'),
    ('2', '010111 101000', '숫자 2'),
    ('3', '010111 110000', '숫자 3'),
    ('4', '010111 110100', '숫자 4'),
    ('5', '010111 100100', '숫자 5'),
    ('6', '010111 111000', '숫자 6'),
    ('7', '010111 111100', '숫자 7'),
    ('8', '010111 101100', '숫자 8'),
    ('9', '010111 011000', '숫자 9'),
    ('0', '010111 011100', '숫자 0')
]
cur.executemany("INSERT INTO braille_number (number, dot_pattern, description) VALUES (?, ?, ?)", numbers)

conn.commit()
conn.close()
print("✅ braille.db 생성 완료 — 초성, 중성, 종성, 숫자 테이블 포함!")

conn = sqlite3.connect('braille.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS correct_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS wrong_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("✅ braille.db에 correct_words, wrong_words 테이블이 추가되었습니다.")
