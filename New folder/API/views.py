from functools import reduce
from operator import and_
from django.db.models import Q
from .models import MyModel
import re
from .serializers import MyModelSerializer
from rest_framework import generics, filters
from rest_framework.filters import SearchFilter
def apply_operator(field, operator, value):
    if operator == 'eq':
        return Q(**{f"{field}": value})
    elif operator == 'ne':
        return ~Q(**{f"{field}": value})
    elif operator == 'gt':
        return Q(**{f"{field}__gt": value})
    elif operator == 'lt':
        return Q(**{f"{field}__lt": value})
    else:
        return False

    # def parse_expression(expression):
    #     for operator in ['and', 'or']:
    #         subexpressions = re.split(fr'\s*{operator}\s*', expression, flags=re.I)
    #         if len(subexpressions) > 1:
    #             return Q(**{f'{operator}_'.join([parse_expression(subexpr) for subexpr in subexpressions]): True})
        
    #     for field, operator, value in re.findall(r'(\w+)\s*(eq|ne|gt|lt)\s*(\S+)', expression):
    #         if field not in allowed_fields:
    #             raise ValueError(f"Field '{field}' is not allowed for filtering.")
    #         return Q(**{f'{field}__{operator}': value})
        
    #     raise ValueError(f"Invalid expression: {expression}")

    # try:
    #     return parse_expression(phrase)
    # except ValueError:
    #     raise ValueError("Invalid search phrase.")






class LCTeacherAPI(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    filter_backends = [SearchFilter]
    # search_fields = ['=date','=distance']

    def get_queryset(self):
        date = None
        d1 = None
        d2 = None
        # queryset = super().get_queryset()
        queryset = MyModel.objects.all()
        search = self.request.query_params.get('search', '')

        
        search_terms = [term.strip() for term in search.split('AND')]
        print(len(search_terms))
        
        if len(search_terms) >= 2:
            date = search_terms[0]
            date = [term.strip() for term in date.split(' ')]
            print(date[0])
            print(date[1])
            date = apply_operator('date', date[0], date[1])
            print(date)
            distance_search_terms = [term.strip() for term in search_terms[1].split('OR')]
            if len(distance_search_terms) >= 2:
                d1 = distance_search_terms[0]
                d1 = [term.strip() for term in d1.split(' ')]
                print(d1[0])
                print(d1[1])
                d1 = apply_operator('distance', d1[0], d1[1])
                print(d1)
                d2 = distance_search_terms[1]
                d2 = [term.strip() for term in d2.split(' ')]
                print(d2[0])
                print(d2[1])
                d2 = apply_operator('distance', d2[0], d2[1])
                print(d2)
            else:
                d1 = distance_search_terms[0]
                d1 = [term.strip() for term in d1.split(' ')]
                print(d1[0])
                print(d1[1])
                d1 = apply_operator('distance', d1[0], d1[1])
                print(d1)
        else:
            # date = search_terms[0]
            try:
                # http://127.0.0.1:8000/tecAPI/?search=gt%202023-10-10
                date = search_terms[0]
                date = [term.strip() for term in date.split(' ')]
                print(date[0])
                print(date[1])
                date = apply_operator('date', date[0], date[1])
                print(date)
                # queryset = queryset.filter(Q(date=date))
                queryset = queryset.filter(date)

                return queryset
            except:
                # http://127.0.0.1:8000/tecAPI/?search=gt%2050ORlt%2020
                date = search_terms[0]
                distance_search_terms = [term.strip() for term in date.split('OR')]
                if len(distance_search_terms) >= 2:
                    d1 = distance_search_terms[0]
                    d1 = [term.strip() for term in d1.split(' ')]
                    print(d1[0])
                    print(d1[1])
                    d1 = apply_operator('distance', d1[0], d1[1])
                    print(d1)
                    d2 = distance_search_terms[1]
                    d2 = [term.strip() for term in d2.split(' ')]
                    print(d2[0])
                    print(d2[1])
                    d2 = apply_operator('distance', d2[0], d2[1])
                    print(d2)
                    queryset = queryset.filter(d1 | d2)
                else:
                    d1 = distance_search_terms[0]
                    d1 = [term.strip() for term in d1.split(' ')]
                    print(d1[0])
                    print(d1[1])
                    d1 = apply_operator('distance', d1[0], d1[1])
                    print(d1)
                    
                
                    queryset = queryset.filter(d1)
                
                # queryset = queryset.filter((Q(distance=d1) | Q(distance=d2)))
                return queryset
            finally:
                return queryset
        if search is not None:
            # http://127.0.0.1:8000/tecAPI/?search=gt%202023-10-1ANDgt%2010ORlt%2040
            queryset = queryset.filter(date & d1 | d2)

        return queryset

    
class LCTeacherAPI2(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['=date','=distance']

    def get_queryset(self):
        
        date = None
        d1 = None
        d2 = None

        search = self.kwargs.get('search')
        queryset = MyModel.objects.all()
        
        search_terms = [term.strip() for term in search.split('AND')]
        print(len(search_terms))

        if len(search_terms) >= 2:
            date = search_terms[0]
            date = [term.strip() for term in date.split(' ')]
            print(date[0])
            print(date[1])
            date = apply_operator('date', date[0], date[1])
            print(date)
            distance_search_terms = [term.strip() for term in search_terms[1].split('OR')]
            if len(distance_search_terms) >= 2:
                d1 = distance_search_terms[0]
                d1 = [term.strip() for term in d1.split(' ')]
                print(d1[0])
                print(d1[1])
                d1 = apply_operator('distance', d1[0], d1[1])
                print(d1)
                d2 = distance_search_terms[1]
                d2 = [term.strip() for term in d2.split(' ')]
                print(d2[0])
                print(d2[1])
                d2 = apply_operator('distance', d2[0], d2[1])
                print(d2)
            else:
                d1 = distance_search_terms[0]
                d1 = [term.strip() for term in d1.split(' ')]
                print(d1[0])
                print(d1[1])
                d1 = apply_operator('distance', d1[0], d1[1])
                print(d1)
        else:
            # date = search_terms[0]
            try:
                date = search_terms[0]
                date = [term.strip() for term in date.split(' ')]
                print(date[0])
                print(date[1])
                date = apply_operator('date', date[0], date[1])
                print(date)
                # http://127.0.0.1:8000/tecAPI2/gt%202023-10-1/
                
                # queryset = queryset.filter(Q(date=date))
                queryset = queryset.filter(date)
                return queryset
            except:
                d1 = search_terms[0]
                d1 = [term.strip() for term in d1.split(' ')]
                print(d1[0])
                print(d1[1])
                d1 = apply_operator('distance', d1[0], d1[1])
                print(d1)
                # http://127.0.0.1:8000/tecAPI2/lt%2025/
                
                # queryset = queryset.filter(Q(distance=date))
                queryset = queryset.filter(d1)

                return queryset
        if search is not None:
            # queryset = queryset.filter(Q(date=date) & (Q(distance=d1) | Q(distance=d2)))
            queryset = queryset.filter(date & d1 | d2)

        return queryset
    
# for retrieve,Update and delete/destroy where PK is required
class RUDTeacherAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs) # use update for Complete update// partial_update for parchial update
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
