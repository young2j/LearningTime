#include <iostream>
using namespace std;

union one4all 
{
	int int_val;
	long long_val;
	double double_val;
};

struct  structunion
{
	string brand;
	int type;
	union id
	{
		long id_num;
		char id_char[20];
	}id_val;
};

int main()
{
	one4all one4;
	one4.int_val = 5;
	cout << one4.int_val << endl;
	one4.double_val = 5.01;
	cout << one4.double_val << endl;

	structunion custom = 
	{
		"lv",
		1,
		id_val
	};
	
	if (custom.type==1)
		cin >> custom.id_val.id_num;
	else
		cin >> custom.id_val.id_char;
}

