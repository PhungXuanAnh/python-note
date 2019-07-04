import json
import random


post = {
    "post_text": "this is test text",
    "post_like": 1074,
    "post_view": 5,
    "post_comment": 0,
    "post_id": "2716120005077509",
    "images": [],
    "timestamp": 1560837600,
    "post_share": 0,
    "username": "K14vn",
    "tag": "hat paper hat furniture cat river person house tree river person"
}

tags = ["person", "animal", "furniture", "computer", "table",
        "paper", "dog", "cat", "tree", "house", "moto", "car",
        "music", "hat", "river"]

# data = []
# for i in range(0, 500000):
#     dt = {
#         "post_text": "this is test text",
#         "post_like": random.choice(range(0, 50),
#         "post_view": random.choice(range(0, 50),
#         "post_comment": random.choice(range(0, 50),
#         "post_share": random.choice(range(0, 50),
#         "post_id": str(2716120 + i),
#         "timestamp": 1560837600 + i,
#         "username": "K14vn",
#         "tag": " ".join(random.choices(tags, k=random.randint(0, len(tags))))
#     }
#     data.append(dt)
# with open('branlytic1.json', "w+") as out_file:
#     json.dump(data, out_file, indent=4)

with open('branlytic1.csv', "w+") as out_file:
    # data = ','.join(['post_text', 'post_like', 'post_view', 'post_comment', 'post_share', 'post_id', 'timestamp', 'username', 'tag'])
    # out_file.write(data + "\n")
    for i in range(0, 500000):
        data = [
            "this is test text",
            str(random.choice(range(0, random.randint(10, 500)))),
            str(random.choice(range(0, random.randint(10, 500)))),
            str(random.choice(range(0, random.randint(10, 500)))),
            str(random.choice(range(0, random.randint(10, 500)))),
            str(2716120 + i),
            str(1560837600 + i),
            "K14vn",
            " ".join(random.choices(tags, k=random.randint(0, len(tags)))),
        ]
        data = ','.join(data)
        out_file.write(data + "\n")
