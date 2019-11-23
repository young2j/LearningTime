# include <iostream>
# include <vector>
# include <deque>
using namespace std;

//vector.clear()
//vector.empty() ---bool
//vector.reserve(number) ---增加内存空间，以避免频繁重新分配内存

template <typename T>
void displayVector(const vector<T>& intVec)
{
	for(auto element = intVec.cbegin(); element!=intVec.cend();++element)
		cout << *element << ',' ;
	cout << endl;
}

template<typename T>
void displayDeque(const deque<T>& deque)
{
	for(auto element = deque.cbegin(); element!=deque.cend();++element)
		cout << *element << ',' ;
	cout << endl;
}

int main()
{
	//初始化vector
	vector<int> intVec1{2019,5,25};
	vector<int> intVec2(2); //2个int,默认2个0
	vector<int> intVec3(3,666); //3个666
	vector<int> intVec4(intVec3); //=intVec3
	vector<int> intVec5(intVec4.begin(),intVec4.begin()+5); //使用迭代器初始化为intVec4的前5个元素
	
	//插入insert元素
	intVec2.push_back(888);//末尾插入
	intVec2.push_back(999);
	cout << "intVec2 has " << intVec2.size() <<" elements: " << endl; //注意是4个，不是2个
	displayVector(intVec2);

	intVec2.insert(intVec2.begin(),111);//开头插入111
	intVec2.insert(intVec2.end()-2,2,666); //在倒数第二个位置前插入2个666
	intVec2.insert(intVec2.begin()+1,intVec3.begin(),intVec3.end()); //在第二个位置插入intVect3
	cout << "插入元素后intVec2 has " << intVec2.size() <<" elements" << endl;
	displayVector(intVec2);

	//访问vector中的元素
	cout << endl;
	intVec2[4] = 6868; //改变元素值
	
	for(size_t i=0;i<intVec2.size();i++) //数组语法
	{

		cout << "intVec2[" << i << "]=" ;
		//cout <<intVec2[i] <<endl; 
		cout << intVec2.at(i) << endl; //成员函数at在运行阶段会检查容器的大小，越界时会抛出异常
	}

	cout<<endl;
	vector<int>::const_iterator element = intVec2.cbegin(); //指针语法,也可用for实现(见displayVector)
	while(element!=intVec2.cend())
	{
		size_t elementPos = distance(intVec2.cbegin(),element);
		cout << "intVec2[" << elementPos <<"]=" << *element << endl;
		++ element;
	}

	//删除vector中的元素
	cout << endl;
	cout << "intVec2 has " << intVec2.size() << " elements:" << endl;
	displayVector(intVec2);
	intVec2.pop_back();
	intVec2.pop_back();
	cout << "after pop_back() twice, intVec2 has " << intVec2.size() << " elements:" << endl;
	displayVector(intVec2);

	//deque示例
	cout << endl;
	deque<float> floatDeque {0};
	floatDeque.push_back(1);
	floatDeque.push_front(1);
	cout << "floatDeque has " << floatDeque.size() << " elements:" <<endl;
	displayDeque(floatDeque);

	floatDeque.pop_back();
	floatDeque.pop_front();
	cout << "after pop_back/front,floatDeque has " << floatDeque.size() << " elements:" <<endl;
	displayDeque(floatDeque);


	return 0;
}