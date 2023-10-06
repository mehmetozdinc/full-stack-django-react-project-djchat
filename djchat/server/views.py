from rest_framework import viewsets
from .models import Server
from .serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs

class ServerListViewSet(viewsets.ViewSet):
    # Initial queryset to retrieve all Server objects
    queryset = Server.objects.all()

    # Custom method to handle GET requests for retrieving a list of servers
    @server_list_docs
    def list(self, request):
        """Retrieves a list of servers based on specified query parameters.

        This method allows filtering servers based on various criteria such as category,
        server ID, user membership, and quantity of results. Additionally, it provides
        the option to include the number of members in each server when requested.

        Args:
        request (rest_framework.request.Request): The HTTP request object containing query parameters.

        Raises:
        AuthenticationFailed: If authentication is required and the user is not authenticated.
        ValidationError: If there is a validation error in the provided query parameters.

        Returns:
        rest_framework.response.Response: JSON response containing the serialized server data.

        Query Parameters:
        category (str, optional): Filter servers by category name.
        by_serverid (str, optional): Filter servers by server ID.
        by_user (bool, optional): If 'true', filter servers by the requesting user.
        qty (int, optional): Limit the number of servers returned.
        with_num_members (bool, optional): If 'true', include the number of members in each server.

        Raises:
        AuthenticationFailed: If authentication is required and the user is not authenticated.
        ValidationError: If there is a validation error in the provided query parameters.

        Returns:
        rest_framework.response.Response: JSON response containing the serialized server data.

        Example Usage:
        To retrieve servers in a specific category:
        ```
        GET /api/servers/?category=gaming
        ```

        To retrieve a server by its ID and include the number of members:
        ```
        GET /api/servers/?by_serverid=123&with_num_members=true
        ```

        To filter servers by user membership:
        ```
        GET /api/servers/?by_user=true
        ```

        To limit the number of results:
        ```
        GET /api/servers/?qty=10
        ```

        To combine multiple filters:
        ```
        GET /api/servers/?category=gaming&by_user=true&qty=5
        ```
        """

        # Retrieve query parameters from the request
        category = request.query_params.get("category")
        by_serverid = request.query_params.get("by_serverid")
        by_user = request.query_params.get("by_user") == "true"
        qty = request.query_params.get("qty")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Check if authentication is required and user is not authenticated
        if (by_user or by_serverid) and not request.user.is_authenticated:
            raise AuthenticationFailed

        # Filter queryset based on category parameter
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter queryset based on user parameter
        if by_user:
            user = request.user.id
            self.queryset = self.queryset.filter(member=user)

        # Annotate queryset with the number of members if requested
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))
        
        # Limit queryset results based on qty parameter
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Filter queryset based on server ID if provided
        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                # Raise validation error if server with the provided ID does not exist
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} does not found")
            except ValueError:
                raise ValidationError(detail="Server value error")

        # Serialize the queryset and return the data as a JSON response
        serializer = ServerSerializer(self.queryset, many=True, context={"with_num_members": with_num_members})
        return Response(serializer.data)
