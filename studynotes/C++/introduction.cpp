# include <iostream>
# include <cstring>
int main()
{
	using namespace std;
	cout << "-----输出字符-----\n";
	cout << 'A' << endl;
	cout.put('A') << endl;

	cout << "-----宽字符-----\n";
	wchar_t bob = L'P';
	wcout << L"tall" << endl;
	// char16_t ch16 = u"aa";
	// char32_t ch32 =U"aa";
	
	cout << "----控制小数位数-----n";
	double d = 1.237e8;
	cout << d;
	cout << fixed << endl;
	//cout.setf(ios_base::fixed,ios_base::floatfield);
	cout << "fixed:固定6位小数 " << d << endl;
	
	cout << "----类型强制转换-----\n";
	int sum = (int) 19.99 + (int) 1.88;
	//int sum = int (19.99) + int (1.88);
	int sum_ = static_cast<int> (19.99) + static_cast<int> (1.88);
	cout << "sum=" << sum << endl << "sum_=" << sum_ << endl;

	cout << "------创建数组--------\n";
	int intarr[3] = {32}; //可初始化部分元素，其余自动为0
	cout << "int intarr[3]为三个整形元素数组：" 
		 << intarr[0] << ","
		 << intarr[1] << ","
		 << intarr[2] << endl;

	cout << "------字符串-------\n";
	const int con = 12;
	char str[con] = "C++owboy";
	cout << "str[12] = \"C++owboy\" has " 
		 << strlen(str) 
		 << " letters and " 
		 << sizeof (str) << " bytes" << endl;
	str[3] = '\0';
	cout << "\'\\0\' 将把字符串str截断为：" << str << endl;

	cout << "-----getline()和get()的使用------\n";
	char name[con];
	cout << "input your name:\n";
	cin.getline(name,con); //读取不超过con-1个字符，结尾需为空字符占一个字符位
	cout << "your name is " << name << endl;
	// cin.get();
}