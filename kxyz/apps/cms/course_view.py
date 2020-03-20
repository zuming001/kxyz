from django.shortcuts import render
from django.views import View
from apps.course.models import Course, CourseCategory, Lecturer
from .forms import AddCourseCtegoryForm, EditCourseCategoryForm
from .forms import PubCourseForm
from utils import restful


# 课程列表管理
class PubCourse(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'lecturers': Lecturer.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            category_id = form.cleaned_data.get("category_id")
            lecturer_id = form.cleaned_data.get("lecturer_id")
            video_url = form.cleaned_data.get("video_url")
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get("price")
            duration = form.cleaned_data.get("duration")
            profile = form.cleaned_data.get("profile")

            # 因为category,和lecturer 在Course中是以外键从存储,
            # 所以需要在CourseCategory,Lecturer中先查询出来,再存入Course中
            category = CourseCategory.objects.get(pk=category_id)
            lecturer = Lecturer.objects.get(pk=lecturer_id)

            Course.objects.create(title=title, category=category, lecturer=lecturer,
                                  video_url=video_url, cover_url=cover_url, price=price, duration=duration,
                                  profile=profile)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 课程分类
def course_category(request):
    categories = CourseCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/course_category.html', context=context)


# 编辑课程分类
def edit_course_category(request):
    category_id = request.POST.get("category_id")
    new_name = request.POST.get("new_name")
    if category_id and new_name:
        CourseCategory.objects.filter(pk=category_id).update(name=new_name)
        return restful.ok()
    else:
        return restful.params_error(message='课程分类的新名称不为空!!!')


# 添加课程分类
def add_course_category(request):
    form = AddCourseCtegoryForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        exists = CourseCategory.objects.filter(name=name).exists()
        if not exists:
            CourseCategory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='该课程分类已经存在!')
    else:
        return restful.params_error(message=form.get_errors())


# 删除课程分类
def delete_course_category(request):
    try:
        category_id = request.POST.get("category_id")
        CourseCategory.objects.filter(pk=category_id).delete()
        return restful.ok()
    except ValueError:
        return restful.params_error(message='该课程分类不存在!')
