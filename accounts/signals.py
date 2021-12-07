from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Vendor
User = get_user_model()

@receiver(post_save,sender=User)

def send_activation_email(sender,instance,created,**kwargs):

    if created:
        message = f"""Hello {instance.username},
            Welcome,Thank you for joining Phiston today,you can now place your order on Phiston to get your meal delivered to you at your doorstep.
            You have a 50% discount for your first order, your choice is an order away. 
        """
        send_mail(subject="Activation mail",message=message,recipient_list=[instance.email],from_email = 'admin@phiston.com')

   