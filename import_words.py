
from wordfreq import top_n_list
from database import get_connection

TARGET_WORDS = 50000
BATCH_SIZE = 1000
BACKUP_TABLE = "words_backup_20261014"


def main():
    print("Preparing common English vocabulary...")

    source_words = top_n_list("en", TARGET_WORDS * 2)

    words = []
    seen = set()

    for item in source_words:
        word = item.strip().lower()

        if not word.isascii() or not word.isalpha():
            continue
        if not 3 <= len(word) <= 25:
            continue
        if word in seen:
            continue

        seen.add(word)
        words.append(word)

        if len(words) >= TARGET_WORDS:
            break

    if len(words) < 10000:
        raise RuntimeError(
            "Not enough words were generated. Existing database unchanged."
        )

    print(f"Prepared {len(words)} ranked words.")
    print("Sample:", words[:30])

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {BACKUP_TABLE} AS "
            "SELECT * FROM words"
        )
        connection.commit()

        cursor.execute("DELETE FROM words")

        for start in range(0, len(words), BATCH_SIZE):
            batch = words[start:start + BATCH_SIZE]

            cursor.executemany(
                "INSERT IGNORE INTO words (word) VALUES (%s)",
                [(word,) for word in batch]
            )

            print(f"Imported through {min(start + BATCH_SIZE, len(words))}")

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM words")
        print("Total words in MySQL:", cursor.fetchone()[0])

        cursor.execute(
            "SELECT word FROM words ORDER BY id ASC LIMIT 30"
        )
        print("First 30 words:", [row[0] for row in cursor.fetchall()])

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
