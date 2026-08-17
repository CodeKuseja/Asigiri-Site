from flask import Flask, render_template, request, abort
import sqlite3


app = Flask(__name__)


# ===============================================================#
# ASIGIR HOME PAGE //ANIME DETAILS ON CARD AND AMOUNT PORTRAYED
#  IN THE FRONT 
# ===============================================================#

@app.route("/")
def home():

    search = request.args.get("q", "").strip()

    conn = sqlite3.connect("anime rating.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # If someone searches
    if search:

        search_value = f"%{search}%"

        cursor.execute(
            """
            SELECT name, genre, type, rating, image_url
            FROM "Anime Ratings Table set"

            WHERE (
                   name LIKE ?
                OR genre LIKE ?
                OR type LIKE ?
                OR CAST(rating AS TEXT) LIKE ?
            )

            AND image_url IS NOT NULL
            AND image_url != ''

            ORDER BY rating DESC

            LIMIT 100
            """,
            (
                search_value,
                search_value,
                search_value,
                search_value,
            ),
        )

    # If there is no search
    else:

        cursor.execute(
            """
            SELECT name, genre, type, rating, image_url
            FROM "Anime Ratings Table set"

            WHERE image_url IS NOT NULL
              AND image_url != ''

            ORDER BY rating DESC

            LIMIT 100
            """
        )

    anime = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        anime=anime,
        search=search,
    )


# ==============================================================================================#
# COMMUNITY PAGEI-FUNCTION ALLOWS ANONYMOUSE COMMENTS WITHOUT THE NEED OF PRIVATE INFORMATION   #
# ==============================================================================================#

@app.route("/community", methods=["GET", "POST"])
def community():

    conn = sqlite3.connect("anime rating.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # If someone submits a comment
    if request.method == "POST":

        anime_name = request.form.get(
            "anime_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()

        # Use Anonymous if no name was entered
        if not username:
            username = "Anonymous"

        # Save comment to database
        if anime_name and message:

            cursor.execute(
                """
                INSERT INTO Community_Posts
                (
                    anime_name,
                    username,
                    message
                )

                VALUES (?, ?, ?)
                """,
                (
                    anime_name,
                    username,
                    message,
                ),
            )

            conn.commit()
            conn.close()

            return redirect(
                url_for("community")
            )

    # Get recent community posts
    cursor.execute(
        """
        SELECT
            anime_name,
            username,
            message,
            created_at

        FROM Community_Posts

        ORDER BY created_at DESC

        LIMIT 100
        """
    )

    posts = cursor.fetchall()


    # Get anime names for dropdown
    cursor.execute(
        """
        SELECT DISTINCT name

        FROM "Anime Ratings Table set"

        WHERE name IS NOT NULL

        ORDER BY name

        LIMIT 500
        """
    )

    anime_names = cursor.fetchall()

    conn.close()

    return render_template(
        "community.html",
        posts=posts,
        anime_names=anime_names,
    )


# ===================================================================================================#
#    ANIME LEADERBOARD / RANKINGS OF ANIME AND TOTAL RATING,MEMBERS,GENRE AND DETAILS(AMOUNT 50)   #
# ===================================================================================================#

@app.route("/anime")
def anime_page():

    conn = sqlite3.connect("anime rating.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            name,
            genre,
            rating,
            members,
            image_url

        FROM "Anime Ratings Table set"

        WHERE rating IS NOT NULL
          AND members IS NOT NULL
          AND members >= 1000

        ORDER BY
            rating DESC,
            members DESC

        LIMIT 50
        """
    )

    leaderboard = cursor.fetchall()

    conn.close()

    return render_template(
        "anime.html",
        leaderboard=leaderboard,
    )



# HELP PAGE


@app.route("/content")
def content():

    return render_template(
        "content.html"
    )

#=============================================================================================#
#ERROR HANLDERS- COSTUM 404 PAGE AND 505 ERROR HANDLERS FOR HTTP ERRORS#
#=============================================================================================#
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html"), 404

@app.errorhandler(505)
def http_version_not_supported(error):
    return render_template("error505.html"), 505

# START WEBSITE

if __name__ == "__main__":

    app.run(debug=True)