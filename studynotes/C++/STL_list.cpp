# include <iostream>
# include <list>
# include <forward_list>
# include <vector>
# include <string>
using namespace std;

template<typename T>
void display(const T& container)
{
	for (auto element=container.begin();element!=container.end();++element)
	{
		cout << *element << " ";
	}
	cout << endl;
}

bool sortDescending(const float& lhs,const float& rhs)
{
	return (lhs>rhs);
}




struct ContactItems
{
	string name;
	string phone;
	string displayAs;

	ContactItems(const string& conName,const string& conPhone)//constructor
	{
		name = conName;
		phone = conPhone;
		displayAs = name+": " + phone;
	}
	
	bool operator ==(const ContactItems& itemToCompare) const //used by list::remove()
	{
		return (itemToCompare.name==this->name);
	}

	bool operator < (const ContactItems& itemToCompare) const //used by list::sort()
	{
		return (this->name < itemToCompare.name);
	}

	operator const char*() const
	{
		return displayAs.c_str();
	}
};

bool sortByPhoneNumber(const ContactItems& item1,const ContactItems& item2)
{
	return (item1.phone<item2.phone);
}






int main()
{
	//初始化list
	list<int> intList{5,4,3,2,1};
	list<float> floatList(3,6.6);
	list<char> charList(10);

	vector<int> intVec(3,8);
	list<int> intListFromVec(intVec.cbegin(),intVec.cend());

	display(intList);
	display(floatList);
	display(charList);
	display(intListFromVec);

	//插入元素insert/push_back/push_front
	intList.push_back(0);
	intList.push_front(6);

	intList.insert(intList.begin(),7);
	intList.insert(intList.end(),2,0);
	intList.insert(intList.begin(),intVec.begin(),intVec.end()); //list.begin()不能+1；vector.begin()+1就可以？？？

	display(intList);

	//删除erase元素
	auto iter = intList.insert(intList.begin(),9);
	display(intList);
	intList.erase(iter);
	display(intList);

	intList.erase(intList.begin(),intList.end()); //同intList.clear()
	display(intList);
	if(intList.empty())
		cout<<"intList.empty():" << "true" << endl;

	//反转reverse和排序sort
	cout<< endl;
	floatList.insert(floatList.begin(),3,7.7);
	floatList.insert(floatList.end(),3,5.5);
	cout << "floatList is :" ;
	display(floatList);

	floatList.reverse();
	cout << "reverse floatList is: ";
	display(floatList);

	floatList.sort();
	cout << "sort floatList is: ";
	display(floatList);

	floatList.sort(sortDescending);
	cout << "sort floatList by descending is:" ;
	display(floatList);

	//list<struct> 示例
	cout << endl;
	list<ContactItems> contacts;
	contacts.push_back(ContactItems("小明","18200921421"));
	contacts.push_back(ContactItems("小李","18032423522"));
	contacts.push_back(ContactItems("小王","17732339992"));
	contacts.push_back(ContactItems("小杨","13223332455"));
	cout << "list<ContactItems> contacts is:" <<endl;
	display(contacts);

	contacts.sort();
	cout << "list<ContactItems> contacts sorted by name is:" << endl;
	display(contacts);

	contacts.sort(sortByPhoneNumber);
	cout << "list<ContactItems> contacts sorted by phone is: " <<endl;
	display(contacts);

	contacts.remove(ContactItems("小王",""));
	cout << "after removing '小王',list<ContactItems> contacts is:" << endl;
	display(contacts);

	//forward_list
	forward_list<int>  forwardList = { 5,4,3,2,1,1,1 };
	cout << endl << "forwardList contains:" ;
	display(forwardList);
	forwardList.push_front(6);
	forwardList.remove(1);
	cout << "after push_front(6) and remove(1),forwardList contains:";
	display(forwardList);
	
	return 0;
}