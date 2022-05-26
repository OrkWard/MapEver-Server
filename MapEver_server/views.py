from django.http import FileResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from .serializers import FileSerializer
from .models import upload_file

def index(request):
    return HttpResponse('<p>Hello! MapEver here.<p><a href=\"https://github.com/OrkWard/WebGIS_Project\">GitHub<a>')

class data(viewsets.ModelViewSet):
    queryset = upload_file.objects.all()
    serializer_class = FileSerializer

    @action(methods=['get', 'post'], detail=True)
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.data.path, 'rb'))
        return response

@api_view(['PUT'])
def overlay(request):
    how = request.data['how']
    # if how in ['intersection', 'union', 'identity', 'symmetric_difference', 'differnce']:
    
    return HttpResponse('overlay finish!' + str(request.data))