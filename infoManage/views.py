from datetime import date

from django.shortcuts import render, get_object_or_404, redirect

from infoManage import models, forms

# Create your global variables here

form_ls = []


# Create your helpers here

def calculate_age(birthday):
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


# Create your views here.

def home(request):
    return render(request, 'home.html')


def payment_records(request):
    content = {'payment_records': models.缴费.objects.all()}
    record_id = []
    for payment_record in content['payment_records']:
        record_id.append(
            str(date.today().year) + str(date.today().month) +
            str(date.today().day) + str("%05d" % payment_record.id)
        )
    record_id.reverse()
    content['payment_converted_id'] = record_id
    return render(request, 'payment_records.html', content)


def payment_detail_record(request, payment_id):
    if request.method == 'POST':
        cf = forms.comment_form(request.POST, prefix='co')
        if cf.is_valid():
            c_form = cf.save(commit=False)
            c_form.备注类型 = '缴费备注'
            c_form.备注关联id = payment_id
            c_form.save()
            return redirect('infoManage:缴费详单', payment_id)
    else:
        cf = forms.comment_form(prefix='co')
        this_payment = get_object_or_404(models.缴费, id=payment_id)
        comment = models.备注.objects.filter(备注关联id=payment_id, 备注类型='缴费备注')
        this_coupon = models.优惠券使用.objects.filter(缴费单号=this_payment)
        content = {'payment_record': this_payment, 'comment': comment, 'c_form': cf,
                   'this_coupon': this_coupon}
        return render(request, 'payment_detail_record.html', content)


def payment_record_delete(request, payment_id):
    models.缴费.objects.get(id=payment_id).delete()
    for comment in models.备注.objects.filter(备注类型='缴费备注', 备注关联id=payment_id):
        comment.delete()
    return redirect('infoManage:缴费记录表')


def payment_record_edit(request, payment_id):
    return redirect('infoManage:缴费记录表')


def payment_new(request):
    if request.method == 'POST':
        student_form = forms.student_info_form(request.POST, prefix='student')
        parent_form = forms.parent_info_form(request.POST, prefix='parent')
        payment_form = forms.payment_form(request.POST, prefix='payment')
        coupon_form = forms.coupon_usage_form(request.POST, prefix='coupon_usage')
        if student_form.is_valid() and parent_form.is_valid() \
                and payment_form.is_valid() and coupon_form.is_valid():
            form = {'student_form': student_form, 'parent_form': parent_form, 'payment_form': payment_form,
                    'coupon_form': coupon_form}
            form_ls.append(form)
            form_id = form_ls.index(form)
            return redirect('infoManage:缴费确认', form_id)
    else:
        student_form = forms.student_info_form(prefix='student')
        parent_form = forms.parent_info_form(prefix='parent')
        payment_form = forms.payment_form(prefix='payment')
        coupon_form = forms.coupon_usage_form(prefix='coupon_usage')
    content = {'sf': student_form, 'pf': parent_form, 'nf': payment_form, 'coupon_usage_form': coupon_form}
    return render(request, 'payment_new.html', content)


def payment_confirm(request, sequence):
    sequence = int(sequence)
    student_model = form_ls[sequence]['student_form'].save(commit=False)
    parent_model = form_ls[sequence]['parent_form'].save(commit=False)
    payment_model = form_ls[sequence]['payment_form'].save(commit=False)
    coupon_model = form_ls[sequence]['coupon_form'].save(commit=False)
    should_pay = payment_model.缴费项目.课程定价 - coupon_model.优惠券编号.优惠券折扣

    if request.method == 'POST':
        payment_actual_amount_form = forms.payment_actual_amount_form(request.POST, prefix='paaf')
        comment_form = forms.comment_form(request.POST, prefix='comment')
        if payment_actual_amount_form.is_valid() and comment_form.is_valid():
            student_model.save()

            payment_actual_amount_model = payment_actual_amount_form.save(commit=False)

            payment_model.缴费学生 = student_model
            payment_model.缴费编号 = ''
            payment_model.缴费金额 = payment_actual_amount_model.缴费金额

            comment_model = comment_form.save(commit=False)

            payment_model.save()
            modified_row = models.缴费.objects.get(id=payment_model.id)
            modified_row.缴费编号 = str(date.today().year) + str(date.today().month) + str(date.today().day) + str(
                "%06d" % payment_model.id)
            modified_row.save()

            if parent_model.与学生关系 != '':
                parent_model.学生编号 = student_model
                parent_model.save()

            if coupon_model.优惠券编号 != '':
                coupon_model.缴费单号 = payment_model
                coupon_model.关联手机号 = parent_model.联系电话
                coupon_model.save()

            if comment_model.备注 != '':
                comment_model.备注类型 = '缴费备注'
                comment_model.备注关联id = payment_model.id
                comment_model.save()

            del form_ls[sequence]
            return redirect('infoManage:缴费详单', payment_model.id)

    else:
        payment_actual_amount_form = forms.payment_actual_amount_form(prefix='paaf')
        comment_form = forms.comment_form(prefix='comment')

    content = {'student_model': student_model, 'parent_model': parent_model,
               'payment_model': payment_model, 'coupon_model': coupon_model,
               'should_pay': should_pay,
               'payment_actual_amount_form': payment_actual_amount_form, 'comment_form': comment_form}

    return render(request, 'payment_confirm.html', content)


