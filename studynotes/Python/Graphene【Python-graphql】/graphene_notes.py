# [graphene] https: // docs.graphene-python.org/en/latest/quickstart/

# ===================a simple example============================================
from graphene import ObjectType, Field, Schema
from graphene import ObjectType, String
from graphene import ObjectType, String, Field, Schema
from collections import namedtuple
import graphene
from graphene import ObjectType,String,Schema

class Query(ObjectType):
    hello = String(name=String(default_value='stranger'))
    goodbye = String()

    def resolve_hello(root,info,name):
        return f'Hello {name}!'
    
    def resolve_goodbye(root,info):
        return 'See ya!'

schema = Schema(Query)


result = schema.execute(
    '''
    {
        hello
        goodbye
    }
    '''
)

print(result.data['hello'])


#===================Types Reference====================
#----------Schema------------
'''
 Schema:defines the types and relationship between Fields
          by supplying the root ObjectType of each operation.
# Query:fetches data
# Mutation:changes data and retrieve the changes
# Subscription:sends changes to clients in real time
'''
schema = Schema (
    query=MyRootQuery, 
    mutation=MyRootMutation,
    subscription=MyRootSubscription,
    types=[SomeUnknowObjectType], # 一些Schema无法理解的ObjectType放这里
    auto_camelcase=False, #控制自动转换命名方式
)

#--------------
'''
默认情况下下划线字段名会被自动转换为驼峰式命名，除非用name参数指定
'''
class Person(ObjectType):
    last_name = String() # lastName
    other_name = String(name='_other_name') # _other_name


#---------Scalars----------
'''
graphene.String
graphene.Int
graphene.Float
graphene.Boolean
graphene.ID
graphene.types.datetime.Date
graphene.types.datetime.Time
graphene.types.json.JSONString
'''
# All Scalar types accept the following arguments.
class ModelMap(ObjectType):
    field_name = String(
                        name,
                        description,
                        required,
                        deprecation_reason,
                        default_value
                    )
    # mount scalar with params                    
    mount_field = graphene.Field(graphene.String, to=graphene.String())
    # Is equivalent to:
    mount_field_ = graphene.Field(graphene.String, to=graphene.Argument(graphene.String))

#------NonNull and List------
class ModelMap(ObjectType):
    non_null_field = graphene.NonNull(graphene.String)
    #equivalent to
    required_field = graphene.String(required=True)

    list_fields = graphene.List(graphene.String)
    non_null_list_fields = graphene.List(graphene.NonNull(graphene.String))

# SDL
#  type ModelMap {
#      nonNullField:String!
#      nonNullListFields:[String!]
#  }

#------------ObjectType---------
class PersonMap(ObjectType):
    first_name = String() # use default resolver
    last_name = String() # use default resolver
    full_name=String()

    def resolve_full_name(parent,info):
        # parent:
            # 指向父对象PersonMap
        # info:
            #引用有关当前GraphQL查询执行的元信息（字段，架构，已解析的查询等）
            #访问每个请求context，可用于存储用户身份验证，数据加载器实例或任何其他可用于解决查询的内容。
        return f"{parent.first_name} {parent.last_name}" 

# SDL
# type PersonMap{
#   firstName:String,
#   lastName:String,
#   fullName:String
# }        


#resolver
# 所有解析器方法都被隐式地视为静态方法。这意味着，解析器的第一个参数永远不会是self
# return 类型是dict则按key匹配，为其他类型则按参数名匹配
PersonValueObject = namedtuple('Person', ['first_name', 'last_name'])

class Person(ObjectType):
    first_name = String()
    last_name = String()

class Query(ObjectType):
    me = Field(Person)
    my_best_friend = Field(Person)

    def resolve_me(parent, info):
        # always pass an object for `me` field
        return PersonValueObject(first_name='Luke', last_name='Skywalker')

    def resolve_my_best_friend(parent, info):
        # always pass a dictionary for `my_best_fiend_field`
        return {"first_name": "R2", "last_name": "D2"}

schema = Schema(query=Query)
result = schema.execute('''
    {
        me { firstName lastName }
        myBestFriend { firstName lastName }
    }
''')

