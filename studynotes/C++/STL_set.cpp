# include<iostream>
# include<typeinfo>
# include<string>
# include<set> 
//为了实现快速搜索，set将把新元素同内部树中得其他元素比较，进而将其放在其他位置，因此位于set中特定位置得元素不能替换为值不同得新元素。
//set插入时排序，默认使用谓词std::less进行升序排列。
# include<unordered_set>
//使用散列函数计算处一个唯一的索引，再根据该索引决定将元素放到哪个桶bucket中。

using namespace std;

//排序
template <typename T>
struct sortDescending //等价于greater<int>
{
	bool operator()(const T& lhs,const T& rhs) const
	{
		return (lhs>rhs);
	}
};

//显示
template<typename T>
void display(const T& container)
{
	for(auto element = container.cbegin();element!=container.cend();++element)
		cout<<*element<<' ';
	cout<<endl;
}

template<typename T>
void displayUnorderedSet(const T& container)
{
	for(auto element = container.cbegin();element!=container.cend();++element)
		cout<<*element<<' ';
	cout<<endl;
	cout <<"size:" << container.size()<<endl;
	cout << "bucket_count:"<< container.bucket_count() << endl;
	cout << "max_load_factor:"<<container.max_load_factor() << endl;
	cout << "load_factor:"<<container.load_factor() << endl;
	cout << endl;
}

typedef multiset<int> MINTSET;


// 结构体
struct contactItems
{
	string name;
	string phone;
	string displayAs;
	contactItems(const string& Inputname,const string& inputPhone)//constructor
	{
		name = Inputname;
		phone = inputPhone;
		displayAs = name+": "+ phone;
	}

	bool operator==(const contactItems& itemToCompare) const //used to set::find()
	{
		return (itemToCompare.name==this->name);
	}

	bool operator<(const contactItems& itemToCompare) const // used to set::sort()
	{
		return (this->name < itemToCompare.name);
	}

	operator const char*() const //used to cout
	{
		return displayAs.c_str();
	}
};


int main()
{
	//实例化set
	set<int> intSet{20,-10,0,1,50};
	MINTSET mintSet{20,-10,0,1,50};
	set<int,sortDescending<int>> intSetDesc(intSet.cbegin(),intSet.cend());
	multiset<int,greater<int>> mintSetDesc(mintSet.cbegin(),mintSet.cend());
	set<int> intSet2(intSet);
	multiset<int> mintSet2;

	//插入元素insert
	intSet.insert(1);
	mintSet.insert(1);
	intSetDesc.insert(1);
	mintSetDesc.insert(1);

	cout<<"intSet:has "<< intSet.count(1) << " element 1" << endl;
	display(intSet);
	cout<<"multiIntSet: has "<< mintSet.count(1) <<" element 1" << endl;
	display(mintSet);
	cout<<endl<<"intSetDesc:";
	display(intSetDesc);
	cout <<endl <<"multiIntSetDesc:";
	display(mintSetDesc);
	cout<<endl;


	//查找元素find
	auto efind = intSet.find(1);
	if (efind!=intSet.end())
		cout<<"element " << *efind << " found." <<endl;
	else
		cout << "element not found." << endl;

	//删除元素erase
	intSet.erase(20);
	if(efind!=intSet.end())
	{
		intSet.erase(efind);
		cout << "intSet erase 1:"<<endl;
		display(intSet);
	}
	else
		cout<<"element 20 not found to erase."<<endl;

	auto efind2 = intSet.find(0);
	if(efind2!=intSet.end())
		{
			intSet.erase(intSet.begin(),efind2); //含头不含尾
			cout<<"intSet erase start element to 0:" <<endl;
			display(intSet);
		}
	else
		cout<<"element 0 not found."<<endl;

	//set<struct>
	set<contactItems> setContacts;
	setContacts.insert(contactItems("Boss",""));
	setContacts.insert(contactItems("小明","18200921421"));
	setContacts.insert(contactItems("小李","18032423522"));
	setContacts.insert(contactItems("小王","17732339992"));
	setContacts.insert(contactItems("小杨","13223332455"));
	cout << "set<struct> :"<<endl;
	display(setContacts);

	//unordered_set
	unordered_set<int> unorderedSet{1,300,-1,989,-300,9};
	cout << "unorderedSet:"<<endl;
	displayUnorderedSet(unorderedSet);
	unorderedSet.insert(999);
	unorderedSet.insert(666);
	cout<< "unorderedSet after insert 999 and 666:" << endl;
	displayUnorderedSet(unorderedSet);

	auto efind3 = unorderedSet.find(300);
	if(efind3!=unorderedSet.end())
		cout << *efind3 << " found in set." << endl;
	else
		cout << *efind3 << "not found in set." << endl;

	return 0;
}  