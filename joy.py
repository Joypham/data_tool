joy = [
["short_id", "countries", "square_image", "itune_album_id"],
["short_id", "countries", "square_image"],
["short_id", "square_image"],
["short_id", "countries", "square_image", "verification"],
["short_id"],
["short_id", "square_image", "verification"],
["short_id", "countries", "square_image", "verification", "itune_album_id"],
["countries", "square_image"],
["square_image"],
["short_id", "square_image", "itune_album_id"],
["$field", "short_id", "countries", "square_image", "verification"],
["countries", "square_image", "verification"],
["short_id", "verification"],
["short_id", "countries"],
["short_id", "square_image", "verification", "itune_album_id"],
["square_image", "verification"],
["short_id", "countries", "square_image", "verification", "itunes_album_id_1"],
["short_id", "countries", "square_image", "verification", "itune_album_id", "itunes_album_id_1"],
["countries", "square_image", "itune_album_id"]
]
joy_xinh = []
for i in joy:
    for k in i:
        joy_xinh.append(k)

k = joy_xinh
mylist = set(k)
print(mylist)











