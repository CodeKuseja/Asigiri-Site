import sqlite3
import time

import requests

DATABASE = "anime rating.db"
ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($search: String) {
    Media(search: $search, type: ANIME) {
        title {
            romaji
            english
        }
        coverImage {
            large
        }
    }
}
"""


def find_cover(title: str) -> str | None:
    """Return an AniList cover URL for one anime title."""

    try:
        response = requests.post(
            ANILIST_URL,
            json={
                "query": QUERY,
                "variables": {"search": title},
            },
            timeout=15,
        )
        response.raise_for_status()

        media = response.json().get("data", {}).get("Media")

        if not media:
            return None

        return media.get("coverImage", {}).get("large")

    except (requests.RequestException, ValueError) as error:
        print(f"API error for {title}: {error}")
        return None


def update_covers(limit: int = 20) -> None:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT rowid, name
        FROM "Anime Ratings Table set"
        WHERE image_url IS NULL
           OR image_url = ''
        LIMIT ?
        """,
        (limit,),
    )

    anime_rows = cursor.fetchall()

    for number, anime in enumerate(anime_rows, start=1):
        title = anime["name"]
        print(f"{number}/{len(anime_rows)}: Searching for {title}")

        cover_url = find_cover(title)

        if cover_url:
            cursor.execute(
                """
                UPDATE "Anime Ratings Table set"
                SET image_url = ?
                WHERE rowid = ?
                """,
                (cover_url, anime["rowid"]),
            )

            connection.commit()
            print("Cover saved.")
        else:
            print("No matching cover found.")

        # Avoid sending requests too rapidly.
        time.sleep(1)

    connection.close()
    print("Finished updating covers.")


if __name__ == "__main__":
    update_covers(limit=20)