# default arguments
class Query(ObjectType):
    hello = String(required=True, name=String())

    def resolve_hello(parent, info, **kwargs):
        name = kwargs.get('name', 'World')
        return f'Hello, {name}!'

    def resolve_hello(parent, info, name='World'):
        return f'Hello, {name}!'


class Query(ObjectType):
    hello = String(
        required=True,
        name=String(default_value='World')
    )

    def resolve_hello(parent, info, name):
        return f'Hello, {name}!'


# meta class 
class MyGraphQlSong(ObjectType):
    class Meta:
        name = 'Song'
        description = 'But if we set the description in Meta, this value is used instead'
        # specifies the GraphQL Interfaces that this Object implements.
        interfaces = (Node, )
        # helps Graphene resolve ambiguous types such as interfaces or Unions.
        possible_types = (Song, )


#---------------Enum------------------
# You can create an Enum using classes:
class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


# But also using instances of Enum:
Episode = graphene.Enum(
    'Episode', [('NEWHOPE', 4), ('EMPIRE', 5), ('JEDI', 6)])

#--------interfaces---------------
'''
# 当有多个ObjectType具有共同属性时，可以使用接口简化工作
# 接口必须被ObjectType类实现(impliments),且ObjectType类必须明确包含接口类定义的属性或字段
# 当需要返回一个Object或者不同的Object集合，接口就很有用

when error:
 "Abstract type Character must resolve to an Object 
   type at runtime for field Query.hero ..."
reason:
  Graphene doesn’t have enough information to convert 
  the data object into a Graphene type needed to resolve the Interface
solve: @classmethod
'''
class Character(graphene.Interface):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    friends = graphene.List(lambda: Character)
    # @classmethod
    # def resolve_type(cls,isinstance,info):
    #     if isinstance.type=='Human':
    #         return Human
    #     return Monster

class Human(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)
    height = graphene.Float()

class Monster(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)
    crawler = graphene.Boolean(default_value=True)

class Query(graphene.ObjectType):
    hero = graphene.Field(
                        Character,
                        required=True,
                        has_crawler=graphene.Boolean(required=True)
                        )
    def resolve_hero(parent,info,has_crawler):
        if has_crawler:
            return get_monster(name='big monster')
        return get_human(name='oh baby')

schema = graphene.Schema(query=Query,types=[Human,Monster])


# SDL
# interface Character{
#     id:ID!
#     name:String!
#     friends:[Character]
# }
# type Human implements Character{
#     id:ID!
#     name:String!
#     friends:[Character]
#     height:String
# }
# type Monster implements Character{
#     id:ID!
#     name:String!
#     friends:[Character]
#     crawler:Boolean
# }
# query getHero($hasCrawler:Boolean!){
#     hero(hasCrawler:$hasCrawler){
#         __typename #Human/Monster
#         name
#         ...on Human{
#             height
#         }
#         ... on Monster{
#             hasCrawler
#         }
#     }
# }

#--------------Union-------------------
# 联合类：仅仅是返回多个不同类的集合，不需要像接口一样的公共字段

class Human(graphene.ObjectType):
    ...
class Monster(graphene.ObjectType):
    ...
class Others(graphene.ObjectType):
    ...

class SearchResult(graphene.Union):
    class Meta:
        types = (Human,Monster,Others)

#SDL
# type Human{}
# type Monster{}
# type Others{}
# union SearchResult = Human|Monster|Others

#---------Mutation-----------
class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
   
    # output fields
    ok = graphene.Boolean() 
    person = graphene.Field(lambda: Person)

    # mutate is the function that will be applied once the mutation is called.
    def mutate(root,info,name):
        person = Person(name=name)
        ok = True
        return CreatePerson(person=person,ok=ok)

# your Schema
class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()

class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()

class Query(graphene.ObjectType):
    person = graphene.Field(Person)

schema = graphene.Schema(query=Query,mutation=MyMutations)

schema.execute('''
    mutation myMutation{
        createPerson(name:"Peter"){
            person{
                name
            }
            ok
        }
    }

''')

# InputObjectTypes 
# 输入多个参数
class PersonInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    age = graphene.Int(required=True)

class CreatePerson(graphene.Mutation):
    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(Person)        
    @staticmethod
    def mutate(root,info,person_data=None):
        person = Person(
            name = person_data.name,
            age = person_data.age
        )
        return CreatePerson(person=person)

