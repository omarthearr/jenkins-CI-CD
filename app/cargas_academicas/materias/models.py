from django.db import models


class UnidadAcademica(models.Model):
    nombre = models.CharField('Nombre', max_length=250)
    abreviacion = models.CharField(
        'Abreviación', max_length=5, null=True, blank=True)

    def __str__(self):
        return self.nombre


class ProgramaAcademico(models.Model):
    nombre = models.CharField('Nombre', max_length=250)
    abreviacion = models.CharField('Abreviación', max_length=5)
    unidad_academica = models.ForeignKey(
        "materias.UnidadAcademica", verbose_name="Unidad académica", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    clave = models.CharField('Clave', max_length=50, primary_key=True)
    nombre = models.CharField('Nombre', max_length=250)
    descripcion = models.CharField(
        'Descripción', max_length=500, blank=True, null=True)
    creditos = models.SmallIntegerField()
    semestre = models.SmallIntegerField()
    programa_academico = models.ForeignKey(
        "materias.ProgramaAcademico", verbose_name="Programa académico", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