def payment_old(request, student_id):
    if request.method == 'POST':
        payment_form = forms.payment_form(request.POST, prefix='payment')
        coupon_form = forms.coupon_usage_form(request.POST, prefix='coupon_usage')
        this_student = get_object_or_404(models.学生, id=student_id)
        if payment_form.is_valid() and coupon_form.is_valid():
            form = {'this_student': this_student,
                    'payment_form': payment_form,
                    'coupon_form': coupon_form}
            form_ls.append(form)
            form_id = form_ls.index(form)
            return redirect('infoManage:续费确认', form_id)
    return redirect('infoManage:缴费记录表')


def payment_old_confirm(request, sequence):
    sequence = int(sequence)
    this_student = form_ls[sequence]['this_student']
    payment_model = form_ls[sequence]['payment_form'].save(commit=False)
    coupon_model = form_ls[sequence]['coupon_form'].save(commit=False)
    should_pay = payment_model.缴费项目.课程定价 - coupon_model.优惠券编号.优惠券折扣

    if request.method == 'POST':
        payment_actual_amount_form = forms.payment_actual_amount_form(request.POST, prefix='paaf')
        comment_form = forms.comment_form(request.POST, prefix='comment')
        if payment_actual_amount_form.is_valid() and comment_form.is_valid():
            payment_actual_amount_model = payment_actual_amount_form.save(commit=False)

            payment_model.缴费学生 = this_student
            payment_model.缴费编号 = ''
            payment_model.缴费金额 = payment_actual_amount_model.缴费金额

            comment_model = comment_form.save(commit=False)

            payment_model.save()
            modified_row = models.缴费.objects.get(id=payment_model.id)
            modified_row.缴费编号 = str(date.today().year) + str(date.today().month) + str(date.today().day) + str(
                "%06d" % payment_model.id)
            modified_row.save()

            if coupon_model.优惠券编号 != '':
                coupon_model.缴费单号 = payment_model
                contact = models.家长联系方式.objects.filter(学生编号=this_student).first()
                if contact is None:
                    coupon_model.关联手机号 = ''
                else:
                    coupon_model.关联手机号 = contact.联系电话
                coupon_model.save()

            if comment_model.备注 != '':
                comment_model.备注类型 = '缴费备注'
                comment_model.备注关联id = payment_model.id
                comment_model.save()

            del form_ls[sequence]
            return redirect('infoManage:缴费详单', payment_model.id)

    else:
        payment_actual_amount_form = forms.payment_actual_amount_form(prefix='paaf')
        comment_form = forms.comment_form(prefix='comment')
    content = {'payment_model': payment_model,
               'coupon_model': coupon_model,
               'student_model': this_student,
               'should_pay': should_pay,
               'payment_actual_amount_form': payment_actual_amount_form,
               'comment_form': comment_form}
    return render(request, 'payment_old_confirm.html', content)


def students(request):
    content = {'student_list': models.学生.objects.all()}
    today = date.today()
    birthday = []
    for student in content['student_list']:
        birthday.append(calculate_age(student.学生生日))
    birthday.reverse()
    content['birthday'] = birthday
    return render(request, 'student.html', content)


def students_detail(request, student_id):
    if request.method == 'POST':
        student_comment_form = forms.comment_form(request.POST, prefix='co')
        if student_comment_form.is_valid():
            c_form = student_comment_form.save(commit=False)
            c_form.备注类型 = '学生备注'
            c_form.备注关联id = student_id
            c_form.save()
            return redirect('infoManage:学生信息', student_id)

    else:
        student_comment_form = forms.comment_form(prefix='co')
        this_student = get_object_or_404(models.学生, id=student_id)
        student_comment = models.备注.objects.filter(备注关联id=student_id, 备注类型='学生备注')
        this_student_payment_record = models.缴费.objects.filter(缴费学生=student_id)
        student_age = calculate_age(this_student.学生生日)
        class_assignment = models.班级分配.objects.filter(学生编号=student_id)
        class_state = []
        for class_assign in class_assignment:
            class_state.append(class_state_color(class_assign))
            class_state.append(class_state_color(class_assign))

        class_state.reverse()
        student_assign_form = forms.student_assign_form(prefix='assign')
        parent_contact_form = forms.parent_info_form(prefix='parent')
        payment_form = forms.payment_form(prefix='payment')
        coupon_usage_form = forms.coupon_usage_form(prefix='coupon_usage')

        parent_contact = models.家长联系方式.objects.filter(学生编号=this_student)
        content = {'student': this_student,
                   'parent_contact': parent_contact,
                   'student_comment': student_comment,
                   'student_comment_form': student_comment_form,
                   'student_age': student_age,
                   'student_payment_record': this_student_payment_record,
                   'class_assignment': class_assignment,
                   'class_state_color': class_state,
                   'student_assign_form': student_assign_form,
                   'parent_contact_form': parent_contact_form,
                   'payment_form': payment_form,
                   'coupon_usage_form': coupon_usage_form}
        return render(request, 'student_detail.html', content)


