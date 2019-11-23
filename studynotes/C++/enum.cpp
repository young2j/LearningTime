#include <iostream>
using namespace std;

enum e1 {red,blue,black,white,green}; //分别对应{0，1，2，3，4}
e1 enumer = blue; //yes
/*
e1 enumer = 2+blue; //yes
int color = blue; //yes
e1 enumer = red+blue; //no
e1 enumer = 1; //no
e1 enumer = e1(1); //yes强制类型转换
*/

enum bits
{
	one=1,
	two=2,
	four = 4,
	eight=8
}; //显示设置枚举量的值{1,2,4,8}

enum bigstep
{
	first,
	second=100,
	third
}; //显示设置一些枚举值{0,100,101},后面的比前面的大1

enum equalstep
{
	_1st,
	_2nd=0,
	_3rd,
	_4th=1
}; //设置相同的枚举值{0,0,1,1}

int main()
{
	cout << "----枚举的范围----" << endl
	     << "上限：大于最大值的 2的幂-1" << endl
	     << "下限：大于0为0，小于0时为小于最小值的 -(2的幂-1)" << endl;
	cout << "例如： " << endl
		 << "{1,2,3,4}的上下限为  [0,2^3-1] = [0,7]" << endl
		 << "{-6,2,4,8}的上下限为  [-(2^3-1),(2^4-1)] = [-7,15]" << endl;

}