import json

d = {
    'name': '小明',
    'age': 18,
    'hobby': ['football', 'basketball']
}

S = json.dumps(d, ensure_ascii=False)
print(type(S))
print(S)