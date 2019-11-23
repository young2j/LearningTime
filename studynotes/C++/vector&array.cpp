#include <iostream>
#include <vector>
#include <array>
int main()
{
	using namespace std;
	// c/c++ original array
	double arr1[4] = {1.2,2.4,3.6,4.8}; //存储于栈中
	//c++98 STL
	vector<double> arr2(4);//使用new和delete管理内存，存储于堆
	arr2[0] = 1.2;
	arr2[1] = 2.4;
	arr2[2] = 3.6;
	arr2[3] = 4.8;
	//c++11 
	array<double,4> arr3 = {1.2,2.4,3.6,4.8}; //长度固定
	array<double,4> arr4;
	arr4 = arr3 ;

	cout << "arr4[-2] = " << arr4[-2] << endl; //不安全,会出错
	cout << "arr4.at(2) = " << arr4.at(2) << endl;
}
