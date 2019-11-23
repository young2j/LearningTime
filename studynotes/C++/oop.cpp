# include <iostream>
# include <string>
# include <string.h>
using namespace std;

class Human
{
public:
	string name;
private:
	int age;
//构造函数：与类同名,创建对象时被调用。
public:
	Human() //default constructor
	{
		name = "无名氏";
		age = 888;
		cout<<"Here's default constructor." << endl;
	}
	Human(string Name,int Age=0)//reloaded constructor
		//：name(Name),age(Age) //初始化列表
	{
		name = Name;
		age = Age;
		cout << "Here's reloaded constructor." << endl;
	}

public:
	int GetAge()
	{
		if (age>=30)
			return age-2;
		else
			return age;
	}

	void SetAge(int humanAge)
	{
		if (humanAge>0)
			age = humanAge;
	}
};


class MyString
//类包含原始指针成员(char*等)时，务必编写复制构造函数和复制赋值运算符；
//编写复制构造函数时，务必将接受源对象的参数声明为const引用；
//声明构造函数时，务必考虑使用explicit，以避免隐式转换；
//务必将类成员声明为std::string类和智能指针类，他们实现了复制构造函数，可减少工作量；
// 除非万不得已，不要将类成员声明为原始指针。
{
private:
	char* buffer;
public:
	MyString(const char* initString)
	{
		if(initString!=NULL)
		{
			buffer = new char[strlen(initString)+1];
			strcpy(buffer,initString);
		}
		else
			buffer = NULL;
	}
	MyString(const MyString& source) //复制构造函数,保证深复制
	//复制构造函数的参数必须按引用传递，否则复制构造函数将不断调用自己，直至内存耗尽。
	{	
		buffer = NULL;
		if (source.buffer!=NULL)
		{
			buffer = new char[strlen(source.buffer)+1];
			strcpy(buffer,source.buffer);
		}
	}
	~MyString() //析构函数，在对象被销毁时自动调用
	{
		cout << "Invoking destructor,cleaning up" << endl;
		if(buffer!=NULL)
			delete[] buffer;
	}

	int GetLength()
	{
		return strlen(buffer);
	}
	const char* GetString()
	{
		return buffer;
	}
};

void UseMyString(MyString str)
{
	cout << "The length of " << str.GetString() << " is " << str.GetLength() << endl;
}


int main()
{
	Human firstMan;
	firstMan.name = "Adam";
	firstMan.SetAge(30);
	
	cout<<"I am " + firstMan.name << " and am ";
	cout<< firstMan.GetAge() <<" years old." << endl;

	Human firstWoman("666",668);
	//firstWoman.name = "Rose";
	//firstWoman.SetAge(28);
	cout <<"I am " + firstWoman.name << " and am ";
	cout << firstWoman.GetAge() <<" years old." << endl;

	Human God("God");
	cout << "I am " + God.name << " and am " << God.GetAge() << " years old." << endl;

	cout<<"----------------------------------------------------"<<endl;
	MyString sayHello("Hello world"); //实例化调用一次构造函数
	cout << "The length of \"" << sayHello.GetString() << "\" is " << sayHello.GetLength() << endl;

	UseMyString(sayHello); //深复制，完毕时调用一次析构函数;main()结束时会再调用一次析构函数.

	return 0;
} 