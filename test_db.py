from database import get_connection, get_all_words

try:
    connection = get_connection()
    print("MySQL connected successfully!")

    connection.close()

    words = get_all_words()
    print("Total words in database:", len(words))
    print("Words:", words[:10])

except Exception as e:
    print("Error:", e)