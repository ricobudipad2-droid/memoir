import json
class Analyzer:
    def __init__(self, mimo_client, db):
        self.mimo = mimo_client
        self.db = db
    def analyze_and_save(self, content, title='', tags=''):
        result, tokens = self.mimo.analyze_entry(content)
        entry_id = self.db.add_entry(content=content, title=title, tags=tags, mood_score=result.get('mood_score',5), sentiment=result.get('sentiment','neutral'), themes=json.dumps(result.get('themes',[])), emotions=json.dumps(result.get('emotions',[])), insights=result.get('insights',''), tokens_used=tokens)
        self.db.track_tokens(tokens)
        return entry_id, result, tokens
