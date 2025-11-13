from random import randint
#引入库时会执行一遍py文件，所以需要确保文件里没有无条件运行的代码
from 判断中位数 import Generated_List

list_ = Generated_List(randint(1,50),randint(1,100),randint(1,100))
print(f"list == {list_}")

a_,b_ = sum(list_),len(list_)

print(f"列表求和 == {a_:.2f}")
print(f"元素个数 == {b_}")

print(f"平均数 == {(a_/b_):.2f}")