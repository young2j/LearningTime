/* ------------------------------------------STL 容器------------------------------------------------------ */
/*
顺序容器：适用于插入、删除
                 优点                                                             缺点
std::vector      末尾插入数据时速度快；可像访问数组一样进行访问；                调整大小时影响性能；搜索时间与元素个数成正比；只能在末尾插入数据

std::deque       同vector；可在开头和末尾插入数据                              同vector；不需要支持reverse()

std::list        可在任何位置(开头、中间、结尾)插入删除数据，且时间固定           不能像数组那样根据索引随机访问元素；搜索时间与元素个数成正比；
                插入删除数据后，指向其他元素的迭代器仍有效。                     由于元素没有存储在连续的内存单元中，搜素速度比vector慢。

std::forward_list单向链表，只能向一个方向遍历                                    只能使用put_front()在开头插入元素


关联容器：适用于搜索、查找
                 优点                                                             缺点
std::set        存储不同的值，在插入元素时排序；                                插入速度比顺序容器慢，因为插入时会对元素排序
                搜索时间与元素个数的对数成正比，因此搜索速度比顺序容器快

std::unordered_set 存储不同的值，在插入元素时排序【c++11新增】                    元素未被严格排序，不能依赖于元素的相对位置
                搜素、插入和删除速度几乎不受元素个数的影响

std::multiset    可存储相同的值                                               插入速度比顺序容器慢，因为插入时会对元素排序

std::unordered_multiset 可存储相同的值，在插入元素时排序【c++11新增】             元素未被严格排序，不能依赖于元素的相对位置
                搜素、插入和删除速度几乎不受元素个数的影响

std::map         存储键值对，键唯一，插入时根据键排序                           插入速度比顺序容器慢，因为插入时会对元素排序
                搜索时间与元素个数的对数成正比，因此搜索速度比顺序容器快

std::unordered_map 存储键值对，键唯一，插入时根据键排序 【c++11新增】             元素未被严格排序，不适用于顺序很重要的情形
                搜素、插入和删除时间固定，不受容器长度影响

std::multimap    存储键值对，键可相同，插入时排序                              插入时排序，插入速度比顺序容器慢

std::unordered_multimap 存储键值对，键可相同，插入时排序                       元素未被严格排序，不适用于顺序很重要的情形
                搜素、插入和删除时间固定，不受容器长度影响
 */

/* ----------------------STL 容器适配器(container adapter)----------------------- */
/*
std::stack 栈 LIFO
std::queue  队列 FIFO
std::priority_queue 优先级队列，开头的优先级最高
 */

/* ----------------------STL 迭代器----------------------------------------------*/
//输入迭代器、输出迭代器、前向迭代器、双向迭代器、随机访问迭代器

/* ----------------------STL 算法------------------------------------------------*/
/*
 std::find()
 std::find_if()
 std::reverse()
 std::remove_if()
 std::transform()
*/

//example:在vector中查找元素及位置
# include <iostream>
# include <vector>
# include <algorithm>
using namespace std;

int main()
{
    vector<int> intArray;
    intArray.push_back(50);
    intArray.push_back(2991);
    intArray.push_back(23);
    intArray.push_back(9999);
    cout<< "The elements of intArray are:" << endl;
    vector<int>::iterator arrIter = intArray.begin(); //指针指向首元素
    while(arrIter!=intArray.end()) //intArray.end()指向最后一个元素的后面
    {
        cout<< *arrIter <<endl;
        ++arrIter;
    }

    vector<int>::iterator eFind = find(intArray.begin(),intArray.end(),23);
    if (eFind != intArray.end())
    {
        int ePos = distance(intArray.begin(),eFind);
        cout << "value  " << *eFind << " found in the vector at positon:" << ePos<<endl;
    }
    return 0;
}