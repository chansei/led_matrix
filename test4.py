list1 = ['1330T', '1338T', '1326T', '1442T']
list2 = ['1338T', '1326T', '1442T', '1448T']

diff = list(set(list1) - set(list2))
print(diff)
