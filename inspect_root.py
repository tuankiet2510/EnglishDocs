import os, sys, requests, json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


token = os.getenv("NOTION_API_TOKEN", "")
if not token:
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("NOTION_API_TOKEN="):
                    token = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                    break

headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2022-06-28'
}
r = requests.get('https://api.notion.com/v1/blocks/26aeb70c-17c5-8060-9c96-e578765d55ad/children?page_size=100', headers=headers)
data = r.json()
results = data.get('results', [])
print(f'Total direct children of EnglishDocs: {len(results)}')
for b in results:
    btype = b['type']
    txt = ''
    if btype == 'child_page':
        txt = b['child_page']['title']
    elif 'rich_text' in b.get(btype, {}):
        txt = ''.join(t.get('plain_text', '') for t in b[btype]['rich_text'])
    print(f'- {btype:15} | {txt[:60]} (id: {b["id"]})')
