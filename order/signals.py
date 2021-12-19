from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Order


"""
THIS SECTION SENDS A MESSAGE TO THE USER AND ADMIN DEPENDING ON THE ACTION
"""

@receiver(post_save,sender=Order)

def order_placed(sender,instance,created,**kwargs):
   
    if created:
        #a post save, sends an email to a user after an order has been created
        message = f"""Hello {instance.user.name},
            Your order requesting {instance.unit} unit/units of {instance.order} has been placed and is still pending, kindly wait as we confirm your order. Once order is confirmed you will  get an email on the new update of your order, the delivery address is {instance.billing_address}. Thanks for using our services.
            remember to give us a feedback and rate us to enable other customers find their best choice. we hope you enjoy your meal 
        """
        send_mail(subject=f"Order {instance.order_no} ",message=message,recipient_list=[instance.user],from_email = 'admin@phiston.com')



        # this sends an email to the admin notifying the admin of any new order created
        message = f"""Hello {'Admin'},
            You have a new order, with order number {instance.order_no} for {instance.unit} unit/s of {instance.order}. Please update the order status and ship immediately
        """
        send_mail(subject=f"New order ",message=message,recipient_list=['Admin@phiston.com'],from_email = 'admin@phiston.com')

        


@receiver(post_save,sender=Order)

def scheduled(sender,instance,created,**kwargs):
   
    #this sends an email to the user  to update the user on the status of his order, from when the order was placed and moved from pending to scheduled then to anyother valid status
    if instance.status == "scheduled":
        message = f"""Hello {instance.name},
            Your order has been scheduled and will be delivered in 10mins kindly excercise patience while we deliver your meal. Remember us a feedback and rate us to enable other customers find their best choice. we hope you enjoy your meal 
        """
        send_mail(subject=f"Order: {instance.order_no} ",message=message,recipient_list=[instance.user],from_email = 'admin@phiston.com')

    elif instance.status == "delivered":

        message = f"""Hello {instance.name},
            Your order has been delivered and will be delivered in 10mins kindly excercise patience while we deliver your meal. Remember us a feedback and rate us to enable other customers find their best choice. we hope you enjoy your meal 
        """
        send_mail(subject=f"Order {instance.order_no} ",message=message,recipient_list=[instance.user],from_email = 'admin@phiston.com')


    elif instance.status == "failed":

        message = f"""Hello {instance.name},
            Efforts to deliver your order to you has failed and  kindly contact the delivery agent as soon as possible to recieve your package as the order will be cancelled in the next hour. Thanks for your patronage we hope to see you next time.
        """
        send_mail(subject=f"Order {instance.order_no} ",message=message,recipient_list=[instance.user],from_email = 'admin@phiston.com')

    elif instance.status == "cancelled":

        message = f"""Hello {instance.name},
            Your order has been cancelled due to some problems, we are really sorry for these issues. Kindly contact the customer support to place to help you complete your order. Remember us a feedback and rate us to enable other customers find their best choice. we hope you enjoy your meal 
        """
        send_mail(subject=f"Order {instance.order_no} ",message=message,recipient_list=[instance.user],from_email = 'admin@phiston.com')

