# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from datetime import *
from .forms import *
from .models import *
# Create your views here.

def register(request):
    form=registroForm(request.POST or None)
    if form.is_valid():
        save_it=form.save(commit=False)
        save_it.save()
        user=request.session.get('username')
        exist=request.session.get('user_exist')
        if user is None:
            exist=False
        return HttpResponseRedirect('/../')
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    if user is None:
        exist=False

    user_motel=request.session.get('username_motel')
    exist_motel=request.session.get('user_motel_exist')
    if user_motel is None:
        exist_motel=False


    return render_to_response("registro.html",locals(), context_instance=RequestContext(request))

def home(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    if user is None:
        exist=False

    user_motel=request.session.get('username_motel')
    exist_motel=request.session.get('user_motel_exist')
    if user_motel is None:
        exist_motel=False
    return render_to_response("home.html",locals(), context_instance=RequestContext(request))

def login(request):
    form=loginForm(request.POST or None)
    user_exist=False
    user_not_registered=False
    if request.method == 'POST':

        if form.is_valid():
            username=form.cleaned_data['nombre_de_usuario']
            contr=form.cleaned_data['password']
            possible_user= usuario.objects.filter(nombre_de_usuario=username,password=contr)
            user_exist =len(possible_user) > 0

            if user_exist:
                request.session['username']=username
                request.session['user_exist']=user_exist
                exist = user_exist
                return HttpResponseRedirect('/../')
            else:
                user_not_registered= not user_exist
    exist=user_exist
    return render_to_response("login.html",locals(), context_instance=RequestContext(request))

def login_motel(request):
    form=loginMotelForm(request.POST or None)
    user_motel_exist=False
    user_not_registered=False
    if request.method == 'POST':

        if form.is_valid():
            username=form.cleaned_data['nombre_de_usuario']
            contr=form.cleaned_data['password']
            possible_user= usuarios_moteles.objects.filter(nombre_de_usuario=username,password=contr)
            user_motel_exist =len(possible_user) > 0

            if user_motel_exist:
                request.session['username_motel']=username
                request.session['user_motel_exist']=user_motel_exist
                exist_motel = user_motel_exist
                return HttpResponseRedirect('/../')
            else:
                user_not_registered= not user_motel_exist
    exist_motel=user_motel_exist
    return render_to_response("login_motel.html",locals(), context_instance=RequestContext(request))


def logout(request):
    try:
        user=request.session.get('username')
        user_motel=request.session.get('username_motel')
        if user is not None:
            del request.session['username']
        if user_motel is not None:
            del request.session['username_motel']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def amistades(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    user_info= usuario.objects.get(nombre_de_usuario=user)
    user_id=user_info.pk
    amis= amistad.objects.filter(Q(usuario_1=user_id) | Q(usuario_2=user_id))
    sol_amis=solicitudesDeAmistad.objects.filter(solicitante=user_id)
    amigos=[]
    for am in amis:
        if (am.usuario_1).nombre_de_usuario == user :
            amigos.append(str(am.usuario_2))
        else:
            amigos.append(str(am.usuario_1))
    solicitudes_de_amistad=[]
    for s_a in sol_amis:
        solicitudes_de_amistad.append(str(s_a.solicitado))

    has_friends=len(amis)>0
    has_made_frequest=len(sol_amis)>0


    if user is None:
        exist=False
    return render_to_response("amistades.html",locals(), context_instance=RequestContext(request))

def solicitar_amistad(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    form=solicitudAmistadForm(request.POST or None)

    if request.method == 'POST':
       solicitado=request.POST.get("solicitado")
       if len(usuario.objects.filter(nombre_de_usuario=solicitado))>0:
            user1_info= usuario.objects.get(nombre_de_usuario=user)
            user2_info= usuario.objects.get(nombre_de_usuario=solicitado)
            user_info= usuario.objects.get(nombre_de_usuario=user)
            user_pk=user_info.pk
            friend_request_for_user=solicitudesDeAmistad.objects.filter(solicitado=user_pk)
            for request in friend_request_for_user:
                if request.solicitante==user2_info:
                    request.delete()
                    amist=amistad.create(user1_info,user2_info)
                    amist.save()
                    return HttpResponseRedirect('/../')
            if len(amistad.objects.filter(Q(usuario_1=user1_info.pk) | Q(usuario_2=user1_info.pk),Q(usuario_1=user2_info.pk) | Q(usuario_2=user2_info.pk)))==0:
                sol=solicitudesDeAmistad.create(user1_info,user2_info)
                sol.save()
       return HttpResponseRedirect('/../')

    return render_to_response("solicitar_amistad.html",locals(), context_instance=RequestContext(request))


def mis_reservas(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    if user is None:
        exist=False
    current_user = usuario.objects.get(nombre_de_usuario=user)              
    lista_reservas=reservas.objects.filter(usuario=current_user.id)
    if user is None:
        exist=False
    return render_to_response("mis_reservas.html",locals(), context_instance=RequestContext(request))
def contacto(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    if user is None:
        exist=False
    user_motel=request.session.get('username_motel')
    exist_motel=request.session.get('user_motel_exist')
    if user_motel is None:
        exist_motel=False
    return render_to_response("contacto.html",locals(), context_instance=RequestContext(request))
def moteles(request):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    lista_moteles=motel.objects.all()
    if user is None:
        exist=False
    return render_to_response("moteles.html",locals(), context_instance=RequestContext(request))
def info_motel(request, motel_id):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    motel_info=motel.objects.get(id=motel_id)
    lista_piezas=pieza.objects.filter(motel=motel_id)
    if user is None:
        exist=False
    return render_to_response("info_motel.html",locals(), context_instance=RequestContext(request))
def info_pieza(request, pieza_id):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    pieza_info=pieza.objects.get(id=pieza_id)
    if user is None:
        exist=False
    return render_to_response("info_pieza.html",locals(), context_instance=RequestContext(request))

def calcularDisponibilidad(pieza_id, f1, h1, f2, h2):
        dt1 = datetime.combine(f1, h1);
        dt2 = datetime.combine(f2, h2);
        lista_reservas = reservas.objects.filter(pieza=pieza_id)
        pieza_buscada = pieza.objects.get(id=pieza_id)
        disponibilidad = pieza_buscada.piezas_disponibles
        for reserva in lista_reservas:
            dt1_reserva = datetime.combine(reserva.fecha1, reserva.hora1)
            dt2_reserva = datetime.combine(reserva.fecha2, reserva.hora2)
            if(dt1 > dt1_reserva and dt1 < dt2_reserva) or (dt2 > dt1_reserva and dt2 < dt2_reserva) or (dt1 == dt1_reserva or dt2== dt2_reserva):
                disponibilidad = disponibilidad-1
        print disponibilidad
        return disponibilidad        

def crear_reserva(request, pieza_id):
    user=request.session.get('username')
    exist=request.session.get('user_exist')
    if user is None:
        exist=False
    if request.method == 'POST':
        form = reservaForm(request.POST)
        if form.is_valid():
            #guardamos la reserva sólo si hay disponibilidad
            pieza_reserva = pieza.objects.get(id=pieza_id)
            cantidad_piezas = pieza_reserva.piezas_disponibles
            fecha_1=form.cleaned_data['fecha1']
            hora_1=form.cleaned_data['hora1']
            fecha_2=form.cleaned_data['fecha2']
            hora_2=form.cleaned_data['hora2']
            disponibilidad = calcularDisponibilidad(pieza_id, fecha_1, hora_1, fecha_2, hora_2)
            if(disponibilidad > 0):
                user_name=request.session.get('username')
                user = usuario.objects.get(nombre_de_usuario=user_name)
                motel_reserva=motel.objects.get(nombre_del_motel=form.cleaned_data['motel'])
                fecha_1=form.cleaned_data['fecha1']
                hora_1=form.cleaned_data['hora1']
                fecha_2=form.cleaned_data['fecha2']
                hora_2=form.cleaned_data['hora2']
                nueva_reserva = reservas(motel=motel_reserva, usuario=user, pieza = pieza_reserva, 
                    fecha1=fecha_1, hora1=hora_1,
                    fecha2=fecha_2, hora2=hora_2)
                nueva_reserva.save()           
                lista_reservas=reservas.objects.filter(usuario=user.id)
                return render_to_response("reserva_realizada.html",{'nueva_reserva':nueva_reserva}, context_instance=RequestContext(request))
                
            else:
                return render(request, 'crear_reserva.html', {'form': form, 'lista_reservas': lista_reservas, 'no_disponibilidad':True})
        else:
            return HttpResponseRedirect('/')    
    else:
        pieza_obj = pieza.objects.get(id=pieza_id)
        motel_obj = motel.objects.get(id=pieza_obj.motel.id)
        form = reservaForm(initial={'motel':motel_obj.nombre_del_motel, 'pieza':pieza_obj.nombre_de_la_pieza})
        lista_reservas = reservas.objects.filter(pieza = pieza_id)
        #me tinca q esto es ultra poco seguro, pero la entrega es hoy.
    return render(request, 'crear_reserva.html', {'form': form, 'lista_reservas': lista_reservas})

    
