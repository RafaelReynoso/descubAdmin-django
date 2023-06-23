from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from .models import *
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from datetime import date


# Create your views here.

######################## ------USUARIO------ ########################
class UsuarioView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if(id>0):
            usuarios = list(Usuario.objects.filter(id = id).values())
            if len(usuarios)>0:
                usuario = usuarios[0]
                datos = {'message':"Success", 'usuario':usuario}
            else:
                datos = {'message': "Usuario not found..."}
            return JsonResponse(datos)
        else:
            usuarios = list(Usuario.objects.values())
            if len(usuarios)>0:
                datos = {'usuarios':usuarios}
            else:
                datos = {'message': "Usuario not found..."}
            return JsonResponse(datos)
        
    """def get(self, request, id=0):
        if id > 0:
            usuarios = list(Usuario.objects.filter(id=id).values())
            if len(usuarios) > 0:
                usuario = usuarios[0]
                datos = {'message': "Success", 'usuario': usuario}
            else:
                datos = {'message': "Usuario not found..."}
        else:
            usuarios = list(Usuario.objects.values())
            if len(usuarios) > 0:
                for usuario in usuarios:
                    del usuario['usuario']  # Eliminar el campo "usuario" de cada objeto
                datos = usuarios
            else:
                datos = {'message': "Usuario not found..."}

        return JsonResponse(datos, safe=False)"""

        
    

    def post(self,request):
        #print(request.body)
        jd = json.loads(request.body)
        #print(jd)
        Usuario.objects.create(nombre =jd['nombre'], apellidos =jd['apellidos'], usuario =jd['usuario'], email =jd['email'], contrasena =jd['contrasena'], fecha_registro =jd['fecha_registro'],)
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
    def put(self,request, id):
        jd = json.loads(request.body)
        usuarios = list(Usuario.objects.filter(id = id).values())
        if len(usuarios)>0:
            usuario = Usuario.objects.get(id = id)
            usuario.nombre = jd['nombre']
            usuario.apellidos = jd['apellidos']
            usuario.usuario = jd['usuario']
            usuario.email = jd['email']
            usuario.contrasena = jd['contrasena']
            usuario.fecha_registro = jd['fecha_registro']
            usuario.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Usuario not found..."}
        return JsonResponse(datos)

        
    def delete(self,request, id):
        usuarios = list(Usuario.objects.filter(id = id).values())
        if len(usuarios) > 0:
            Usuario.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Usuario not found..."}
        return JsonResponse(datos)
    
######################## ------MURALISTA------ ########################
class MuralistaView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            muralistas = list(Muralista.objects.filter(id=id).values())
            if len(muralistas) > 0:
                muralista = muralistas[0]
                muralista['foto'] = self.convertir_a_base64(muralista['foto'])
                datos = {'message': "Success", 'muralista': muralista}
            else:
                datos = {'message': "Muralista not found..."}
        else:
            muralistas = list(Muralista.objects.values())
            if len(muralistas) > 0:
                for muralista in muralistas:
                    muralista['foto'] = self.convertir_a_base64(muralista['foto'])
                datos = {'message': "Success", 'muralistas': muralistas}
            else:
                datos = {'message': "Muralistas not found..."}
        
        return JsonResponse(datos)
    
    
    def post(self, request):
        jd = json.loads(request.body)
        foto = jd.get('foto', None)
        
        if foto is not None:
            foto_binaria = base64.b64decode(foto)
        else:
            foto_binaria = None
        
        muralista = Muralista(
            nombre=jd.get('nombre', ''),
            apellidos=jd.get('apellidos', ''),
            seudonimo=jd.get('seudonimo', ''),
            foto=foto_binaria,
            celular=jd.get('celular', ''),
            user_instagram=jd.get('user_instagram', ''),
            user_facebook=jd.get('user_facebook', ''),
            email=jd.get('email', '')
        )
        muralista.save()
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        muralistas = list(Muralista.objects.filter(id=id).values())
        
        if len(muralistas) > 0:
            muralista = Muralista.objects.get(id=id)
            muralista.nombre = jd.get('nombre', muralista.nombre)
            muralista.apellidos = jd.get('apellidos', muralista.apellidos)
            muralista.seudonimo = jd.get('seudonimo', muralista.seudonimo)
            muralista.foto = jd.get('foto', muralista.foto)
            muralista.celular = jd.get('celular', muralista.celular)
            muralista.user_instagram = jd.get('user_instagram', muralista.user_instagram)
            muralista.user_facebook = jd.get('user_facebook', muralista.user_facebook)
            muralista.email = jd.get('email', muralista.email)
            
            if muralista.foto:
                muralista.foto = self.convertir_a_base64(muralista.foto)
            
            muralista.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Muralista not found..."}
        
        return JsonResponse(datos)
    

        
    def delete(self,request, id):
        muralistas = list(Muralista.objects.filter(id = id).values())
        if len(muralistas) > 0:
            Muralista.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Muralista not found..."}
        return JsonResponse(datos)
    
    def convertir_a_base64(self, imagen_binaria):
        if imagen_binaria:
            imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
            return imagen_base64
        return None
    
