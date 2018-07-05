class Teacher:
    def __init__(self, school_obj):
        self.school_obj = school_obj


class Student:
    def __init__(self, school_obj, class_obj):
        self.school_obj = school_obj
        self.class_obj = class_obj


class School:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.classes = []

    def create_course(self, course_name, duration, price):
        """ 创建课程 """
        course_obj = Course(course_name, duration, price)
        self.courses.append(course_obj)
        return course_obj

    def create_class(self, class_name, course_obj, teacher_obj):
        """ 创建班级 """
        class_obj = Class(class_name, course_obj, teacher_obj)
        self.classes.append(class_obj)
        return class_obj


class Class:
    def __init__(self, class_name, course_obj, teacher_obj):
        self.class_name = class_name
        self.course_obj = course_obj
        self.teacher_obj = teacher_obj


class Course:
    def __init__(self, course_name, duration, price):
        self.course_name = course_name
        self.duration = duration
        self.price = price

