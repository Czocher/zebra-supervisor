from judge.models import Submission, Result, Tests
from rest_framework import serializers


class TestsTimestampsSerializer(serializers.ModelSerializer):
    input = serializers.CharField(source='input.timestamp', read_only=True)
    output = serializers.CharField(source='output.timestamp', read_only=True)
    config = serializers.CharField(source='config.timestamp', read_only=True)

    class Meta:
        model = Tests
        fields = ('input', 'output', 'config')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('mark', 'returncode', 'time')


class SubmissionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_codename',
                                   read_only=True)
    problem = serializers.CharField(source='problem.codename',
                                    read_only=True)
    active = serializers.BooleanField(source='contest._is_active',
                                      read_only=True)
    language = serializers.CharField(source='get_language_display',
                                     read_only=True)
    results = ResultSerializer(many=True, required=False)
    error = serializers.BooleanField(write_only=True)

    def update(self, instance, validated_data):
        results = validated_data.pop('results')
        for result in results:
            res = Result(
                submission=instance,
                mark=result.get('mark'),
                returncode=result.get('returncode'),
                time=result.get('time')
            )
            res.save()
        return instance

    class Meta:
        model = Submission
        fields = ('id', 'status', 'problem', 'active', 'language', 'source',
                  'score', 'error', 'results', 'compilelog')
        write_only_fields = ('compilelog', )
        read_only_fields = ('source', 'id', 'score')


class PrintRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_codename',
                                   read_only=True)
    author = serializers.CharField(source='author.username',
                                   read_only=True)
    contest = serializers.CharField(source='contest.name',
                                    read_only=True)
    problem = serializers.CharField(source='problem.codename',
                                    read_only=True)
    language = serializers.CharField(source='get_language_display',
                                     read_only=True)
    error = serializers.BooleanField(write_only=True)

    class Meta:
        model = Submission
        fields = ('id', 'status', 'author', 'contest', 'problem', 'language',
                  'source', 'error',)
        read_only_fields = ('source', 'id',)
