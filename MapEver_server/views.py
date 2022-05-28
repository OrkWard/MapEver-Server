from django.http import FileResponse, HttpResponse
from django.core.files import File
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .serializers import FileSerializer
from .models import upload_file
import geopandas as gpd
import os

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
# 叠加分析
def overlay(request):
    # 请求为一个dict，包含了操作文件所需的信息
    how = request.data['how']
    if how in ['intersection', 'union', 'identity', 'symmetric_difference', 'differnce']:
        # geopandas操作
        source_file = upload_file.objects.get(id=request.data['source']).data
        source = gpd.read_file(source_file)
        object_file = upload_file.objects.get(id=request.data['object']).data
        object = gpd.read_file(object_file)
        result = gpd.overlay(source, object, how=how)
        # 该文件为临时文件，记得删除，数据库存取时会自动向指定目录写入
        result.to_file(request.data['output'], driver='GeoJSON')

        # 数据库操作和返回请求，模仿即可
        with open(request.data['output'], 'rb') as f:
            # 写入
            new_record = upload_file(name=request.data['output'], form='vector', data=File(f))
            new_record.save()
        # 线性化
        serializer = FileSerializer(upload_file.objects.get(pk=new_record.id))
        # 删除临时文件
        os.remove(request.data['output'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

#   联合分析
def sjoin(request):
    how = request.data['how']
    if how in ['left', 'right', 'inner']:
        # geopandas操作
        left_file = upload_file.objects.get(id=request.data['source']).data
        left = gpd.read_file(left_file)
        right_file = upload_file.objects.get(id=request.data['object']).data
        right = gpd.read_file(right_file)
        result = gpd.sjoin(left, right, how=how)
        # 该文件为临时文件，记得删除，数据库存取时会自动向指定目录写入
        result.to_file(request.data['output'], driver='GeoJSON')

        # 数据库操作和返回请求，模仿即可
        with open(request.data['output'], 'rb') as f:
            # 写入
            new_record = upload_file(name=request.data['output'], form='vector', data=File(f))
            new_record.save()
        # 线性化
        serializer = FileSerializer(upload_file.objects.get(pk=new_record.id))
        # 删除临时文件
        os.remove(request.data['output'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

# 裁剪分析
def clip(request):
    gdf_file = upload_file.objects.get(id=request.data['source']).data
    gdf = gpd.read_file(gdf_file)
    mask_file = upload_file.objects.get(id=request.data['object']).data
    mask = gpd.read_file(mask_file)
    result = gpd.clip(gdf, mask)
    # 该文件为临时文件，记得删除，数据库存取时会自动向指定目录写入
    result.to_file(request.data['output'], driver='GeoJSON')

    # 数据库操作和返回请求，模仿即可
    with open(request.data['output'], 'rb') as f:
        # 写入
        new_record = upload_file(name=request.data['output'], form='vector', data=File(f))
        new_record.save()
    # 线性化
    serializer = FileSerializer(upload_file.objects.get(pk=new_record.id))
    # 删除临时文件
    os.remove(request.data['output'])
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 中心点提取
def centroid(request):
    source_file = upload_file.objects.get(id=request.data['source']).data
    source = gpd.read_file(source_file)
    result = source.centroid
    # 该文件为临时文件，记得删除，数据库存取时会自动向指定目录写入
    result.to_file(request.data['output'], driver='GeoJSON')

    # 数据库操作和返回请求，模仿即可
    with open(request.data['output'], 'rb') as f:
        # 写入
        new_record = upload_file(name=request.data['output'], form='vector', data=File(f))
        new_record.save()
    # 线性化
    serializer = FileSerializer(upload_file.objects.get(pk=new_record.id))
    # 删除临时文件
    os.remove(request.data['output'])
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 重投影
def to_src(request):
    how = request.data['how']
    source_file = upload_file.objects.get(id=request.data['source']).data
    source = gpd.read_file(source_file)
    result = source.to_crs(crs=how)
    # 该文件为临时文件，记得删除，数据库存取时会自动向指定目录写入
    result.to_file(request.data['output'], driver='GeoJSON')

    # 数据库操作和返回请求，模仿即可
    with open(request.data['output'], 'rb') as f:
        # 写入
        new_record = upload_file(name=request.data['output'], form='vector', data=File(f))
        new_record.save()
    # 线性化
    serializer = FileSerializer(upload_file.objects.get(pk=new_record.id))
    # 删除临时文件
    os.remove(request.data['output'])
    return Response(serializer.data, status=status.HTTP_201_CREATED)