######################## ------MURAL------ ########################
class MuralView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            murales = list(Mural.objects.filter(id=id).values())
            if len(murales) > 0:
                mural = murales[0]
                mural['imagen'] = self.convertir_a_base64(mural['imagen'])
                datos = {'mural': mural}
            else:
                datos = {'message': "Mural not found..."}
        else:
            murales = list(Mural.objects.values())
            if len(murales) > 0:
                for mural in murales:
                    mural['imagen'] = self.convertir_a_base64(mural['imagen'])
                datos = {'message': "Success", 'murales': murales}
            else:
                datos = {'message': "Murales not found..."}
        
        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        imagen = jd.get('imagen', None)
        
        if imagen is not None:
            imagen_binaria = base64.b64decode(imagen)
        else:
            imagen_binaria = None
        
        id_muralista = jd.get('id_muralista', None)
        if id_muralista is not None:
            try:
                muralista = Muralista.objects.get(id=id_muralista)
            except Muralista.DoesNotExist:
                return JsonResponse({'message': 'Muralista does not exist'}, status=400)
        else:
            muralista = None
        
        mural = Mural(
            nombre=jd.get('nombre', ''),
            direccion=jd.get('direccion', ''),
            fecha_creacion=jd.get('fecha_creacion', ''),
            imagen=imagen_binaria,
            descripcion=jd.get('descripcion', ''),
            id_muralista_id=id_muralista,
            latitud=jd.get('latitud', ''),
            altitud=jd.get('altitud', '')
        )
        mural.save()
        datos = {'message': "Success"}
        return JsonResponse(datos)

    
    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            mural = Mural.objects.get(id=id)
        except Mural.DoesNotExist:
            datos = {'message': "Mural not found..."}
            return JsonResponse(datos, status=400)
            
        mural.nombre = jd.get('nombre', mural.nombre)
        mural.direccion = jd.get('direccion', mural.direccion)
        mural.fecha_creacion = jd.get('fecha_creacion', mural.fecha_creacion)
        mural.imagen = jd.get('imagen', mural.imagen)
        mural.descripcion = jd.get('descripcion', mural.descripcion)
        
        id_muralista_id = jd.get('id_muralista_id', None)
        if id_muralista_id is not None:
            try:
                muralista = Muralista.objects.get(id=id_muralista_id)
                mural.id_muralista_id = muralista
            except Muralista.DoesNotExist:
                datos = {'message': "Muralista not found..."}
                return JsonResponse(datos, status=400)

        mural.latitud = jd.get('latitud', mural.latitud)
        mural.altitud = jd.get('altitud', mural.altitud)

        if mural.imagen:
            mural.imagen = self.convertir_a_base64(mural.imagen)

        mural.save()
        datos = {'message': "Success"}

        return JsonResponse(datos)
    
    
    
    def delete(self,request, id):
        murales = list(Mural.objects.filter(id = id).values())
        if len(murales) > 0:
            Mural.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Mural not found..."}
        return JsonResponse(datos)
    
    def convertir_a_base64(self, imagen_binaria):
        if imagen_binaria:
            imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
            return imagen_base64
        return None
    
######################## ------COLOR------ ########################
class ColorView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if(id>0):
            colores = list(Color.objects.filter(id = id).values())
            if len(colores)>0:
                color = colores[0]
                datos = {'message':"Success", 'color':color}
            else:
                datos = {'message': "Color not found..."}
            return JsonResponse(datos)
        else:
            colores = list(Color.objects.values())
            if len(colores)>0:
                datos = {'message':"Success", 'colores':colores}
            else:
                datos = {'message': "Color not found..."}
            return JsonResponse(datos)
        
    def post(self,request):
        #print(request.body)
        jd = json.loads(request.body)
        #print(jd)
        Color.objects.create(nombre =jd['nombre'], codigo =jd['codigo'], red =jd['red'], blue =jd['blue'], green =jd['green'])
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
    def put(self,request, id):
        jd = json.loads(request.body)
        colores = list(Color.objects.filter(id = id).values())
        if len(colores)>0:
            color = Color.objects.get(id = id)
            color.nombre = jd['nombre']
            color.codigo = jd['codigo']
            color.red = jd['red']
            color.blue = jd['blue']
            color.green = jd['green']
            color.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Color not found..."}
        return JsonResponse(datos)
    
    def delete(self,request, id):
        colores = list(Color.objects.filter(id = id).values())
        if len(colores) > 0:
            Color.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Color not found..."}
        return JsonResponse(datos)
    
