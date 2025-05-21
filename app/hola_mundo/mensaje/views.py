from django.shortcuts import render


def calculadora(request):
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    operaciones = {'X', '/', '-', '+', '%'}
    context = {
        'numero': 0
    }
    if request.method == 'POST':
        # print('Método post')
        operando1 = request.POST.get('operando1', None)
        operacion = request.POST.get('operacion', None)

        resultado = request.POST.get('resultado')
        numero = list(request.POST.keys())[2]
        if numero in numeros or numero == '.':
            context['numero'] = resultado + \
                numero if resultado != '0' else numero
        elif numero == '+/-':
            context['numero'] = int(resultado) * -1
        elif numero in operaciones:
            if numero == 'X':
                context['operador1'] = resultado
                context['operacion'] = numero
        else:
            if operando1:
                if operacion == 'X':
                    context['numero'] = int(resultado) * int(context['numero'])
        # print(request.POST.keys())
    else:
        print('Método get')
    print(context)
    return render(request, 'calculadora.html', context)


def tabla(request, numero, numero2):
    multiplicaciones = []
    for num in range(1, numero2+1):
        multiplicaciones.append({'num': num, 'res': num * numero})
    # print(multiplicaciones)
    context = {
        'numero': numero,
        'numero2': numero2,
        'multiplicaciones': multiplicaciones,
    }
    return render(request, 'tabla.html', context)


def bienvenida(request):
    return render(request, 'bienvenida.html')


def calificaciones(request):
    cals = [
        {'materia': 'Linux', 'calif': 10},
        {'materia': 'Testing', 'calif': 7},
        {'materia': 'Deployment', 'calif': 8},
        {'materia': 'Frameworks', 'calif': 10},
    ]
    return render(request, 'calificaciones.html', {'calificaciones': cals})


def hola(request):
    # name = 'Alex'
    # edad = 43

    context = {
        'name': 'Alex',
        'edad': 43,
        'materias': [
            'Linux',
            'Testing',
            'Deployment',
            'Frameworks'
        ]
    }
    # return render(request, 'hola.html', {'name': name, 'edad':edad})
    return render(request, 'hola.html', context)
