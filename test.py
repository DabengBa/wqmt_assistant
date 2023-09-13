from utils.functions import Getxy
import utils.adb as adb

# adb.connect()
# center=Getxy(tgt_pic="friend1", retry_enabled=False)
# if center is not None:
#     print(center.x, center.y)
#     center.click()
# else:
#     print("fail")




# center=Getxy(tgt_pic="friend1", retry_enabled=False)  
# if center is not None:  
#     print(center.x, center.y)  
#     center.click()  
# else:  
#     print("fail")


class MyClass:  
    def __init__(self):  
        self.x = 0  
        self.y = 0  
  
    def getxy(self):  
        # 在这里执行你的步骤  
        print("执行步骤...")  
  
        # 停止并返回None  
        return None  
  
# 使用这个类  
my_object = MyClass()  
result = my_object.getxy()  
print(my_object)

if result is not None:
    print(my_object)
    print("success")  
else:  
    print("fail")
