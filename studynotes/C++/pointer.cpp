#include <iostream>
#include <cstring>
using namespace std;


void pointer()
{
/*
1.声明指针时必须指定指针指向的数据类型，不同类型使用的字节数不同;
2.指针在解除引用(*pointer)之前，一定要先初始化为一个确定的、适当的地址；
*/
	cout << "-----指针与解除引用-----" << endl
		<< "若var为变量，则 &var为变量的存储地址；" << endl
		<< "若var为指针(物理地址)，则 *var为指针的值。" << endl;
	int var = 6;
	int *p_var;
	p_var = &var;

	cout << "p_var = &var = " << p_var << endl
		<< "*p_var = "  << *p_var << endl;
	*p_var += 1;
	cout << "*p_var+1 = " << *p_var << endl;
}

void force_transform() 
{
	cout << "-----指针强制类型转换-----" << endl;
	int * p;
	// p = 0xB800000; NO
	p = (int *) 0xB800000;
	cout << "p = (int *) 0xB800000" << endl;
}

void pointer_new()
{
	/*
	1.new 分配的内存块与常规变量声明分配的内存块不同：常规变量存储在栈中，new从堆或自由存储区分配内存；
	2.使用delete释放内存，一定要配对使用new和delete，否则会发生内存泄漏；
	3只能用delete来释放new分配的内存，对空指针使用delete也是安全的；
	4.new 返回第一个元素的地址，并赋给指针;
	5.指针变量+1，增加的量等于指向类型的字节数；
	6.C++将数组名解释为数组第一个元素的地址；
	*/
	cout << "----new/delete创建和释放动态数组-------" << endl;
	int *p_int = new int [3]; //称为数组的动态联编
	short *p_short = new short;
	delete p_short; //配对释放
	p_int[0] = 1;
	p_int[1] =2;
	p_int[2] =3;
	cout << "*p_int =p_int[0] =  " << *p_int << endl; //一开始指针指向第一个数组元素
	cout << "p_int[0] = " << p_int[0] << endl;
	p_int +=1; //指针移动4个字节(int)
	cout << "p_int[0] = " << p_int[0] << endl; //相当于指向下一个数组元素p_int[1]

	double arr[3] = {3,2,1}; //称为数组的静态联编
	double *pd = arr; //等价于
	double *pd_ = &arr[0];
	cout << "*pd= " << *pd << " = arr[0]= " << arr[0] << endl
		 << "*(pd+1)= " << *(pd+1) << " =arr[1]= " << arr[1] << endl ;
	cout << "数组长度sizeof(arr)=3x8= " << sizeof(arr) << endl
		 << "指针长度sizeof(pd)= " << sizeof(pd) << endl;

	delete [] p_int; //[]表明应释放整个数组，而不仅仅是指针指向的元素。
}

void pointer_string()
{
	cout << "------指针和字符串---------" << endl;
	char animal[10] = "bear";
	const char *bird = "googa"; //字符串字面量是常量，const意味着可以用bird访问字符串，但不能修改指向的内容
	char *p = animal; 
	cout << "animal= " << animal << endl; //打印字符串
	cout<< "(int *) animal = " << (int *) animal << endl; // 强制转换为另一种指针类型
	cout << "bird= " << bird << endl; //使用bird访问字符串
	cout << "p= " << p << endl; //向cout提供一个指针将打印地址，但指针类型是char*,将打印指向的字符串
	cout << "(int *) p= " << (int *) p << endl; //若要显示字符串地址，必须将指针强制转换为另一种指针类型

	strncpy(animal,"there is a bear",20); //将字符串赋值给char数组应使用strcpy/strncpy，而不是=
	cout << "strncpy: animal= " << animal << endl; 
}

void struct_new()
{
	cout << "-------使用new创建动态结构体--------" << endl;
	struct inflatable
		{
			char name[20];
			float volume;
			double price;
		};
	inflatable *p_struct = new inflatable;//创建动态结构体
	strcpy(p_struct->name,"babi");
	p_struct->volume = 2.22;
	p_struct->price = 5.5;
	cout << "name: " << p_struct->name << endl
		 << "volume: " << p_struct->volume << endl
		 << "price: " << p_struct->price << endl;
	cout << "(*p_struct).name = " << (*p_struct).name << endl;
	delete p_struct;
};

int main()
{
	pointer();
	force_transform();
	// pointer_new();
	pointer_string();
	struct_new();
}

