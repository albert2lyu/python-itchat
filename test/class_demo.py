class Student(object):
    school = 'ly.university'
    __slots__ = ('__name','__age')
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    def __str__(self):
        return 'this student is {} , he is {} years old'.format(self.__name,self.__age)

    def get_name(self):
        return self.__name
    # @property
    def get_age(self):
        return self.__age
    def set_age(self, age):
        self.__age =age
    def set_name(self, name):
        self.__name =name
if __name__ == '__main__':
    st1 = Student('jaak',24)
    print(st1)
    # st1.age = 25
    print(st1.get_age())
    st1.set_name('chenyy')
    print(st1)
    print(st1._Student__name)
    print(type(st1))
    print(isinstance(st1,object))
    print(isinstance(st1,Student))
    print(dir(st1))
    print(hasattr(st1,'school'))
    print(st1.school)
    print(Student.school)
    # setattr(st1,'school','ly2')
    print(st1.school)
    # del st1.school
    # st1.ss = 123
    print(getattr(st1,'school'))
else:
    print('hello world')
    

