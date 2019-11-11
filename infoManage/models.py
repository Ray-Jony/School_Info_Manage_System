from django.db import models


# Create your models here.

class 学生(models.Model):
    学生姓名 = models.CharField(max_length=12)
    学生性别 = models.CharField(max_length=12, default='女',
                            choices=[
                                ('男', '男'),
                                ('女', '女')
                            ])
    学生生日 = models.DateField()

    class Meta:
        verbose_name_plural = "学生"

    def __str__(self):
        return self.学生姓名


class 家长联系方式(models.Model):
    学生编号 = models.ForeignKey(to='学生', to_field='id', on_delete=models.CASCADE)
    家长姓名 = models.CharField(max_length=12, blank=True)
    联系电话 = models.CharField(max_length=16, blank=True)
    与学生关系 = models.CharField(max_length=20, blank=True, choices=[
        ('爸爸', '爸爸'),
        ('妈妈', '妈妈'),
        ('爷爷', '爷爷'),
        ('奶奶', '奶奶'),
        ('姥姥', '姥姥'),
        ('姥爷', '姥爷'),
        ('哥哥', '哥哥'),
        ('姐姐', '姐姐'),
        ('姑姑', '姑姑'),
        ('姑父', '姑父'),
        ('姨', '姨'),
        ('姨夫', '姨夫'),
        ('其他直系亲属', '其他直系亲属'),
        ('其他关系', '其他关系'),
    ])

    class Meta:
        verbose_name_plural = "家长联系方式"

    def __str__(self):
        return self.家长姓名 + self.联系电话


class 课程(models.Model):
    课程名称 = models.CharField(max_length=50)
    课程定价 = models.DecimalField(max_digits=7, decimal_places=2)
    课程介绍 = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "课程"

    def __str__(self):
        return self.课程名称


class 老师(models.Model):
    老师姓名 = models.CharField(max_length=12)
    老师电话 = models.CharField(max_length=16)

    class Meta:
        verbose_name_plural = "老师"

    def __str__(self):
        return self.老师姓名


class 班(models.Model):
    班名称 = models.CharField(max_length=50, unique=True)
    上课时间 = models.CharField(max_length=50)
    上课教室 = models.CharField(max_length=50)
    课程编号 = models.ForeignKey(to='课程', to_field='id', on_delete=models.DO_NOTHING)
    老师编号 = models.ForeignKey(to='老师', to_field='id', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "班"

    def __str__(self):
        return self.班名称


class 缴费(models.Model):
    缴费编号 = models.CharField(max_length=50, unique=True)
    缴费学生 = models.ForeignKey(to='学生', to_field='id', on_delete=models.DO_NOTHING)
    缴费时间 = models.DateTimeField(auto_now_add=True)
    缴费金额 = models.DecimalField(max_digits=7, decimal_places=2)
    缴费项目 = models.ForeignKey(to='课程', to_field='id', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "缴费"

    def __str__(self):
        return str(self.id)


class 优惠券(models.Model):
    优惠券名称 = models.CharField(max_length=50, unique=True)
    优惠券折扣 = models.DecimalField(max_digits=7, decimal_places=2)
    优惠券介绍 = models.TextField()

    class Meta:
        verbose_name_plural = "优惠券"

    def __str__(self):
        return self.优惠券名称


class 优惠券使用(models.Model):
    优惠券编号 = models.ForeignKey('优惠券', on_delete=models.DO_NOTHING)
    关联手机号 = models.CharField(max_length=16, blank=True)
    缴费单号 = models.ForeignKey('缴费', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name_plural = "优惠券使用"

    def __str__(self):
        return self.id


class 班级分配(models.Model):
    学生编号 = models.ForeignKey('学生', on_delete=models.CASCADE)
    班编号 = models.ForeignKey('班', on_delete=models.CASCADE)
    上课日期 = models.DateField()
    结课日期 = models.DateField()

    class Meta:
        verbose_name_plural = "班级分配"

    def __str__(self):
        return '学生：' + 学生.objects.filter(id=self.学生编号) + '班：' + 班.objects.filter(id=self.班编号)


class 库存(models.Model):
    物品名称 = models.CharField(max_length=50)
    物品类别 = models.CharField(max_length=30)
    库存数量 = models.IntegerField()
    创建时间 = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "仓库"

    def __str__(self):
        return self.物品名称


class 入库记录(models.Model):
    入库时间 = models.DateTimeField(auto_now_add=True)
    入库物品 = models.ForeignKey('库存', on_delete=models.DO_NOTHING)
    入库数量 = models.IntegerField()
    入库单价 = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name_plural = "入库记录"

    def __str__(self):
        return self.入库物品


class 出库记录(models.Model):
    出库时间 = models.DateTimeField(auto_now_add=True)
    出库物品 = models.ForeignKey('库存', on_delete=models.DO_NOTHING)
    出库数量 = models.IntegerField()
    出库单价 = models.DecimalField(max_digits=7, decimal_places=2)
    关联缴费 = models.ForeignKey('缴费', on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        verbose_name_plural = "出库记录"

    def __str__(self):
        self.出库物品


class 课程表(models.Model):
    上课班次 = models.ForeignKey('班', on_delete=models.CASCADE)
    上课时间 = models.DateTimeField()
    下课时间 = models.DateTimeField()
    上课教室 = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "课程表"

    def __str__(self):
        self.上课班次


class 备注(models.Model):
    备注类型 = models.CharField(max_length=10, choices=[
        ('学生备注', '学生备注'),
        ('缴费备注', '缴费备注'),
        ('优惠券备注', '优惠券备注'),
        ('优惠券使用备注', '优惠券使用备注'),
        ('家长联系方式备注', '家长联系方式备注'),
        ('课程备注', '课程备注'),
        ('班备注', '班备注'),
        ('班级分配备注', '班级分配备注'),
        ('老师备注', '老师备注'),
        ('库存备注', '库存备注'),
        ('入库记录备注', '入库记录备注'),
        ('出库记录备注', '出库记录备注'),
    ])
    备注关联id = models.IntegerField()
    备注 = models.TextField(blank=True)
    # 如果这里设置blank=True 那么就必须限制每次创建订单的时候不会创建空字符串
    备注时间 = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "备注"

    def __str__(self):
        self.备注类型
