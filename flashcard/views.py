from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def novo_flashcard(request):

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user.id)

        categoria_filtrar  = request.GET.get('categoria')
        dificuldade_filtrar  = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

        return render(request, 'novo_flashcard.html', 
            {   
                'categorias': categorias,
                'dificuldades': dificuldades,
                'flashcards': flashcards,
            })

    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        dificuldade = request.POST.get('dificuldade')
        categoria = request.POST.get('categoria')
        cat = Categoria.objects.filter(id=categoria).first()

        if len(pergunta.strip()) != 0 or len(resposta.strip()) != 0:
            flashcard = Flashcard(
                user=request.user,
                resposta=resposta,
                pergunta=pergunta,
                categoria=cat,
                dificuldade=dificuldade,
            )
            flashcard.save()
            messages.add_message(request, constants.SUCCESS, 'flashcard criado com sucesso')
        else:
            messages.add_message(request, constants.ERROR, 'prencha os campos de pergunta e resposta')
        
        return redirect(reverse('novo_flashcard'))
@login_required
def deletar_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    try:
        flashcard.delete()
        messages.add_message(request,  constants.SUCCESS, 'Flashcard deletado com sucesso')
    except: 
        messages.add_message(request, constants.ERROR, 'Não foi possível deletar o flashcard')
    
    return redirect(reverse('novo_flashcard'))

@login_required
def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES 

        return render(request, 'iniciar_desafio.html',
        {
            'categorias': categorias,
            'dificuldades': dificuldades,
        })

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()
        desafio.categoria.add(*categorias)

        flashcards = (
        Flashcard.objects.filter(user=request.user)
        .filter(dificuldade=dificuldade)
        .filter(categoria_id__in=categorias)
        .order_by('?')
        )
        
        if flashcards.count() < int(qtd_perguntas):
            messages.add_message(request, constants.ERROR, 'A quantidade de perguntas excedeu a dos flashcards')
            return redirect(reverse('iniciar_desafio'))

        flashcards = flashcards[: int(qtd_perguntas)]
        
        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
            flashcard=f,
            )
            flashcard_desafio.save()

            desafio.flashcards.add(flashcard_desafio)
        
        desafio.save()

        return redirect(reverse('listar_desafio'))

@login_required
def desafio(request, id):
    desafio = Desafio.objects.get(id=id)
    if request.method == 'GET':
        acertos = desafio.flashcards.filter(respondido=True).filter(acertou=True).count()
        erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
        faltantes = desafio.flashcards.filter(respondido=False).count()

        return render(request, 'desafio.html', {'desafio': desafio,'acertos':acertos,'erros': erros, 'faltantes':faltantes})
@login_required
def listar_desafio(request):

    if request.method == 'GET':
        desafios = Desafio.objects.filter(user=request.user)
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        categoria_filtrar = request.GET.get('categoria_filtrar')
        dificuldade_filtrar = request.GET.get('dificuldade_filtrar')

        if categoria_filtrar:
            desafios = desafios.filter(categoria__id__in=categoria_filtrar)
        if dificuldade_filtrar:
            desafios = desafios.filter(dificuldade=dificuldade_filtrar)

        return render(request, 'listar_desafio.html',
            {'desafios': desafios,
            'categorias': categorias,
            'dificuldades': dificuldades,
            })
    
@login_required
def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)

    if flashcard_desafio.flashcard.user == request.user:

        acertou = request.GET.get('acertou')
        desafio_id = request.GET.get('desafio_id')
        flashcard_desafio.respondido = True
        flashcard_desafio.acertou = True if acertou == '1' else False
        flashcard_desafio.save()
        return redirect(f'/flashcard/desafio/{desafio_id}/')

    else:
        raise Http404()


    return redirect(reverse('desafio', desafio_id))
@login_required
def relatorio(request, id):
    desafio = Desafio.objects.get(id=id)

    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(acertou=False).count()
    dados = [acertos, erros]
    categorias = desafio.categoria.all()
    name_categoria = [i.nome for i in categorias]
    dados2 = []
    for categoria in categorias:
        dados2.append(desafio.flashcards.filter(flashcard__categoria=categoria).filter(acertou=True).count())
        return render(request, 'relatorio.html', {'desafio': desafio, 'dados': dados, 'categorias': name_categoria, 'dados2': dados2,},)
