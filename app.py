import os


from flask import Flask, render_template, request
from forms import WorkoutSearchForm
from workout_search import SugarWodSearch
from tables import WorkoutResults, Workout


application = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@application.route('/', methods=['GET', 'POST'])
def home():
	search = WorkoutSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)
	return render_template("_search.html", form=search)


@application.route('/results')
def search_results(search):
	search_string = search.data['search']
	results = SugarWodSearch(search_string)
	table = WorkoutResults([Workout(result) for result in results])
	table.border = True
	return render_template("_search.html", form=search, table=table)


@application.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		message = 'File NOT uploaded!'
		target = os.path.join(APP_ROOT, 'data')
		f = request.files['file']
		filename = f.filename
		destination = "/".join([target, filename])
		f.save(destination)
		message = 'File Uploaded!'
		return render_template('upload.html', message=message)
	return render_template('upload.html')


@application.errorhandler(404)
def page_not_found(e):
	return render_template('_404.html'), 404

def page_not_found(e):
	return render_template('404.html'), 404


if __name__ == '__main__':
	application.config['TEMPLATES_AUTO_RELOAD'] = True
	application.secret_key = os.urandom(12)
	application.run(host='0.0.0.0')