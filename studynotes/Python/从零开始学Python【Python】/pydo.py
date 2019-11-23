=====================猜字游戏=========================================
import random
num = random.randint(0, 100)
guess = 0
while True:
    num_input = input("请输入一个0到100的数字:")
    guess += 1
    if not num_input.isdigit():
        print("请输入数字")
    elif int(num_input) not in range(100):
        print("输入的数字必须介于0到100")
    else:
        if num == int(num_input):
            print("恭喜，猜对了！总共猜了%d次" % guess)
            break
        elif num > int(num_input):
            print("你输入的数字小了")
        elif num < int(num_input):
            print("你输入的数字大了")
        else:
            print("系统异常")

====================出行建议============================================
    def __init__(self,input_daytime):
        self.input_daytime = input_daytime
    def search_visibility(self):
        visible_level = 0
        if self.input_daytime =="daytime":
            visible_level = 2
        if self.input_daytime =="night":
            visible_level = 9
        return visible_level
    def search_temperature(self):
        temperature = 0
        if self.input_daytime == "daytime":
            temperature = 26
        if self.input_daytime == "night":
            temperature = 16
        return temperature
class OutAdvice(WeatherSearch):
    def __init__(self,input_daytime):
        WeatherSearch.__init__(self, input_daytime)
    def search_temperature(self):
        vehicle = ""
        if self.input_daytime == "daytime":
            vehicle = "bike"
        if self.input_daytime == "night":
            vehicle = "taxi"
        return vehicle
    def out_advice(self):
        visible_level = self.search_visibility()
        if visible_level == 2 :
            print("The weather is good,suitable for use %s."%self.search_temperature())
        elif visible_level == 9 :
            print("The weather is bad,you should use %s."%self.search_temperature())
        else :
            print("The weather is beyond my scope,I can not give you any advice")
got = OutAdvice("daytime")
got.out_advice()

=====================装饰器应用============================================
import time
user,passwd = 'alex','abc123'
def auth(auth_type):
    print("auth func:",auth_type)
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            print("wrapper func args:", *args, **kwargs)
            if auth_type == "local":
                username = input("Username:").strip()
                password = input("Password:").strip()
                if user == username and passwd == password:
                    print("\033[32;1mUser has passed authentication\033[0m")
                    res = func(*args, **kwargs)  # from home
                    print("---after authenticaion ")
                    return res
                else:
                    exit("\033[31;1mInvalid username or password\033[0m")
            elif auth_type == "ldap":
                print("搞毛线ldap,不会。。。。")

        return wrapper
    return outer_wrapper

def index():
    print("welcome to index page")
@auth(auth_type="local") # home = wrapper()
def home():
    print("welcome to home  page")
    return "from home"

@auth(auth_type="ldap")
def bbs():
    print("welcome to bbs  page")

index()
print(home()) #wrapper()
bbs()

====================购物列表====================================
product_list = [
    ('Iphone',5800),
    ('Mac Pro',9800),
    ('Bike',800),
    ('Watch',10600),
    ('Coffee',31),
    ('Alex Python',120),
]
shopping_list = []
salary = input("Input your salary:")
if salary.isdigit():
    salary = int(salary)
    while True:
        for index,item in enumerate(product_list):
            #print(product_list.index(item),item)
            print(index,item)
        user_choice = input("选择要买嘛？>>>:")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(product_list) and user_choice >=0:
                p_item = product_list[user_choice]
                if p_item[1] <= salary: #买的起
                    shopping_list.append(p_item)
                    salary -= p_item[1]
                    print("Added %s into shopping cart,your current balance is \033[31;1m%s\033[0m" %(p_item,salary) )
                else:
                    print("\033[41;1m你的余额只剩[%s]啦，还买个毛线\033[0m" % salary)
            else:
                print("product code [%s] is not exist!"% user_choice)
        elif user_choice == 'q':
            print("--------shopping list------")
            for p in shopping_list:
                print(p)
            print("Your current balance:",salary)
            exit()
        else:
            print("invalid option")

