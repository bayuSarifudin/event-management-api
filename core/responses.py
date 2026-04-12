from rest_framework.response import Response

def success_response(data=None, message="Success", status_code=200, meta=None):
    return Response({
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
        "meta": meta
    }, status=status_code)


def error_response(errors=None, message="Validation error", status_code=400):
    return Response({
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
        "meta": None
    }, status=status_code)
    
def paginated_response(paginator, serializer_data, message="Success"):
    return Response({
        "success": True,
        "message": message,
        "data": serializer_data,
        "errors": None,
        "meta": {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
        }
    })