v2 = [None] *22
v2[0] = 84
v2[1] = 101
v2[2] = 97
v2[3] = 109
v2[4] = 84
v2[5] = 53
v2[6] = 123
v2[21] = 125

v2[17] = 25 #int((200 - 3 * v2[0]) / 2)
v2[8] = 49 #int((4 - v2[2] - 3 * v2[5]) / 5)
v2[14] = 151 #int(v2[5] - 205)
v2[16] = int(147 - v2[8])
v2[13] = 75 #int((v2[17] - 126) / 2)
v2[15] = 10 #int(65 + v2[13])

v2[11] = int(246 + v2[13] - 2)
v2[9] = int((226 - 8 * v2[15]) / 6)
v2[19] = 11 #int(156 - v2[11])
v2[10] = int(244 + 56 + v2[9])
v2[7] = int(v2[11] - 5)
v2[12] = int(194 - v2[7])
v2[20] = 24 #int(v2[19] + v2[12] - 44)
v2[18] = 1 #int((v2[16] + 2 * v2[17] - 152) / 3)

#(unsigned __int8)(v2[12] + v2[7]) == 194
#(unsigned __int8)(v2[16] + v2[8]) == 147
#(unsigned __int8)(v2[10] + -56 - v2[9]) == 244
#(unsigned __int8)(v2[11] - v2[13] + 2) == 246
#(unsigned __int8)(v2[19] + v2[12] - v2[20]) == 44
#(unsigned __int8)(v2[5] - v2[14]) == 205
#(unsigned __int8)(3 * v2[0] + 2 * v2[17]) == 200
if (4 * v2[15] - 7 * v2[17]) == 2:
    print("yes")
print((4 * v2[15] - 7 * v2[17]))
#(unsigned __int8)(v2[16] + 2 * v2[17] - 3 * v2[18]) == 152
#(unsigned __int8)(5 * v2[8] + 3 * v2[5] + v2[2]) == 4
if (v2[16] + v2[7] - v2[12] - v2[20]) == 252 : 
    print("yes")
print(v2[16] + v2[7] - v2[12] - v2[20])
print("=====")
#(unsigned __int8)(v2[11] + v2[19]) == 156
#(unsigned __int8)(v2[17] - 2 * v2[13]) == 126
#(unsigned __int8)(6 * v2[9] + 8 * v2[15]) == 226
#(unsigned __int8)(v2[13] - v2[15]) == 65
#(unsigned __int8)(v2[11] - v2[7]) == 5 )
# for i in range(22):
#     if(v2[i] < 0):
#         v2[i] = ~v2[i]

# for i in range(22):
#     print(v2[i])

print(v2)
for i in range(22):
    v2[i] = chr(v2[i])
print(v2)