====================三级菜单=============================================
data = {
    '北京':{
        "昌平":{
            "沙河":["oldboy","test"],
            "天通苑":["链家地产","我爱我家"]
        },
        "朝阳":{
            "望京":["奔驰","陌陌"],
            "国贸":{"CICC","HP"},
            "东直门":{"Advent","飞信"},
        },
        "海淀":{},
    },
    '山东':{
        "德州":{},
        "青岛":{},
        "济南":{}
    },
    '广东':{
        "东莞":{},
        "常熟":{},
        "佛山":{},
    },
}
exit_flag = False

while not exit_flag:
    for i in data:
        print(i)
    choice = input("选择进入1>>:")
    if choice in data:
        while not exit_flag:
            for i2 in data[choice]:
                print("\t",i2)
            choice2 = input("选择进入2>>:")
            if choice2 in data[choice]:
                while not exit_flag:
                    for i3 in data[choice][choice2]:
                        print("\t\t", i3)
                    choice3 = input("选择进入3>>:")
                    if choice3 in data[choice][choice2]:
                        for i4 in data[choice][choice2][choice3]:
                            print("\t\t",i4)
                        choice4 = input("最后一层，按b返回>>:")
                        if choice4 == "b":
                            pass
                        elif choice4 == "q":
                            exit_flag = True
                    if choice3 == "b":
                        break
                    elif choice3 == "q":
                        exit_flag = True
            if choice2 == "b":
                break
            elif choice2 == "q":
                exit_flag = True

===================进度条=============================================
import sys,time

for i in range(20):
    sys.stdout.write("#")
    sys.stdout.flush() #写入后刷新内存
    time.sleep(0.1)

====================xml==============================================
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank updated="yes">5</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank updated="yes">69</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
===================configparser==================================
[DEFAULT]
ServerAliveInterval = 45
Compression = yes
CompressionLevel = 9
ForwardX11 = yes
 
[bitbucket.org]
User = hg
 
[topsecret.server.com]
Port = 50022
ForwardX11 = no

====================继承：学校系统================================
class School(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.students = []
        self.staffs = []
    def enroll(self, stu_obj):
        print("为学员%s 办理注册手续" % stu_obj.name)
        self.students.append(stu_obj)
    def hire(self, staff_obj):
        self.staffs.append(staff_obj)
        print("雇佣新员工%s" % staff_obj.name)

class SchoolMember(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def tell(self):
        pass

class Teacher(SchoolMember):
    def __init__(self, name, age, sex, salary, course):
        super(Teacher, self).__init__(name, age, sex)
        self.salary = salary
        self.course = course
    def tell(self):
        print('''
        ---- info of Teacher:%s ----
        Name:%s
        Age:%s
        Sex:%s
        Salary:%s
        Course:%s
        ''' % (self.name, self.name, self.age, self.sex, self.salary, self.course))
    def teach(self):
        print("%s is teaching course [%s]" % (self.name, self.course))

class Student(SchoolMember):
    def __init__(self, name, age, sex, stu_id, grade):
        super(Student, self).__init__(name, age, sex)
        self.stu_id = stu_id
        self.grade = grade
    def tell(self):
        print('''
        ---- info of Student:%s ----
        Name:%s
        Age:%s
        Sex:%s
        Stu_id:%s
        Grade:%s
        ''' % (self.name, self.name, self.age, self.sex, self.stu_id, self.grade))
    def pay_tuition(self, amount):
        print("%s has paid tution for $%s" % (self.name, amount))

school = School("老男孩IT", "沙河")

t1 = Teacher("Oldboy", 56, "MF", 200000, "Linux")
t2 = Teacher("Alex", 22, "M", 3000, "PythonDevOps")

s1 = Student("ChenRonghua", 36, "MF", 1001, "PythonDevOps")
s2 = Student("徐良伟", 19, "M", 1002, "Linux")

t1.tell()
s1.tell()
school.hire(t1)
school.enroll(s1)
school.enroll(s2)

print(school.students)
print(school.staffs)
school.staffs[0].teach()

for stu in school.students:
    stu.pay_tuition(5000)