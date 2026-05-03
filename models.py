import sqlite3
from datetime import date

class Database:
    def __init__(self, path='memoir.db'):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._migrate()
    def _migrate(self):
        self.conn.executescript('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, title TEXT DEFAULT '', tags TEXT DEFAULT '', mood_score REAL DEFAULT 0, sentiment TEXT DEFAULT 'neutral', themes TEXT DEFAULT '[]', emotions TEXT DEFAULT '[]', insights TEXT DEFAULT '', tokens_used INTEGER DEFAULT 0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);CREATE TABLE IF NOT EXISTS token_usage (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL UNIQUE, total_tokens INTEGER DEFAULT 0, entry_count INTEGER DEFAULT 0);''')
    def add_entry(self, content, title='', tags='', mood_score=0, sentiment='neutral', themes='[]', emotions='[]', insights='', tokens_used=0):
        cur = self.conn.execute('INSERT INTO entries (content,title,tags,mood_score,sentiment,themes,emotions,insights,tokens_used) VALUES (?,?,?,?,?,?,?,?,?)', (content,title,tags,mood_score,sentiment,themes,emotions,insights,tokens_used))
        self.conn.commit()
        return cur.lastrowid
    def get_entry(self, id):
        return self.conn.execute('SELECT * FROM entries WHERE id=?', (id,)).fetchone()
    def get_entries(self, limit=50, tag=None, search=None):
        q = 'SELECT * FROM entries WHERE 1=1'
        p = []
        if tag: q += ' AND tags LIKE ?'; p.append(f'%{tag}%')
        if search: q += ' AND content LIKE ?'; p.append(f'%{search}%')
        q += ' ORDER BY created_at DESC LIMIT ?'; p.append(limit)
        return self.conn.execute(q, p).fetchall()
    def get_mood_history(self, days=30):
        return self.conn.execute('SELECT created_at, mood_score, sentiment FROM entries ORDER BY created_at DESC LIMIT ?', (days,)).fetchall()
    def track_tokens(self, tokens):
        today = date.today().isoformat()
        self.conn.execute('INSERT INTO token_usage (date, total_tokens, entry_count) VALUES (?,?,1) ON CONFLICT(date) DO UPDATE SET total_tokens=total_tokens+?, entry_count=entry_count+1', (today, tokens, tokens))
        self.conn.commit()
    def get_stats(self):
        t = self.conn.execute('SELECT COUNT(*) as c, COALESCE(SUM(tokens_used),0) as t FROM entries').fetchone()
        r = self.conn.execute('SELECT * FROM entries ORDER BY created_at DESC LIMIT 5').fetchall()
        return {'total_entries': t['c'], 'total_tokens': t['t'], 'recent': r}