def class_state_color(class_assign):
    if class_assign.上课日期 > date.today():
        return 'primary'
    elif class_assign.上课日期 <= date.today():
        if class_assign.结课日期 < date.today():
            return 'danger'
        else:
            return 'success'


def teachers(request):
    teacher_all = models.老师.objects.all()
    content = {'teacher_list': teacher_all}
    return render(request, 'teacher.html', content)


def teachers_new(request):
    if request.method == 'POST':
        tf = forms.teacher_form(request.POST, prefix='teacher')
        if tf.is_valid():
            tf.save()
            return redirect('infoManage:老师')
    else:
        tf = forms.teacher_form(prefix='teacher')
    content = {'teacher_form': tf}
    return render(request, 'teacher_new.html', content)


def time_table(request):
    return render(request, 'time_table.html')


def course(request):
    content = {'course_list': models.课程.objects.all()}
    return render(request, 'course.html', content)


def course_new(request):
    if request.method == 'POST':
        cf = forms.course_form(request.POST)
        if cf.is_valid():
            cf.save()
            return redirect('infoManage:课程')
    else:
        cf = forms.course_form()
    content = {'course_form': cf}
    return render(request, 'course_new.html', content)


def coupon(request):
    content = {'coupon_list': models.优惠券.objects.all()}
    return render(request, 'coupon.html', content)


def coupon_new(request):
    if request.method == 'POST':
        cf = forms.coupon_form(request.POST)
        if cf.is_valid():
            cf.save()
            return redirect('infoManage:优惠券')
    else:
        cf = forms.coupon_form()
    content = {'coupon_form': cf}
    return render(request, 'coupon_new.html', content)


def classes(request):
    class_all = models.班.objects.all()
    student_number = []
    for class_single in class_all:
        student_number.append(len(calculate_current_student_list(class_single)))
    student_number.reverse()
    content = {'class_list': class_all, 'student_number': student_number}
    return render(request, 'class.html', content)


def class_new(request):
    if request.method == 'POST':
        class_form = forms.class_form(request.POST, prefix='class')
        if class_form.is_valid():
            class_form.save()
            return redirect('infoManage:班')

    else:
        class_form = forms.class_form(prefix='class')
    content = {'class_form': class_form}
    return render(request, 'class_new.html', content)


def class_detail(request, class_id):
    if request.method == 'POST':
        class_comment_form = forms.comment_form(request.POST, prefix='co')
        if class_comment_form.is_valid():
            c_form = class_comment_form.save(commit=False)
            c_form.备注类型 = '班备注'
            c_form.备注关联id = class_id
            c_form.save()
            return redirect('infoManage:班信息', class_id)

    else:
        class_comment_form = forms.comment_form(prefix='co')
        this_class = get_object_or_404(models.班, id=class_id)
        class_comment = models.备注.objects.filter(备注关联id=class_id, 备注类型='班备注')
        student_list = calculate_current_student_list(this_class=this_class)
        student_age = []
        for student in student_list:
            student_age.append(calculate_age(student.学生编号.学生生日))

        student_age.reverse()

        content = {'class': this_class,
                   'class_comment': class_comment,
                   'class_comment_form': class_comment_form,
                   'students_list': student_list,
                   'students_list_count': len(student_list),
                   'student_age': student_age}
        return render(request, 'class_detail.html', content)


def calculate_current_student_list(this_class):
    student_all = models.班级分配.objects.filter(班编号=this_class)
    student_list = []
    for student in student_all:
        if student.上课日期 <= date.today() <= student.结课日期:
            student_list.append(student)

    return student_list


def students_assign(request, student_id):
    if request.method == 'POST':
        student_assign_form = forms.student_assign_form(request.POST, prefix='assign')
        if student_assign_form.is_valid():
            student_assign_model = student_assign_form.save(commit=False)
            if student_assign_model.上课日期 < student_assign_model.结课日期:
                this_student = get_object_or_404(models.学生, id=student_id)
                student_assign_model.学生编号 = this_student
                student_assign_model.save()

            return redirect('infoManage:学生信息', student_id)


def students_contact_new(request, student_id):
    if request.method == 'POST':
        parent_contact_form = forms.parent_info_form(request.POST, prefix='parent')
        if parent_contact_form.is_valid():
            parent_contact_model = parent_contact_form.save(commit=False)
            if parent_contact_model.家长姓名 != '' and parent_contact_model.联系电话 != '' \
                    and parent_contact_model.与学生关系 != '':
                this_student = get_object_or_404(models.学生, id=student_id)
                parent_contact_model.学生编号 = this_student

                parent_contact_model.save()

        return redirect('infoManage:学生信息', student_id)
