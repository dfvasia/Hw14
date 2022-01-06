# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
from functions import open_sqlite3 as sql
from flask import Flask, render_template, request, abort, jsonify
import os

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DBNAME = f"{BASEDIR}\\netflix.db"

@app.route("/")
def start_page():
	query = """
		SELECT show_id, title
		FROM netflix
		LIMIT 1 
		OFFSET 100
	"""
	s = sql(DBNAME, query)
	return render_template('about.html', s=s)


@app.route("/movie/")
def found_page_name():
	movie_search = request.args.get("title")
	query = f"\
		SELECT title, country, release_year, listed_in, description \
		FROM netflix\
		WHERE title LIKE '%{movie_search}%'\
		ORDER BY 'release_year' DESC\
		LIMIT 1"
	s = sql(DBNAME, query)
	dict_t = {
		"title": s[0][0],
		"country": s[0][1],
		"release_year": s[0][2],
		"genre": s[0][3],
		"description": s[0][4]
	}
	return render_template('found_films.html', s=dict_t)
	# return jsonify(s)


@app.route("/years/")
def found_page_year():
	movie_search_year_from = request.args.get("year_from")
	movie_search_year_to = request.args.get("year_to")
	list_film = []
	query = f"\
		SELECT title, release_year \
		FROM netflix\
		WHERE release_year BETWEEN {movie_search_year_from} AND {movie_search_year_to}\
		LIMIT 100"
	s = sql(DBNAME, query)
	for row in s:
		dict_t = {
			"title": row[0],
			"release_year": row[1],
		}
		list_film.append(dict_t)
	return render_template('found_films_years.html', s=list_film)
	# return jsonify(list_film)


@app.route("/rating/")
def found_page_rating():
	list_rating = []
	dict_t = []
	query = f"\
		SELECT DISTINCT rating \
		FROM netflix \
		ORDER BY rating DESC"
	s = sql(DBNAME, query)
	for row in s:
		list_rating.append(row[0])
	movie_search_rating = request.args.get("rating")
	query = f"\
			SELECT title,  description \
			FROM netflix\
			WHERE rating LIKE '{movie_search_rating}'"
	s = sql(DBNAME, query)
	for row in s:
		dict_t.append({
			"title": row[0],
			"description": row[1]
		})
	return render_template('found_films_rating.html', s=list_rating, w=dict_t, name_sa=movie_search_rating)
	# return jsonify(s)


@app.route("/listed_in/")
def found_page_listed_in():
	list_listed_in = set()
	dict_t = []
	query = f"\
		SELECT DISTINCT listed_in \
		FROM netflix \
		WHERE type = 'Movie' "
	s = sql(DBNAME, query)
	for row in s:
		temp_t = row[0].split(', ')
		for t in temp_t:
			list_listed_in.add(t)
	movie_search_listed_in = request.args.get("listed_in")
	query = f"\
		SELECT title, description \
		FROM netflix\
		WHERE listed_in LIKE '%{movie_search_listed_in}%'\
		ORDER BY release_year DESC\
		LIMIT 10"
	s = sql(DBNAME, query)
	for row in s:
		dict_t.append({
			"title": row[0],
			"description": row[1]
		})
	return render_template('found_films_top10.html', s=list_listed_in, w=dict_t, name_sa=movie_search_listed_in)
	# return jsonify(s)


@app.route("/cast/")
def found_page_cast_to_cast():
	list_listed_in = set()
	dict_t = []
	query = f"\
		SELECT DISTINCT `cast` \
		FROM netflix \
		WHERE `cast` IS NOT NULL \
		ORDER BY `cast`"
	s = sql(DBNAME, query)
	for row in s:
		temp_t = row[0].split(', ')
		for t in temp_t:
			list_listed_in.add(t)
	movie_search_listed_in = request.args.get("listed_in")
	query = f"\
		SELECT title, description \
		FROM netflix\
		WHERE listed_in LIKE '%{movie_search_listed_in}%'\
		ORDER BY 'release_year' DESC\
		LIMIT 10"
	s = sql(DBNAME, query)
	for row in s:
		dict_t.append({
			"title": row[0],
			"description": row[1]
		})
	return render_template('found_films_cast_to_cast.html', s=list_listed_in, w=dict_t, name_sa=movie_search_listed_in)
	# return jsonify(s)

# query = """
# 	SELECT
# 	FROM
#
# """
# sql(DBNAME, query)

if __name__ == '__main__':
	app.run(debug=True)
