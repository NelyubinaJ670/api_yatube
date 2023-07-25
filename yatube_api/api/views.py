from rest_framework import viewsets, permissions

from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет эндпоинта posts/."""
    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Установка автора при создании поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет эндпоинта groups/."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет эндпоинта posts/.../comments/."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        """Возврат набора комментария для запрошенного поста."""
        post_id = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        new_queryset = post_id.comments.select_related('author')
        return new_queryset

    def perform_create(self, serializer):
        """Установка автора и связанного поста при создании комментария."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