schema.execute(
    '''
    mutation myMutation{
        createPerson(personData:{name:"Peter",age:24}){
            person {
                name,
                age
            }
        }
    }
    '''
)

# complex input data
class LatLngInput(graphene.InputObjectType):
    lat = graphene.Float()
    lng = graphene.Float()

class LocationInput(graphene.InputObjectType):
    name = graphene.String()
    latlng = graphene.InputField(LatLngInput)

# output type
class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    Output = Person

    def mutate(root, info, name):
        return Person(name=name)

schema.execute(
    '''
    mutation myFirstMutation {
        createPerson(name:"Peter") {
            name
            __typename
        }
    }
    '''
)
#===================Execution====================
#----------Query-------------
# query via context
class Query(ObjectType):
    name = String()

    def resolve_name(root, info):
        return info.context.get('name')


schema = Schema(Query)
result = schema.execute('{ name }', context={'name': 'Syrus'})
assert result.data['name'] == 'Syrus'

# query via variables
class Query(ObjectType):
    user = Field(User, id=ID(required=True))

    def resolve_user(root, info, id):
        return get_user_by_id(id)

schema = Schema(Query)
result = schema.execute(
    '''
      query getUser($id: ID) {
        user(id: $id) {
          id
          firstName
          lastName
        }
      }
    ''',
    variables={'id': 12},
)

#query via root value
# Value used for Parent Value Object(parent) in root queries and mutations can be overridden using root parameter.

class Query(ObjectType):
    me = Field(User)

    def resolve_user(root, info):
        return {'id': root.id, 'firstName': root.name}


schema = Schema(Query)
user_root = User(id=12, name='bob'}
result = schema.execute(
    '''
    query getUser {
        user {
            id
            firstName
            lastName
        }
    }
    ''',
    root=user_root
)

# query via operation name,
# operation_name used to indicate which operation should be executed.
class Query(ObjectType):
    me = Field(User)

    def resolve_user(root, info):
        return get_user_by_id(12)

schema = Schema(Query)
query_string = '''
    query getUserWithFirstName {
        user {
            id
            firstName
            lastName
        }
    }
    query getUserWithFullName {
        user {
            id
            fullName
        }
    }
'''
result = schema.execute(
    query_string,
    operation_name='getUserWithFullName'
)

#---------Middleware----------
# class-based middleware

class AuthorizationMiddleware(object):
    def resolve(next, root, info, **args):
        if info.field_name == 'user':
            return None
        return next(root, info, **args)

result = schema.execute('THE QUERY', middleware=[AuthorizationMiddleware()])

#function middleware

def timing_middleware(next, root, info, **args):
    start = time.time()
    return_value = next(root, info, **args)
    duration = time.time() - start
    logger.debug("{parent_type}.{field_name}: {duration} ms".format(
        parent_type=root._meta.name if root and hasattr(root, '_meta') else '',
        field_name=info.field_name,
        duration=round(duration * 1000, 2)
    ))
    return return_value


result = schema.execute('THE QUERY', middleware=[timing_middleware])

#------DataLoader---------
from promise import Promise
from promise.dataloader import DataLoader
# batching
class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        return Promise.resolve([get_user(id=key) for key in keys])

user_loader = UserLoader()
user_loader.load(1).then(lambda user: user_loader.load(user.best_friend_id))
user_loader.load(2).then(lambda user: user_loader.load(user.best_friend_id))


class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        users = {user.id: user for user in User.objects.filter(id__in=keys)}
        return Promise.resolve([users.get(user_id) for user_id in keys])


# Using with Graphene
# {
#     me {
#         name
#         bestFriend {
#             name
#         }
#         friends(first: 5) {
#             name
#             bestFriend {
#                 name
#             }
#         }
#     }
# }
class User(graphene.ObjectType):
    name = graphene.String()
    best_friend = graphene.Field(lambda: User)
    friends = graphene.List(lambda: User)

    def resolve_best_friend(root, info):
        return user_loader.load(root.best_friend_id)

    def resolve_friends(root, info):
        return user_loader.load_many(root.friend_ids)

# file upload
# $pip install graphene-file-upload
from graphene_file_upload.scalars import Upload

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file
        return UploadMutation(success=True)
