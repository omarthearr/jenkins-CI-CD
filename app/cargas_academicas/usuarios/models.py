from django.db import models
from django.contrib.auth.models import User


class Alumno(models.Model):
    matricula = models.CharField(max_length=10)
    nombre = models.CharField(max_length=60)
    apelllido_paterno = models.CharField(max_length=80)
    apelllido_materno = models.CharField(max_length=60, null=True, blank=True)
    programa_academico = models.ForeignKey(
        "materias.ProgramaAcademico", 
        verbose_name="Programa académico", on_delete=models.DO_NOTHING)
    fecha_nacimiento = models.DateField()
    usuario = models.OneToOneField(User, verbose_name="usuario", on_delete=models.CASCADE)

class Docente(models.Model):
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=60)
    apelllido_paterno = models.CharField(max_length=80)
    apelllido_materno = models.CharField(max_length=60, null=True, blank=True)
    programa_academico = models.ManyToManyField(
        "materias.ProgramaAcademico", 
        verbose_name="Programa académico")
    fecha_nacimiento = models.DateField()
    usuario = models.OneToOneField(User, verbose_name="usuario", on_delete=models.CASCADE)
