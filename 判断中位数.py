from random import randint,uniform

#定义函数_生成值随机的从小到大排序的列表
def Generated_List(long,min_,max_):
    a = [randint,uniform]
    list_ = []
    #range函数结束值不包括自身，所以需要+1表示真实值
    for i in range(1,long+1,1):
        #确保randint函数的最小值<最大值
        min_,max_ = min(min_,max_),max(min_,max_)
        list_.append(a[randint(0,1)](min_,max_))
    return list_

def Median(list_):

    long = len(list_)
    print(f"元素个数 == {long}")
    len_ = long % 2

    #判断列表为 奇/偶 数
    if long == 1:
        #长度为1时直接取值
        print("奇数")
        print("索引值 == -1")
        print(f"中位数 == {(list_[-1]):.2f}")
    elif len_ == 1:
        print("奇数")
        #长度为奇数时取中间值
        a = int((long+1)/2)
        print(f"索引值 == {a-1}")
        a = list_[a-1]
        print(f"中位数 == {a:.2f}")
    elif len_ == 0:
        print("偶数")
        #长度为偶数时取两个中位值的平均数
        a = int(long/2)
        b = int((long/2)+1)
        print(f"索引值 == {a-1} , {b-1}")
        a,b = list_[a-1],list_[b-1]
        print(f"偶数中位值 == {a:.2f} + {b:.2f}")
        c = (a+b)/2
        print(f"中位数 == {c:.2f}")

#防止作为库被调用时出现无条件运行的情况
if __name__ == "__main__":
    #可自定义列表
    list_ = Generated_List(randint(1,50),randint(1,100),randint(1,100))
    list_ = sorted(list_,key=lambda x:x,reverse=False)
    print(f"list == {list_}")
    Median(list_)