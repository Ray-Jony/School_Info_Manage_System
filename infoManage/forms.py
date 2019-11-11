from django import forms
from infoManage import models


class student_info_form(forms.ModelForm):
    class Meta:
        model = models.学生
        fields = '__all__'

        widgets = {
            '学生姓名': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入学生姓名'}),
            '学生性别': forms.Select(attrs={'class': 'form-control'}),
            '学生生日': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class student_assign_form(forms.ModelForm):
    class Meta:
        model = models.班级分配
        exclude = ['学生编号']

        widgets = {
            '班编号': forms.Select(attrs={'class': 'form-control my-1 mr-sm-2 col-auto'}),
            '上课日期': forms.DateInput(attrs={'class': 'form-control my-1 mr-sm-2 col-auto', 'type': 'date'}),
            '结课日期': forms.DateInput(attrs={'class': 'form-control my-1 mr-sm-2 col-auto', 'type': 'date'}),
        }


class parent_info_form(forms.ModelForm):
    class Meta:
        model = models.家长联系方式
        exclude = ['学生编号']

        widgets = {
            '家长姓名': forms.TextInput(attrs={'class': 'form-control my-1 mr-sm-2 col-auto', 'placeholder': '输入家长姓名'}),
            '联系电话': forms.TextInput(attrs={'class': 'form-control my-1 mr-sm-2 col-auto', 'placeholder': '输入11位国内手机号'}),
            '与学生关系': forms.Select(attrs={'class': 'form-control my-1 mr-sm-2 col-auto', 'placeholder': '输入与学生的关系'}),
        }


class payment_form(forms.ModelForm):
    class Meta:
        model = models.缴费
        exclude = ['缴费学生', '缴费编号', '缴费金额']

        widgets = {
            '缴费金额': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入缴费金额'}),
            '缴费项目': forms.Select(attrs={'class': 'form-control'}),
        }


class payment_actual_amount_form(forms.ModelForm):
    class Meta:
        model = models.缴费
        fields = ['缴费金额']

        widgets = {
            '缴费金额': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入缴费金额'}),
        }


class course_form(forms.ModelForm):
    class Meta:
        model = models.课程
        fields = '__all__'

        widgets = {
            '课程名称': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入课程名称'}),
            '课程定价': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入课程定价'}),
            '课程介绍': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '输入课程介绍'}),
        }


class teacher_form(forms.ModelForm):
    class Meta:
        model = models.老师
        fields = '__all__'

        widgets = {
            '老师姓名': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入老师姓名'}),
            '老师电话': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入老师电话'})
        }


class comment_form(forms.ModelForm):
    class Meta:
        model = models.备注
        fields = ['备注']

        widgets = {
            '备注': forms.TextInput(attrs={'class': 'form-control'})
        }


class coupon_form(forms.ModelForm):
    class Meta:
        model = models.优惠券
        fields = '__all__'

        widgets = {
            '优惠券名称': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入优惠券名称'}),
            '优惠券折扣': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入优惠券折扣'}),
            '优惠券介绍': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '输入优惠券使用说明'}),
        }


class coupon_usage_form(forms.ModelForm):
    class Meta:
        model = models.优惠券使用
        fields = ['优惠券编号']

        widgets = {
            '优惠券编号': forms.Select(attrs={'class': 'form-control'})
        }


class class_form(forms.ModelForm):
    class Meta:
        model = models.班
        fields = '__all__'

        widgets = {
            '班名称': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入班名称'}),
            '上课时间': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入上课时间'}),
            '上课教室': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入上课教室'}),
            '老师编号': forms.Select(attrs={'class': 'form-control', 'placeholder': '输入上课教室'}),
            '课程编号': forms.Select(attrs={'class': 'form-control', 'placeholder': '输入上课教室'}),
        }
