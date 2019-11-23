#include <iostream>
using namespace std;
struct info
{
	string name;
	float volume;
	double price;
	
} info_1,info_2; //创建结构的同时声明结构变量

/*创建结构的同时声明并初始化结构变量
struct info
{
	string name;
	float volume;
	double price;
	
} info_1 =
{
	"babiwawa",
	1.44,
	2.33
}; 
*/

int main()
{
	info product = 
	{
		"babi",
		1.88,
		2.99
	};
	cout << "product.name=" << product.name << endl;
	cout << "product.volume=" << product.volume << endl;
	cout << "product.price=" << product.price << endl;

	info_1 = product; //可以进行结构成员赋值
	cout << "info_1.name="  << info_1.name << endl;

	info structarr[2] = 
	{
		{"babi1",2.33,1.23},
		{"babi2",3.55,2.11}
	};
	cout << "structarr[1].name=" << structarr[1].name << endl;
}
