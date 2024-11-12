WIDTH = 16
HEIGHT = 16
FIRST = 48
LAST = 107
_FONT = \
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\xff\xdf\xff\xd7\xff\x54\xff\x57\xff\x57\xff\x5f\xff\x5f\xff\x5f\xff\xdf\xff\xd8\xff\xdf\xff\xdf\xff\xde\xff\xde\xff\xdd\xff\xd3'\
b'\xbf\xff\xb7\xbf\x03\xd8\xb7\xef\xb7\xff\xb7\xf8\xb7\xfb\xb7\x1b\xb5\xd8\x01\xde\x5f\xdd\x6f\xdb\xef\xd7\xf7\xcf\xfb\xb3\xfd\x7c'\
b'\xbf\xff\xbe\xff\x00\xff\xbf\xff\xbb\xff\x01\xff\xbb\xff\xbb\xff\x03\xff\xbf\xff\x8f\xff\xb7\xff\xbb\xff\xbf\xff\xff\xff\x01\xff'\
b'\xff\xff\x80\xff\x80\x7e\x9f\x3c\x9f\x39\x9f\x33\x9f\x33\x80\x73\x80\xf3\x93\xf0\x99\xf0\x9c\xf3\x9e\x73\x9f\x33\x9f\xb3\xff\xff'\
b'\xff\xff\x7e\x07\x3e\x03\x9e\x79\xce\x79\xe6\x79\xe6\x79\xe6\x03\xe6\x07\x06\x7f\x06\x7f\xe6\x7f\xe6\x7f\xe6\x7f\xe6\x7f\xff\xff'\
b'\xff\xff\x02\x07\x02\x03\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\xce\x79\x02\x03\x02\x07\xff\xff'\
b'\x01\x80\x01\x04\xff\xfe\x01\x00\x3f\xf8\x21\x08\x3f\xf8\x21\x08\x3f\xf8\x23\x88\x05\x40\x09\x20\x11\x18\x21\x0e\xc1\x04\x01\x00'\
b'\x01\x80\x01\x04\xff\xfe\x00\x00\x10\x10\x1f\xf8\x10\x10\x10\x10\x1f\xf0\x11\x10\x01\x00\x19\x20\x11\x18\x21\x0c\xc7\x04\x02\x00'\
b'\x00\x00\x00\x00\x1f\xcf\x02\x00\x02\x07\x02\x08\x02\x08\x02\x08\x02\x08\x02\x08\x02\x08\x02\x08\x02\x08\x07\x07\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\xe6\x33\x02\x21\xc2\x41\x22\x40\x22\x80\x23\x80\x22\x80\x22\x40\x22\x40\x22\x20\x22\x20\xc6\x30\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x19\xfc\x10\x00\x10\xf8\xa1\x04\xa1\x04\x41\x04\x41\x04\x41\x04\x41\x04\x41\x04\x41\x04\xe0\xf8\x00\x00\x00\x00'\
b'\x00\x00\x10\x7c\x30\xc6\x71\x83\xb1\x83\x31\x83\x31\x83\x31\x83\x31\x83\x31\x83\x31\x83\x31\x83\x31\x83\x30\xc6\xfc\x7c\x00\x00'\
b'\x00\x00\x08\x38\x18\x6c\x38\xc6\x58\xc6\x18\xc6\x18\xc6\x18\xc6\x18\xc6\x18\xc6\x18\xc6\x18\xc6\x18\xc6\x18\x6c\x7e\x38\x00\x00'\
b'\x00\x00\xff\xfe\x01\x00\x01\x00\x01\x00\x7f\xfc\x41\x04\x41\x04\x49\x24\x49\x24\x49\x24\x4f\xe4\x48\x24\x40\x04\x40\x3c\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x00\x90\x00\x83\x5b\x85\x24\x85\x23\x95\x25\x63\xa7\x00\x00'\
b'\x00\x08\x7f\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x3f\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\xff\xfe'\
b'\x00\x80\x3f\xfe\x22\x50\x24\xa0\x2d\xfc\x34\xa0\x25\xfc\x26\x80\x27\xfc\x24\x10\x27\xfe\x24\x00\x27\xfc\x40\x04\x54\xbc\x92\xa8'\
b'\x00\x00\xc6\x38\x44\x10\x44\x10\x6c\x10\x6c\x10\x6c\x10\x6c\x10\x54\x10\x54\x10\x54\x10\x54\x10\x54\x10\x44\x10\xee\x38\x00\x00'\
b'\x00\x00\xfe\x10\x92\x10\x92\x10\x10\x28\x10\x28\x10\x28\x10\x28\x10\x28\x10\x28\x10\x7c\x10\x44\x10\x44\x10\x44\x38\xee\x00\x00'\
b'\x00\x00\xee\x10\x44\x10\x48\x10\x48\x28\x50\x28\x50\x28\x70\x28\x48\x28\x48\x28\x48\x7c\x44\x44\x44\x44\x44\x44\xee\xee\x00\x00'\
b'\x18\x04\x10\x8e\xfe\xf0\x44\x80\x28\x80\xfe\x84\x10\xfe\x14\x88\xfe\x88\x10\x88\x38\x88\x54\x88\x91\x08\x11\x08\x12\x08\x14\x08'\
b'\x01\x80\x41\x04\x7f\xfe\xc0\x04\x98\x08\x17\xfc\x10\x40\x22\x84\x33\xfe\x62\x04\xa2\x04\x23\xfc\x22\x04\x22\x04\x23\xfc\x22\x04'\
b'\x00\x00\x00\x00\x39\x17\x45\x12\x45\x12\x41\x12\x41\x12\x39\xf2\x05\x12\x05\x12\x05\x12\x45\x12\x45\x12\x39\x17\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x44\x74\x64\x24\x64\x24\x64\x24\x54\x24\x54\x24\x54\x24\x54\x24\x4d\x24\x4d\x24\x4d\x24\x44\xc3\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x28\xa1\x28\xa1\x29\x21\x29\x21\x2a\x21\x2e\x21\x2a\x21\x2a\x21\x29\x21\x29\x21\x28\xa1\xc8\x9e\x00\x00\x00\x00'\
b'\x7f\xfc\x01\x00\xff\xfe\x81\x02\xbd\x7a\x81\x02\x3d\x78\x00\x00\x3f\xf8\x21\x08\x3f\xf8\x21\x08\x3f\xf8\x01\x00\x01\x02\x00\xfe'\
b'\x01\x00\xff\xfe\x01\x00\x01\x00\x7f\xfc\x41\x04\x41\x04\x7f\xfc\x41\x04\x41\x04\x7f\xfc\x01\x00\x01\x00\xff\xfe\x01\x00\x01\x00'\
b'\x04\x00\x02\x04\x02\x02\x04\x08\x07\x04\x58\xb0\x68\x88\x08\x84\x08\x84\x10\x82\x10\x82\x20\x80\x25\x00\x43\x00\x42\x00\x00\x00'\
b'\x03\x00\x01\x00\x01\x00\x41\x30\x3f\xc0\x01\x00\x09\x00\x11\x30\x0f\xc0\x01\x00\x01\x00\x0f\x00\x11\xc0\x11\x20\x0e\x10\x00\x00'\
b'\x00\x00\x00\x00\x40\x00\x20\x00\x20\x30\x20\x08\x40\x08\x40\x04\x44\x04\x44\x04\x28\x00\x28\x00\x30\x00\x18\x00\x00\x00\x00\x00'\
b'\x00\x00\x10\x00\x08\x00\x09\xc0\x0a\x20\x12\x10\x12\x10\x14\x10\x14\x10\x14\x10\x08\x10\x08\x20\x00\x20\x00\x40\x01\x80\x06\x00'\
b'\x03\x00\x01\x00\x01\x00\x41\x30\x3f\xc0\x01\x00\x09\x00\x11\x30\x0f\xc0\x01\x00\x01\x00\x0f\x00\x11\xc0\x11\x20\x0e\x10\x00\x00'\
b'\x01\x80\x00\x80\x00\x80\x83\xfe\x7c\x80\x00\x80\x07\x80\x08\x80\x08\x80\x09\x80\x06\x80\x00\x80\x01\x00\x01\x00\x02\x00\x0c\x00'\
b'\x00\x00\x10\x38\x30\x44\x10\x82\x10\xc2\x10\xc2\x10\x04\x10\x08\x10\x10\x10\x20\x10\x40\x10\x40\x10\x82\x10\x82\x38\xfe\x00\x00'\
b'\x00\x00\x8f\xf8\x41\x10\x40\xa0\x07\xfc\x04\x44\xe4\x44\x27\xfc\x24\x44\x24\x44\x27\xfc\x24\x44\x24\x44\x24\x4c\x50\x00\x8f\xfe'\
b'\x80\x00\x43\xfc\x22\x04\x02\x7c\x02\x44\xe2\x44\x27\xfe\x22\x02\x22\xfa\x22\x8a\x22\x8a\x22\xfa\x22\x02\x22\x06\x50\x00\x8f\xfe'\
b'\x20\x00\x18\x00\x10\x00\x10\x00\x10\x00\x10\x00\x10\x00\x10\x00\x10\x00\x10\x08\x10\x08\x10\x10\x10\x20\x08\xc0\x07\x00\x00\x00'\
b'\x10\x00\x10\x8f\x3f\xc9\x20\x89\x51\x0f\x0a\x09\x06\x09\x09\x0f\x30\x89\x40\x69\xff\xcf\x40\x40\x40\x55\x40\x55\x7f\xd4\x40\x53'\
b'\x00\x10\xdf\x10\x11\x17\x11\x10\xd1\x23\x11\x22\x1f\x63\xd9\x20\x18\x2f\x18\x28\xd4\x28\x54\x23\x54\x20\x52\x20\xa2\x20\x21\x23'\
b'\x80\x20\x88\x22\xfb\xfe\x00\x20\xe1\xfc\x21\x24\xe1\x24\x01\xfc\xf9\x24\x09\x24\x29\xfc\xe0\x21\x83\xff\x80\x20\x80\x20\x80\x20'\
b'\x00\x00\x60\x0f\x60\x1f\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x7f\x9f\x7f\x8f\x00\x00'\
b'\x00\x00\x07\x80\x8f\xc1\xd8\x63\xd8\x66\xd8\x0c\xd8\x0c\xd8\x0c\xd8\x0c\xd8\x0f\xd8\x0f\xd8\x6c\xd8\x6c\x8f\xcc\x07\x8c\x00\x00'\
b'\x00\x00\x83\x00\xc3\x00\x63\x00\x33\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\xfb\x00\xfb\x00\x1b\x00\x1b\x00\x1b\xfc\x1b\xfc\x00\x00'\
b'\x02\x00\x02\x00\x02\x00\x7f\xf3\x42\x12\x42\x12\x42\x12\x42\x12\x42\x12\x7f\xf7\x02\x00\x02\x00\x02\x00\x02\x00\x02\x01\x02\x06'\
b'\x20\x10\x20\x10\x20\x53\xfe\x50\x22\x78\x22\x50\x22\x17\x22\x10\x22\x18\xff\x37\x20\x50\x50\x10\x50\x12\x88\x12\x04\x10\x03\x10'\
b'\x81\x10\x81\x10\xe1\x10\x81\x3c\x83\x14\x83\x94\xf3\x94\x25\x14\x21\x7f\xf1\x10\x21\x18\x21\x28\x21\x24\x21\x24\x21\x42\xe1\x41'\
b'\x39\x17\x45\x10\x41\x14\x41\xf4\x41\x14\x45\x14\x39\x13\x00\x00\x4c\xe4\xaa\x8a\x8a\x88\x4c\xe8\x28\x88\xa8\x8a\x48\xe4\x00\x00'\
b'\xdf\x00\x00\x00\x4e\x00\x51\x00\x51\x00\x51\x00\x8e\x00\x00\x00\xe4\x86\x4a\x85\x4a\x85\x4a\x86\x4e\x86\x4a\x85\xea\xe5\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x26\x74\x55\x26\x55\x25\x56\x25\x74\x25\x54\x26\x54\x74\x00\x00'\
b'\x00\x00\x00\x00\x00\x7f\x00\x40\x00\x40\x00\x4f\x00\x48\x00\x48\x00\x48\x00\x48\x00\x4f\x00\x48\x00\x40\x00\x40\x00\x7f\x00\x40'\
b'\x00\x02\x04\x41\xfe\x21\x04\x10\x04\x07\xe4\x00\x24\x00\x24\xe0\x24\x2f\x24\x20\xe4\x20\x24\x20\x04\x21\x04\x32\xfc\x4c\x04\x83'\
b'\x10\x00\x10\x00\x20\x00\x44\x00\xfc\x00\x40\x00\x40\x00\x42\x00\xfe\x00\x40\x00\xa0\x00\x90\x00\x08\x00\x04\x00\x00\x00\xfe\x00'\
b'\x39\x17\x45\x11\x45\x11\x45\x11\x45\x11\x45\x11\x38\xe1\x00\x00\x00\x73\x00\x8a\x00\x82\x00\x73\x00\x0a\x00\x8a\x00\x73\x00\x00'\
b'\xc3\x9f\x04\x50\x04\x50\x04\x5e\x04\x50\x04\x50\x03\x90\x00\x00\xef\x22\x08\xa2\x08\xa2\xcf\x22\x0a\x22\x09\x14\xe8\x88\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe7\x3e\x48\xa0\x48\x20\x48\x3c\x48\x20\x48\xa0\xe7\x3e\x00\x00'\
b'\x00\x03\x00\x03\x00\x03\x00\x03\x00\x03\x00\x03\x00\x03\x00\x03\xf0\x03\xf0\x03\xf0\x03\xf8\x07\xff\xff\x7f\xff\x3f\xff\x0f\xfc'\
b'\xff\xf8\xff\xfc\xff\xfe\xff\xfe\xc0\x0f\xc0\x07\xc0\x07\xc0\x0f\xc7\xfe\xc3\xfe\xc1\xfc\xc0\xf0\xc0\x78\x80\x3c\x00\x1e\x00\x0f'

FONT = memoryview(_FONT)

# 0x00(0から)
# 空白
# 快速
#
#
# RAPID
#
#
# 東
# 京
# TOKYO
#
# 10(日本語)
# 10(英語)
# 両
# CARS
# 三
# 鷹
# MITAKA
#
#
# 新
# 宿
# SHINJUKU
#
#
# 電
# 車
# が
# ま
# い
# り
# ま
# す
# 12
# 通
# 過
# し
# 各駅停車
#
#
# LOCAL
#
#
# 中央特快
#
#
# CHUO SPECIAL RAPID
#
#
# 回送
#
#
# OUT OF SERVICE
#
#
# JRマーク
#

