from django.test import TestCase
from materias.models import UnidadAcademica

class TestSmoke(TestCase):
    def test_dos_mas_dos(self):
        self.assertEqual(2+2, 4)

    def test_agrega_unidad_academica(self):
        unidad_academica = UnidadAcademica.objects.create(
            nombre = 'Unidad Académica de Ingeniería Eléctrica',
            abreviacion = 'UAIE'
        )
        self.assertEqual(1, UnidadAcademica.objects.count())

    def test_agrega_unidad_academica_compara_nombres(self):
        unidad_academica = UnidadAcademica.objects.create(
            nombre = 'Unidad Académica de Ingeniería Eléctrica',
            abreviacion = 'UAIE'
        )
        unidad = UnidadAcademica.objects.first()
        self.assertEqual(unidad.nombre, unidad_academica.nombre)

