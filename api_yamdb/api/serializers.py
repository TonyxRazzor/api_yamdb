from rest_framework import serializers
# from ... import Title, Category, Genre, Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        if Review.objects.filter(
                title=title,
                author=author).exists() and request.method == 'POST':
            raise ValidationError('Можно оставить только один отзыв на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
