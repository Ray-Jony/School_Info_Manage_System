from django.urls import path
from . import views

app_name = 'infoManage'
urlpatterns = [
    path('', views.home, name='主页'),

    path('payment_record/', views.payment_records, name='缴费记录表'),
    path('payment_record/new_payment/', views.payment_new, name='新生缴费'),
    path('payment_record/old_payment/<student_id>', views.payment_old, name='老生缴费'),
    path('payment_record/delete/<payment_id>', views.payment_record_delete, name='缴费详单删除'),
    path('payment_record/edit/<payment_id>', views.payment_record_edit, name='缴费详单编辑'),
    path('payment_record/payment_confirm/<sequence>', views.payment_confirm, name='缴费确认'),
    path('payment_record/old_payment_confirm/<sequence>', views.payment_old_confirm, name='续费确认'),
    path('payment_record/<payment_id>', views.payment_detail_record, name='缴费详单'),

    path('coupon/', views.coupon, name='优惠券'),
    path('coupon/new_coupon', views.coupon_new, name='新优惠券'),

    path('course/', views.course, name='课程'),
    path('course/new_course', views.course_new, name='新课程'),

    path('time_table/', views.time_table, name='课程时间表'),

    path('students/', views.students, name='学生'),
    path('students/student_assign/<student_id>', views.students_assign, name='学生分配'),
    path('students/<student_id>', views.students_detail, name='学生信息'),
    path('students/<student_id>/new_contact', views.students_contact_new, name='新联系方式'),

    path('teachers/', views.teachers, name='老师'),
    path('teachers/new_teacher', views.teachers_new, name='新老师'),

    path('classes/', views.classes, name='班'),
    path('classes/new_class/', views.class_new, name='新班'),
    path('classes/<class_id>', views.class_detail, name='班信息'),

]

# 我如此命名路径在以下情况下会出现问题
# 1. 例如 classes/<class_id>
#         classes/new_class
#    当我想要访问new_class页面的时候，他还是会判断我输入的new_class可能是个class_id
#    但这个问题交换个位置，或者改变命名方式就能解决
