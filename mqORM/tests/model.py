#!/usr/bin/env python

from mqORM import Model
from mqORM.fields import StringField, IntegerField


class User(Model):
    '''
       如果子类定义了自己的__init__构造方法函数,当子类的实例对象被创建时,子类只会执行自己的__init__
       方法函数,如果子类未定义自己的构造方法函数,会沿着搜索树找到父类的构造方法函数去执行父类里的构造方
       法函数.
       如果子类定义了自己的构造方法函数,如果子类的构造方法函数内没有主动调用父类的构造方法函数,那父类
       的实例变量再子类不会在刚刚创建子类实例对象时出现了.
    '''
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


class Db(Model):
    name = StringField('name')
    email = StringField('email')
    password = StringField('password')

if __name__ == "__main__":
    '''
       当用户定义一个class User(Model)时,Python解释器首先在当前类User的定义中查找metaclass, 如果
       没有找到,就继续在父类Model中查找metaclass,找到了,就使用Model中定义的metaclass的ModelMetaclass
       来创建User类,也就是说metaclass可以隐式地继承到子类,但子类自己却感觉不到.
    '''
    u = Db(name="Michael", email="test@test.org", password="my-pwd")
    u.save()
