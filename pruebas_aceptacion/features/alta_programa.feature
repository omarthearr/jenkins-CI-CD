@skip
Característica: Agregar programa academico
Como administrador del sistema de cargas academicas
quiero agregar una Programa Academico
para posteriormente agregar programas academicos

Escenario: Datos Correctos
Dado ingreso a la plataforma en la url "http://app:8000"
Y doy click al menu Programas, lugo click en el sub menu Nuevo
Y registro el programa "Ingenieria en Software" y su abreviacion "IS" y su unidad "Unidad Académica de Ingeniería Eléctrica"
Cuando presione el boton Agregar del formulario
Entonces puedo ver el programa "Ingenieria en Software" en la lista de Programas.