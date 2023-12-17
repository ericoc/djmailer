from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class MailerVariable(models.Model):
    """
    Mailer Variable.
    """
    name = models.SlugField(
        db_column="name",
        help_text="Name of the variable to be made available to all templates.",
        primary_key=True,
        verbose_name="Name"
    )
    value = models.CharField(
        blank=False,
        db_column="value",
        help_text="Value of the global e-mail template variable.",
        max_length=64,
        null=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=64)
        ],
        verbose_name="Value"
    )

    class Meta:
        db_table = "variables"
        managed = True
        verbose_name = "Variable"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self):
        return self.name
