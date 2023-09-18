from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    contactNo = models.CharField(max_length=10)
    otp = models.CharField(max_length=1024, blank=True, null=True)

    # def __str__(self):
    #     return self.firstname + " " + self.lastname + " " +self.username + " " +self.contactNo

    class Meta:
        db_table = 'member'
        # managed = False


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=10, blank=True, null=True)
    member = models.ForeignKey('Member', on_delete=models.DO_NOTHING, related_name='member_payment')

    class Meta:
        db_table = 'payment'
        # managed = False


class PaytmHistory(models.Model):
    member = models.CharField(max_length=30)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.IntegerField('TXN ID')
    BANKTXNID = models.IntegerField('BANK TXN ID', null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        # app_label = 'paytm'
        db_table = 'paytm'
    def __unicode__(self):
        return self.STATUS