######################## ------PALETA------ ########################
class PaletaView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if(id>0):
            paletas = list(Paleta.objects.filter(id = id).values())
            if len(paletas)>0:
                paleta = paletas[0]
                datos = {'message':"Success", 'paleta':paleta}
            else:
                datos = {'message': "Paleta not found..."}
            return JsonResponse(datos)
        else:
            paletas = list(Paleta.objects.values())
            if len(paletas)>0:
                datos = {'message':"Success", 'paletas':paletas}
            else:
                datos = {'message': "Paleta not found..."}
            return JsonResponse(datos)
        
    def post(self, request):
        jd = json.loads(request.body)
        
        id_mural = jd.get('id_mural', None)
        if id_mural is not None:
            try:
                mural = Mural.objects.get(id=id_mural)
            except Mural.DoesNotExist:
                return JsonResponse({'message': 'Mural does not exist'}, status=400)
        else:
            return JsonResponse({'message': 'Mural ID is required'}, status=400)
        
        id_color = jd.get('id_color', None)
        if id_color is not None:
            try:
                color = Color.objects.get(id=id_color)
            except Color.DoesNotExist:
                return JsonResponse({'message': 'Color does not exist'}, status=400)
        else:
            return JsonResponse({'message': 'Color ID is required'}, status=400)
        
        paleta = Paleta(
            id_mural_id=id_mural,
            id_color_id=id_color
        )
        paleta.save()
        
        datos = {'message': 'Success'}
        return JsonResponse(datos)
        
    
    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            paleta = Paleta.objects.get(id=id)
        except Paleta.DoesNotExist:
            datos = {'message': "Paleta not found..."}
            return JsonResponse(datos, status=400)
        
        id_mural = jd.get('id_mural', None)
        if id_mural is not None:
            try:
                mural = Mural.objects.get(id=id_mural)
                paleta.id_mural = mural
            except Mural.DoesNotExist:
                datos = {'message': "Mural not found..."}
                return JsonResponse(datos, status=400)
        
        id_color = jd.get('id_color', None)
        if id_color is not None:
            try:
                color = Color.objects.get(id=id_color)
                paleta.id_color_id = color
            except Color.DoesNotExist:
                datos = {'message': "Color not found..."}
                return JsonResponse(datos, status=400)
        
        paleta.save()
        datos = {'message': "Success"}
        return JsonResponse(datos)

    
    def delete(self,request, id):
        paletas = list(Paleta.objects.filter(id = id).values())
        if len(paletas) > 0:
            Paleta.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Paleta not found..."}
        return JsonResponse(datos)

######################## ------SCAN------ ########################
class ScanView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if(id>0):
            scans = list(Scan.objects.filter(id = id).values())
            if len(scans)>0:
                scan = scans[0]
                datos = {'message':"Success", 'paleta':scan}
            else:
                datos = {'message': "Scan not found..."}
            return JsonResponse(datos)
        else:
            scans = list(Scan.objects.values())
            if len(scans)>0:
                datos = {'message':"Success", 'scans':scans}
            else:
                datos = {'message': "Scan not found..."}
            return JsonResponse(datos)
        
    def post(self, request):
        jd = json.loads(request.body)
        
        id_mural = jd.get('id_mural', None)
        if id_mural is not None:
            try:
                mural = Mural.objects.get(id=id_mural)
            except Mural.DoesNotExist:
                return JsonResponse({'message': 'Mural does not exist'}, status=400)
        else:
            return JsonResponse({'message': 'Mural ID is required'}, status=400)
        
        id_usuario = jd.get('id_usuario', None)
        if id_usuario is not None:
            try:
                usuario = Usuario.objects.get(id=id_usuario)
            except Usuario.DoesNotExist:
                return JsonResponse({'message': 'Usuario does not exist'}, status=400)
        else:
            return JsonResponse({'message': 'Usuario ID is required'}, status=400)
        
        fecha_registro = jd.get('fecha_registro', None)
        if fecha_registro is None:
            return JsonResponse({'message': 'Fecha de registro is required'}, status=400)
        
        scan = Scan(
            id_mural_id=id_mural,
            id_usuario_id=id_usuario,
            fecha_registro=fecha_registro
        )
        scan.save()
        
        datos = {'message': 'Success'}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            scan = Scan.objects.get(id=id)
        except Scan.DoesNotExist:
            datos = {'message': "Scan not found..."}
            return JsonResponse(datos, status=400)
        
        id_mural = jd.get('id_mural', None)
        if id_mural is not None:
            try:
                mural = Mural.objects.get(id=id_mural)
                scan.id_mural_id = mural
            except Mural.DoesNotExist:
                datos = {'message': "Mural not found..."}
                return JsonResponse(datos, status=400)
        
        id_usuario = jd.get('id_usuario', None)
        if id_usuario is not None:
            try:
                usuario = Usuario.objects.get(id=id_usuario)
                scan.id_usuario_id = usuario
            except Color.DoesNotExist:
                datos = {'message': "Usuario not found..."}
                return JsonResponse(datos, status=400)
        
        fecha_registro = jd.get('fecha_registro', None)
        if fecha_registro is not None:
            scan.fecha_registro = fecha_registro
        
        scan.save()
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
    def delete(self,request, id):
        scans = list(Scan.objects.filter(id = id).values())
        if len(scans) > 0:
            Scan.objects.filter(id = id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Scan not found..."}
        return JsonResponse(datos)


######################## ------VISTAS------ ########################

def usuarioListado(request):
    usuarioListado = Usuario.objects.all()
    return render(request, "usuarios.html",{"usuarios":usuarioListado})





    

    






