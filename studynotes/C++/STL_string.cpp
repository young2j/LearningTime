#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

//为了更好地支持中文和日文，应使用wstring.
int main()
{
	/*---------------创建(初始化)字符串---------------------*/
	const char* cstring = "hello string";
	cout << "c风格字符串:" << cstring << endl;
	
	string cppstring(cstring); //constructor
	cout << "STL::string类的构造器创建字符串："<<cppstring<<endl;
	string cppstring_ = "hello string";

	string cppstring5(cstring,5); //初始化前5个字符串
	cout << "可初始化指定字符个数(cstring,5)：" << cppstring5 << endl;

	string cppstringRepeat(10,'R'); //初始化包含10个"R"
	cout <<"可初始化字符串包含指定重复个数的字符：" << cppstringRepeat <<endl;

	cout << endl;
	/*-----------------访问字符串内容----------------------*/
	const char* cstr = cppstring.c_str(); //string 成员函数c_str()获得c风格字符串
	cout << "通过string.c_str()可获得c风格字符串:" << cstr << endl;

	for (size_t i=0;i<cppstring.length();i++) //通过数组下标[]的形式
	{
		cout<< "cppstring[" << i << "] =" << cppstring[i] << endl;
	}
	
	cout << endl;
	string::iterator iter; //通过迭代器的形式
	//string::const_iterator iter;
	int offset = 0;
	for(auto iter=cppstring.cbegin();iter!=cppstring.cend();++iter)
	{
		cout << "cppstring[" << offset++ << "] =" << *iter << endl;
	} //cppstring.begin()\cppstring.end() 一样的

	
	cout << endl;
	/*----------------拼接字符串--------------------------*/
	//使用运算符+=
	string s1("cppstring");
	const char* s2 = " is a instance of STL::string";

	s1+=s2;
	cout << s1 << endl;

	const char* s3 = " and can append(c_style_string)";
	s1.append(s3);
	cout << s1 << endl;

	cout<<endl;
	/*-------------查找字符串内容-----------------------*/
	/* string.find()
	 * string.find_first_of()
	 * string.find_first_not_of()
	 * string.find_last_of()
	 * string.find_last_not_of()
	 * string.clear()
	*/
	//查找首个
	string str = "Today is a nice day and also sunny day!";
	size_t charPos = str.find("day",0);//从0的位置开始查找day
	if (charPos!=string::npos) //string::npos值为-1,find无结果时返回-1
		cout << "First 'day' at pos " << charPos << endl;
	else
		cout << "'day' is not found." << endl;

	//查找全部
	while(charPos!=string::npos)
	{
		cout << "Find 'day' at pos "  << charPos << endl;
		size_t posOffset = charPos+1;
		charPos = str.find("day",posOffset);
	}

	cout<<endl;
	/*--------------截短(erase)字符串-----------------*/
	string sampleStr("emm...,I don't like you!");
	cout << sampleStr;
	sampleStr.erase(0,7); //注意：[0,7)
	cout << " 'erase(0,7)' is: " << sampleStr << endl;

	int dontPos = sampleStr.find("don't",0);
	if (dontPos!=string::npos)
		sampleStr.erase(dontPos,dontPos+4);
	else
		sampleStr.erase(sampleStr.begin(),sampleStr.end());
	cout << sampleStr << endl;

	/*-------------字符串反转-----------------------*/
	cout << "reverse \"" + sampleStr + "\" is ";
	reverse(sampleStr.begin(),sampleStr.end());
	cout << "\"" + sampleStr + "\"" << endl;

	/*--------------转换大小写---------------------*/
	cout << endl;
	string swapCaseStr = "I LiKE You!";
	transform(swapCaseStr.begin(),swapCaseStr.end(),swapCaseStr.begin(),::toupper); //转为大写
	cout << swapCaseStr << endl;
	transform(swapCaseStr.begin(),swapCaseStr.end(),swapCaseStr.begin(),::tolower); //转为小写
	cout << swapCaseStr << endl;

	/*-----------c++14 引入""s操作符---------------*/
	cout <<"this is \0 traditional string" << endl; //被空白字符截断
	cout <<"this is \0 c++14 string "s << endl; //包含空白字符

	return 0;
}