import os, soundcloud, urllib, string, zipfile, numpy, shutil
from flask import Flask, render_template, request, url_for, send_from_directory

application = Flask(__name__)
application.debug = True
application.config['soundcloud_id'] = '03d95ebd66def1de4e31e0bd60b1e718'
application.config['soundcloud_secret'] = 'e1fc2d755ea297c574381ce982ad31e7'
application.config['soundcloud_favorites'] = []

@application.route('/')
def initializesite():
	return render_template('form_submit.html')
	
@application.route('/soundcloudfavorites/', methods=['POST'])
def soundcloudfavorites():
	if request.method == 'POST':
		application.config['soundcloud_username'] = request.form['youremail']
		application.config['soundcloud_password'] = request.form['yourpassword']
		numberOfFavs = request.form['numberoflikes']
		#favsOffset = request.form['favoritesOffset']
		soundcloud_login_info = soundcloud.Client(client_id=application.config['soundcloud_id'], client_secret=application.config['soundcloud_secret'], username=application.config['soundcloud_username'], password=application.config['soundcloud_password'])
		soundcloud_username = soundcloud_login_info.get('/me').username
		my_soundcloud_id = soundcloud_login_info.get('/me').id
		my_soundcloud_favorites = soundcloud_login_info.get('/users/' + str(my_soundcloud_id) + '/favorites?limit=' + numberOfFavs + '?linked_partitioning=1' + '?offset=0')
		count = -1
		favorites_name = []
		favorites_stream_url = []
		progress = 0
		for fav_num in my_soundcloud_favorites:
			count += 1
			try:
				fav = my_soundcloud_favorites[count].obj
				artist = fav['user']['username']
				title = fav['title']
				fav_stream_url = fav['stream_url']
				stream_url = soundcloud_login_info.get(fav_stream_url, allow_redirects=False).location
				filename = artist + " - " + title + ".mp3"
				filename = string.replace(filename, '<', " ")
				filename = string.replace(filename, '>', " ")
				filename = string.replace(filename, ':', " ")
				filename = string.replace(filename, '"', " ")
				filename = string.replace(filename, '/', " ")
				filename = string.replace(filename, '\\', " ")
				filename = string.replace(filename, '|', " ")
				filename = string.replace(filename, '?', " ")
				filename = string.replace(filename, '*', " ")
				filename = string.replace(filename, '#', " ")
				favorites_name.append(filename)
				favorites_stream_url.append(stream_url)
			except:
				continue
	else:
		print "invalid"
		return "form not posted"
	favorites = zip(favorites_name, favorites_stream_url)
	application.config['soundcloud_favorites'] = favorites
	return render_template('form_action.html', soundcloud_username=soundcloud_username, favorites=favorites)

@application.route('/singlelikedownload/', methods=['POST'])
def singlelikedownload():
	script_dir = os.path.dirname(os.path.abspath(__file__))
	dir_path = os.path.join(script_dir, 'sounds')
	fileList = os.listdir(dir_path)
	for fileName in fileList:
		os.remove(dir_path+"/"+fileName)
	filename_to_download = request.form['likename']
	url_to_download = request.form['likeurl']
	savedSCfile = urllib.URLopener()
	savedSCfile.retrieve(url_to_download, os.path.join(dir_path, filename_to_download))	
	dir_path_file = os.path.join('sounds/', filename_to_download)
	return send_from_directory('', dir_path_file, as_attachment=True)

@application.route('/soundcloudlikeszipdownload/', methods=['POST'])
def soundcloudlikeszipdownload():
	script_dir = os.path.dirname(os.path.abspath(__file__))
	dir_path = os.path.join(script_dir, 'sounds')
	fileList = os.listdir(dir_path)
	for fileName in fileList:
		os.remove(dir_path+"/"+fileName)
	dir_path_zip = os.path.join('sounds/', 'MySoundcloudFavorites.zip')
	zfile = zipfile.ZipFile(dir_path_zip, 'w')
	for n,u in application.config['soundcloud_favorites']:	
		print "Working on " + n
		savedSCfile = urllib.URLopener()
		savedSCfile.retrieve(u, n)
		zfile.write(n)
		os.remove(n)
	zfile.close()
	return send_from_directory('', dir_path_zip, as_attachment=True)
	
# Run the app :)
if __name__ == '__main__':
	application.run(port=5000, host='127.0.0.1')