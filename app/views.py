from flask import (render_template, session, request,
                  jsonify, redirect, send_file, url_for)


from app import app
from app.users import *


user_manager = UserManager()
user_manager.add_users(
    User(name="guest", password="guest"),
    User(name="user", password="user"),
    User(name="admin", password="admin"),
)


UNPROTECTED = [
    "/favicon.ico",
    "/login",
    "/logout",
]

MOTD = """
    <br>
    A phenomenon is any thing which manifests itself. 
"""


# Inject middleware for every request
@app.before_request
def access_control():
    if request.path.startswith("/static") or request.path in UNPROTECTED:
        pass
    else:
        username = session.get("user", None)
        # Handle login
        if username is None and request.path != "/login":
            return redirect(url_for("login", next=request.path))
        # Check access control
        if not app.access_controller.is_allowed(request, username):
            return render_template('error.html', msg="Access if not allowed, sorry!")


# Inject user session var into every template
@app.context_processor
def inject_last_tasks():
    username = session.get("user", None)
    return dict(user=user_manager.get_user(username))


# Routes description.
@app.route('/', methods=['GET'])
def hello():
    return render_template(
        'index.html',
        title="""
        Welcome to the <span class="logo-lg"><b>P</b>henomen Application</span>
        """,
        msg="""
        Phenomen implements very strong and secure access control models.
        """,
        panda=url_for("static", filename="imgs/index.svg"),
    )


@app.route('/motd', methods=['GET', 'POST'])
def motd():
    global MOTD
    if request.method == 'GET':
        return render_template(
            'index.html',
            title="""
                    Today's <span class="logo-lg">Message of The <b>Day</b>:</span>
                    """,
            msg=MOTD + """

                    <div class="col-sm-10 col-sm-offset-1 change-motd">   
                        <form method="post">
                            <div class="form-group has-feedback">
                                <textarea type="text" class="form-control" name="motd" required autofocus rows=4></textarea>
                                <span class="glyphicon glyphicon-user form-control-feedback"></span>
                            </div>
                            <div class="col-xs-4 col-xs-offset-8">
                                <button type="submit" class="btn btn-primary btn-block btn-flat btn-motd">Set New MoTD</button>
                            </div>
                        </form>
                    <!-- /.col -->
                    </div>
                """,
            panda=url_for("static", filename="imgs/motd.svg"),
        )

    if request.method == 'POST':
        new_motd = request.form.get('motd', None)
        if new_motd != None:
            MOTD = new_motd
        return redirect("motd")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template(
        'index.html',
        title="""
            Here we are in super secret place! <br> Only <b>admin</b>s can browse it 
            """,
        msg="""
            If you tune your policy well surely...
            """,
        panda=url_for("static", filename="imgs/admin.svg"),
    )


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    return render_template(
        'index.html',
        title="""
            Do you looking for some stats? <br> We have some! 
            """,
        msg="""
            If you tune your policy well surely...
            """,
        panda=url_for("static", filename="imgs/stats.svg"),
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Get values from form
        name = request.form['login']
        password = request.form['password']
        # Find the user in the "database"
        user = user_manager.get_user(name)
        # Check password
        if user is None or user.password != sha256(password.encode()).hexdigest():
            return render_template('login.html', error="Wrong password!")
        # Log him in
        session['user'] = user.name
        # Redirect to the desired page
        next_page = request.args.get('next', '/')
        return redirect(next_page)


@app.route('/logout')
def logout():
    del session['user']
    return redirect(url_for("login"))
