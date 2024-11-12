import numpy as np

# 文字列を2次元リストに変換
pattern_str = """
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
0	1	1	1	1	1	1	1	1	1	1	1	1	0	0	0
0	1	1	1	1	1	1	1	1	1	1	1	1	1	0	0
0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	0
0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
0	1	1	1	1	1	1	1	1	0	0	0	0	0	0	0
0	1	1	1	1	1	1	1	1	0	0	0	0	0	0	0
1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0

"""

# 各行を分割して整数リストに変換
pattern_list = [list(map(int, row.split())) for row in pattern_str.strip().split('\n')]

# 2次元リストをビット列に変換
bit_string = ''.join(str(bit) for row in pattern_list for bit in row)

# ビット列を8ビットずつ区切り、バイト配列に変換
byte_array = bytearray(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

# バイト配列を16進数のバイト文字列に変換
bit_pattern_hex = "b'" + ''.join(f"\\x{byte:02x}" for byte in byte_array) + "'"

print(bit_pattern_hex)  # b'\x
