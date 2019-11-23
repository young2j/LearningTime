# include <iostream>
# include <string>
# include <cstring>
using namespace std;

int main()
{
	cout << "----C风格：strcpy()/strcat()/strlen()/strncpy()/strncat()------\n";
	char str1[20];
	char str2[20] = "my";
 
	strcpy(str1,str2) ;//将str2复制到str1，等同于str1 = str2
	cout << "strcpy(str1,str2): " << str1 << endl;
	strcat(str1,str2); //将str2追加到str1
	cout << "strcat(str1,str2): " << str1 << endl;
	cout << "strlen(str1): " << strlen(str1)<< endl;

	cout << "----------------------c++------------------\n";
	string str3;
	string str4 = "my";
	str3 = str4;
	cout << "str3=" << str3 << endl;
	str3 += str4;
	cout << "str3+str4 = " << str3 << endl;
	cout << "str3.size()=" << str3.size() << endl;

	/*
	cout << "--------string io ------------\n";
	char charstr[20];
	string str;
	cin.getline(charstr,20); //getline是类方法,cin是istream类成员
	getline(cin,str); //这里getline 不是类方法，因为在引入string类之前c++就有了istream类
	*/

	cout << "-------原始字符串R\"(...)\"--------\n";
	cout << R"(WHO PA WHO! \n she roared)" << endl; //默认()为定界符
	cout << R"+*("(WHO PA WHO!)",she roared)+*" << endl; //+*()+*替代定界符，为了输出()
}