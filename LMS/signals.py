
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import BorrowRequest

@receiver(pre_save, sender=BorrowRequest)
def handle_approval(sender, instance, **kwargs):

    if not instance.pk:
        return

    previous = BorrowRequest.objects.get(pk=instance.pk)

    # ONLY when status changes to APPROVED
    if (
        previous.status != BorrowRequest.Status.APPROVED
        and instance.status == BorrowRequest.Status.APPROVED
    ):
        book = instance.book

        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()


@receiver(pre_save, sender=BorrowRequest)
def update_available_copies_on_return(sender, instance, **kwargs):

    # Skip if object is new
    if not instance.pk:
        return

    previous = BorrowRequest.objects.select_related('book').get(
        pk=instance.pk
    )

    # ONLY when status changes APPROVED → RETURNED
    if (
        previous.status == BorrowRequest.Status.APPROVED and
        instance.status == BorrowRequest.Status.RETURNED
    ):

        book = instance.book

        book.available_copies += 1
        book.save()