from flask import Flask,render_template,request,session,redirect,url_for
from zenora.client import APIClient
from config import token,client_secret,oauth_url,redirect_url,guild_id
import config
import gdrive
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import helpers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'write a secret key here, it can be anything; even this should work'
client = APIClient(token=token,client_secret=client_secret)

@app.route('/')
def home():
    if 'token' in session:
        return redirect('/drives')
    
    return render_template('index.html',oauth_url=oauth_url)

@app.route('/redir_temp')
def redir():
    return redirect(oauth_url)

@app.route('/authorise')
def oauth():
    try:
        code = request.args['code']
    except KeyError:
        return redirect('/404')
    access_token = client.oauth.get_access_token(code,redirect_url).access_token

    bearer_client = APIClient(access_token,bearer=True)
    current_user = bearer_client.users.get_current_user()
    session['current_user'] = {
        'user_id':current_user.id,
        'in_guild':False
    }

    session['current_user']['in_guild'] = guild_id in [i.id for i in bearer_client.users.get_my_guilds()]

    if session['current_user']['in_guild']:
        session['token'] = access_token
        return redirect('/drives')
    else:
        return redirect('/401')

@app.route('/drives')
def drives():
    if not 'token' in session:
        return redirect('/')
    
    try:
        if not session['current_user']['in_guild']:
            return redirect('/')
    except:
        pass

    return render_template('drives.html',shared_drives = config.drives)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/404')
def e404():
    return render_template('404.html')


@app.route('/401')
def e401():
    return render_template('401.html')


@app.route('/viewdrives/<driveid>')
def vdrive(driveid=None):
    if not 'token' in session:
        return redirect(url_for('redir', next= f'/viewdrives/{driveid}'))
    
    try:
        if not session['current_user']['in_guild']:
            return redirect('/')
    except:
        pass


    if not driveid:
        return redirect('/drives')
    
    dhelper = gdrive.DriveHelp(gdrive.service)

    parents = dhelper.get_master_parents(driveid)

    files = dhelper.list_drive_dir(driveid)
    cleaned_files = helpers.parse_files_list(files)

    try:
        parent_directory = f'/viewdrives/{parents[-2][1]}'
    except:
        parent_directory = '/drives'


    return render_template('view.html',files = cleaned_files,shared_drives = config.drives, parents=parents,parent_directory=parent_directory)



class SearchForm(FlaskForm):
    searched = StringField("What do you want to search ?",validators=[DataRequired()])
    submit = SubmitField("Search")



@app.context_processor
def to_pass_to_search():
    form = SearchForm()
    return dict(form=form)



@app.route('/search',methods=['POST','GET'])
def search():
    if not 'token' in session:
        return redirect('/')
    
    try:
        if not session['current_user']['in_guild']:
            return redirect('/')
    except:
        pass


    if request.method == 'GET':return redirect('/')
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        if searched not in ['',None]:
            dhelper = gdrive.DriveHelp(gdrive.service)
            all_files = dhelper.search_files(searched,None)
            
            cleaned = helpers.parse_files_list(all_files)
            return render_template('search.html',form=form,searched=searched,shared_drives= config.drives,files=cleaned)
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)


