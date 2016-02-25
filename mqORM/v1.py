#!/usr/bin/env python


class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class ModelMetaclass(type):
    '''
        cls: 当前准备创建类的对象.
        name: 类的名字, 在这里name=User
        bases: 类继承的父类集合.(Model, )
        attrs: 类的方法集合.{key: value}

        在ModelMetaclass中, 一共做了如下几件事情:
        1. 排除掉对Model 类的修改.
        2. 在当前类(eg: User)中查找定义的类的所有属性,如果找到一个Field属性,就把它保存到一个__mappings__的dict中
           ,同时从类属性中删除Field属性,否则,容易造成运行时错误(实例的属性会遮盖类的同名属性).
        3. 把表名保存到__table__中,这里简化为表明默认为类名.
    '''

    def __new__(cls, name, bases, attrs):

        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    '''
       save(): 把一个实例保存到数据库中.因为有表名,属性到字段的映射和属性值的集合,就可以构造出Insert语句.
    '''

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        print(kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            # params.append('?')
            params.append(str(self[k]))
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) values (%s)" % (
            self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))


class User(Model):
    '''
       如果子类定义了自己的__init__构造方法函数,当子类的实例对象被创建时,子类只会执行自己的__init__
       方法函数,如果子类未定义自己的构造方法函数,会沿着搜索树找到父类的构造方法函数去执行父类里的构造方
       法函数.
       如果子类定义了自己的构造方法函数,如果子类的构造方法函数内没有主动调用父类的构造方法函数,那父类
       的实例变量再子类不会在刚刚创建子类实例对象时出现了.
    '''
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


if __name__ == "__main__":
    '''
       当用户定义一个class User(Model)时,Python解释器首先在当前类User的定义中查找metaclass, 如果
       没有找到,就继续在父类Model中查找metaclass,找到了,就使用Model中定义的metaclass的ModelMetaclass
       来创建User类,也就是说metaclass可以隐式地继承到子类,但子类自己却感觉不到.
    '''
    u = User(
        id=12345,
        name="Michael",
        email="test@test.org",
        password="my-pwd")
    u.save()
