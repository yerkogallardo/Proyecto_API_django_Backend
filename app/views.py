from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAdminUser
from app.api.serializers import ReporteSerializer, MedidasSerializer, OrganismoSectorialSerializer
from app.models import Usuario, Reporte, Medidas, OrganismoSectorial
# Create your views here.


class MedidasViewSet(viewsets.ModelViewSet):
    serializer_class = MedidasSerializer
    queryset = Medidas.objects.all()
    permission_classes = [IsAdminUser]



class ReporteViewSet(viewsets.ModelViewSet):
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    queryset = Reporte.objects.all()

    def get_queryset(self):
        """
        Filtramos los reportes para que cada usuario solo vea los suyos,
        excepto si tiene permisos especiales
        """
        user = self.request.user

        if user.has_perm('app.can_view_all_reports'):
            return Reporte.objects.all()
        return Reporte.objects.filter(usuario=user)
    
    def get_tipos_documentos_permitidos(self):
        """
        Retorna las medidas para el tipo de ente del usuario actual
        """
        return Medidas.objects.filter(
            tipo_ente=self.request.user.organismos_permitidos
        )
    
