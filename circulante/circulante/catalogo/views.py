#coding: utf-8


from .models import Publicacao, Credito
from django.shortcuts import render, get_object_or_404
from isbn import validatedISBN10
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import PublicacaoModelForm
from django.forms.models import inlineformset_factory
from django.utils.http import urlquote
 
def busca(request):
    # import pdb; pdb.set_trace() # forma de incluir um break point na execucao do codigo
    erros = []
    pubs = []
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            erros.append(u'Digite um termo para a busca.')
        #elif len(q) > 80:
        #    erros.append(u'Digite no maximo 20 caracteres.')
        else:
            isbn = validatedISBN10(q) # isbn é igual a variavel q porem a partir de agora somente os digitos
            if isbn:
                pubs = Publicacao.objects.filter(id_padrao=isbn)
            else:
                pubs = Publicacao.objects.filter(titulo__icontains=q) #icontains equivale a um LIKE do sql
    vars_template = {'erros': erros, 'q': q}
    if pubs is not None:
        vars_template['publicacoes'] = pubs
        vars_template['pesquisa'] = True
    return render(request, 'catalogo/busca.html', vars_template)

#def catalogar(request):
#    if request.method != 'POST':
#        formulario = PublicacaoModelForm()
#    else:
#        formulario = PublicacaoModelForm(request.POST)
#        if formulario.is_valid():
#            formulario.save()
#            titulo = formulario.cleaned_data['titulo'] #como consequencia de usar o metodo is_valid é a populacao do objecto cleaned_data
#            return HttpResponseRedirect(reverse('busca')+'?q='+titulo)
#    return render(request, 'catalogo/catalogar.html',
#                {'formulario':formulario})
# formato mais comum de se encontar enquanto que o exemplo acima é mais didatico
# metodo abaixo é quase correspondente ao original acima modificado com a funcao INLINE

def catalogar(request):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    if request.method == 'POST':
        formulario = PublicacaoModelForm(request.POST)
        if formulario.is_valid():
            pub = formulario.save()
            formset = CreditoInlineFormSet(request.POST, instance=pub)
            formset.save()
            titulo = formulario.cleaned_data['titulo'] #como consequencia de usar o metodo is_valid é a populacao do objecto cleaned_data
            return HttpResponseRedirect(reverse('busca')+'?q='+urlquote(titulo))
    else:
        formulario = PublicacaoModelForm()
        formset = CreditoInlineFormSet()
    return render(request, 'catalogo/catalogar.html',
                {'formulario':formulario, 'formset':formset})


def editar(request, pk):
    pub = get_object_or_404(Publicacao, pk=pk)
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)    
    if request.method == 'POST':
        formulario = PublicacaoModelForm(request.POST, instance=pub)
        formset = CreditoInlineFormSet(request.POST, instance=pub)        
        if formulario.is_valid() and formset.is_valid():
            formulario.save()
#            formset = CreditoInlineFormSet(request.POST, instance=pub)
            formset.save()
            titulo = formulario.cleaned_data['titulo'] #como consequencia de usar o metodo is_valid é a populacao do objecto cleaned_data
            return HttpResponseRedirect(reverse('busca')+'?q='+urlquote(titulo))
    else:
        formulario = PublicacaoModelForm(instance=pub)
        formset = CreditoInlineFormSet(instance=pub)
    return render(request, 'catalogo/catalogar.html',
                {'formulario':formulario, 'formset':formset})
            
