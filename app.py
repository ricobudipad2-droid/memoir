import os, json
import tornado.ioloop, tornado.web
from config import Config
from models import Database
from mimo_client import MiMoClient
from analyzer import Analyzer

db = Database(Config.DB_PATH)
mimo = MiMoClient(Config.MIMO_API_KEY, Config.MIMO_BASE_URL, Config.MIMO_MODEL)
analyzer = Analyzer(mimo, db)

class IndexHandler(tornado.web.RequestHandler):
    def get(self): self.render('index.html', error=None)
class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        stats = db.get_stats()
        mood = db.get_mood_history(30)
        mood_json = json.dumps([{'date':str(m['created_at']),'score':m['mood_score'],'sentiment':m['sentiment']} for m in mood])
        self.render('dashboard.html', stats=stats, mood_json=mood_json)
class WriteHandler(tornado.web.RequestHandler):
    def post(self):
        content = self.get_argument('content','')
        title = self.get_argument('title','')
        tags = self.get_argument('tags','')
        if not content.strip(): self.render('index.html', error='Please write something'); return
        entry_id, result, tokens = analyzer.analyze_and_save(content, title, tags)
        self.redirect(f'/entry/{entry_id}')
class EntryHandler(tornado.web.RequestHandler):
    def get(self, entry_id):
        entry = db.get_entry(int(entry_id))
        if not entry: raise tornado.web.HTTPError(404)
        self.render('entry.html', entry=entry)
class HistoryHandler(tornado.web.RequestHandler):
    def get(self):
        tag = self.get_argument('tag', None)
        search = self.get_argument('q', None)
        self.render('history.html', entries=db.get_entries(50, tag=tag, search=search), tag=tag, search=search)
class APIEntriesHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/json')
        self.write(json.dumps([dict(e) for e in db.get_entries(20)], default=str))
    def post(self):
        data = json.loads(self.request.body)
        entry_id, result, tokens = analyzer.analyze_and_save(data.get('content',''), data.get('title',''), data.get('tags',''))
        self.set_header('Content-Type','application/json')
        self.write(json.dumps({'id':entry_id,'result':result,'tokens':tokens}))
class APIMoodHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/json')
        self.write(json.dumps([dict(m) for m in db.get_mood_history(30)], default=str))

if __name__ == '__main__':
    app = tornado.web.Application([(r'/',IndexHandler),(r'/dashboard',DashboardHandler),(r'/write',WriteHandler),(r'/entry/(\d+)',EntryHandler),(r'/history',HistoryHandler),(r'/api/entries',APIEntriesHandler),(r'/api/mood-history',APIMoodHandler)], template_path='templates', static_path='static', debug=False)
    app.listen(Config.PORT)
    print(f'Memoir running on http://localhost:{Config.PORT}')
    tornado.ioloop.IOLoop.current().start()
