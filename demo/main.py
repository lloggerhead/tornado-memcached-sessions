import os
import tornado.ioloop
import tornado.web
import tornado.escape
import sys
sys.path.append("..")
from session import Session

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = Session(self)

    # autosave session to server when request finish
    def on_finish(self):
        self.session.save()

    def get_current_user(self):
        return self.session.get("user", None)

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write(self.get_current_user())

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.session["user"] = self.get_argument("user")
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        del self.session["user"]
        self.redirect("/login")

class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            cookie_secret = "YOU_SHOULD_CHANGE_THIS",
            session_secret = "YOU_SHOULD_CHANGE_THIS",
            login_url = "/login",
            debug = True,
        )

        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        Session.register(settings["session_secret"])

def main():
    app = Application()
    app.listen("8888")
    print "start on port 8888..."
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
