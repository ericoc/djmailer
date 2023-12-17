from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models

from .widget import Widget


class WidgetComment(models.Model):
    """
    Widget Comment.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text="Widget comment identification number.",
        primary_key=True,
        verbose_name="Widget Comment ID"
    )
    widget = models.ForeignKey(
        blank=False,
        db_column="widget",
        editable=False,
        null=False,
        help_text="Widget related to the comment.",
        to=Widget,
        on_delete=models.PROTECT,
        verbose_name="Widget"
    )
    text = models.TextField(
        blank=True,
        db_column="text",
        help_text="Text of the widget comment.",
        max_length=256,
        validators=[MaxLengthValidator(limit_value=256)],
        verbose_name="Widget Comment Text"
    )
    created_at = models.DateTimeField(
        blank=False,
        db_column="created_at",
        editable=False,
        null=False,
        auto_now_add=True,
        help_text="Date and time when the widget comment was created.",
        verbose_name="Created At"
    )
    created_by = models.ForeignKey(
        blank=False,
        db_column="created_by",
        editable=False,
        null=True,
        help_text="User who created the widget comment.",
        related_name="+",
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Created By"
    )
    updated_at = models.DateTimeField(
        blank=False,
        db_column="updated_at",
        editable=False,
        default=None,
        null=True,
        help_text="Date and time when the widget comment was last updated.",
        verbose_name="Updated At"
    )

    class Meta:
        db_table = "widget_comments"
        default_related_name = "comment"
        managed = True
        ordering = ("-updated_at", "-created_at", "-id",)
        unique_together = (("created_by", "widget"),)
        verbose_name = "Comment"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return f'"{self.text[0:10]}\"... @ {self.widget} by {self.created_by}'
