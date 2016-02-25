#!/usr/bin/env python

from mqORM.fields import Field
from mqORM.connection import connDb


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

        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
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

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        column_dict = {}
        for k, v in self.__mappings__.items():
            column_dict[v.name] = self[k]
        try:
            conn = connDb()
            conn.insert(self.__table__, column_dict)
        except Exception as e:
            print(e)
            return e

if __name__ == "__main__":
    import os
