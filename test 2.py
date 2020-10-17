joy = ['ok', 'not ok', 'xinh', 'cao', 'thong minh']
with open("/Users/phamhanh/PycharmProjects/data_operation_fixed1/sources/query.txt", "w") as f:
    for i in joy:
        joy_xinh = i
        print(joy_xinh)
        f.write(joy_xinh+ "\n")



