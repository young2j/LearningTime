import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Role, Post

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role,Post=Post)


'''
源码分析:记录25个运行最慢的函数分析

from flask.cli import click
@app.cli.command()
@click.option('--length',default=25,help='Number of functions to include in profile report.')
@click.option('--profile-dir',default='.',help='Directory where profile data are saved.')
def profile(length,profile_dir):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions=[length],profile_dir=profile_dir)
    app.run(debug=False)

$flask profile # app.run()报错
'''