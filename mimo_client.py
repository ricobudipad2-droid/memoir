import json
from openai import OpenAI
class MiMoClient:
    def __init__(self, api_key, base_url, model):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    def analyze_entry(self, content):
        try:
            resp = self.client.chat.completions.create(model=self.model, messages=[{'role':'system','content':'You are an empathetic journal analyst. Return valid JSON: {"sentiment":"positive/negative/neutral","mood_score":1-10,"themes":[],"emotions":[],"insights":"..."}'},{'role':'user','content':f'Analyze this journal entry:\n{content}'}], temperature=0.3, max_tokens=1024)
            text = resp.choices[0].message.content or '{}'
            if '```json' in text: text = text.split('```json')[1].split('```')[0]
            elif '```' in text: text = text.split('```')[1].split('```')[0]
            result = json.loads(text.strip())
            tokens = (resp.usage.prompt_tokens or 0) + (resp.usage.completion_tokens or 0)
            return result, tokens
        except Exception as e:
            return {'sentiment':'neutral','mood_score':5,'themes':[],'emotions':[],'insights':str(e)}, 0
