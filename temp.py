def read_pos(str1, str2):
    pos1 = tuple(map(int, str1.split(",")))
    pos2 = tuple(map(int, str2.split(",")))
    return pos1, pos2


def make_pos(tup1, tup2):
    pos_str1 = str(tup1[0]) + "," + str(tup1[1])
    pos_str2 = str(tup2[0]) + "," + str(tup2[1])
    return pos_str1, pos_str2

pos_tuple1 = (20, 45)
pos_tuple2 = (30, 60)

result = make_pos(pos_tuple1, pos_tuple2)
print(result)

# result = read_pos("20,45", "20,45")

print(result)
