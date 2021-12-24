from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
User = get_user_model()

@receiver(post_save,sender=User)

def send_activation_email(sender,instance,created,**kwargs):

    if created:
        message = f"""Hello {instance.name},
            Welcome,Thank you for joining foodie-z today,you can now place your order on Phiston to get your meal delivered to you at your doorstep.
            You have a 50% discount for your first order, your choice is an order away. 
        """
        send_mail(subject="Welcome to Foodie-z",message=message,recipient_list=[instance.email],from_email = 'admin@foodie-z.com')


    # elif created and CustomUser.is_vendor == True:
    #     message = f"""Hello {instance.vendor_name},
    #             Welcome on board, your journey as a chef just began, kindly list dishes you are great at and let us give you the customers you wish for, remember to update your payment account. Always check the phiston platform everyday to confirm pending orders you may have. we wish you the best of luck.


    #             Team Phiston
    #     """
    #     send_mail(subject="Activation mail",message=message,recipient_list=[instance.email],from_email = 'admin@phiston.com')
   