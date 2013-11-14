import os
import tornado.ioloop
import tornado.web
import tornado.escape
import sys
sys.path.append("..")
import session
        
class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = session.Session(self.application.session_manager, self)

    def get_current_user(self):
        res = self.session.get("name", None)
        return res
        
class IndexHandler(BaseHandler):
    def get(self):
        self.write(self.get_current_user())

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        self.session["name"] = self.get_argument("name")

class LogoutHandler(BaseHandler):
    def get(self):
        if self.session.get("name", None):
            print("logout")
            del self.session["name"]
        print(self.session.get("name", "nothing"))
        #self.redirect("/login")

class Application(tornado.web.Application):
    def __init__(self):
        
        settings = dict(
            cookie_secret = "YOU_SHOULD_CHANGE_THIS",
            session_secret = "YOU_SHOULD_CHANGE_THIS",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            login_url = "/login",
            debug = True,
            memcached_address = ["127.0.0.1:11211"],
        )
        
        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
        ]
        
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = session.SessionManager(settings["session_secret"])

def main():
    app = Application()
    app.listen("8888")
    print "start on port 8888..."
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
        pass
