import json
import logging
import os
from operator import itemgetter

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from instagram.models import Tag, TagPriority, TextSearch

logger = logging.getLogger(__name__)

connections.create_connection(hosts=[os.getenv('FE_ELASTICSEARCH_HOST')])


@csrf_exempt
def tag_priority(request):
    hashtags = request.POST.get('tags', '').split(' ')
    for hashtag in hashtags:
        try:
            tag = Tag.objects.get(name=hashtag)
            TagPriority.objects.create(tag=tag)
        except Tag.DoesNotExist:
            continue
    return HttpResponse(status=201)


def tags(request):
    tag = request.GET.get('tag')
    s = Search(index="post-index").query("match", tags=tag)
    s.aggs.bucket('wordcloud', 'terms', field='tags', size=35)
    response = s.execute()
    for hit in response:
        logger.debug(hit)

    result = []
    result_count = []
    index = []
    for idx, tag in enumerate(response.aggregations.wordcloud.buckets):
        logger.info(f"{idx}: {tag}")
        result.append(f"#{tag.key}")
        result_count.append(f"{tag.doc_count}".ljust(len(tag.key) + 1))
        index.append(f"{idx+1}".ljust(len(tag.key) + 1))

    r = ' '.join(result) + '\n' + ' '.join(result_count) + '\n' + ' '.join(index) + '\nResults: ' + str(len(result))
    return HttpResponse(r, status=200)


def search(request):
    q = request.GET.get('q', None)
    limit = request.GET.get('limit', '30')
    return search_impl(q, limit)


def search_impl(q, limit):
    try:
        limit = int(limit)
    except ValueError:
        limit = 30

    items = []
    if q:
        s = Search(index="post-index").query("match", tags=q)
        s.aggs.bucket('wordcloud', 'terms', field='tags', size=limit)
        response = s.execute()
        for hit in response:
            logger.info(hit)

        # get tags in our database
        tag_list = []
        for tag in response.aggregations.wordcloud.buckets:
            tag_list.append(tag.key)

        tags_in_database = {}
        unsorted_tags = []
        for tag in Tag.objects.filter(name__in=tag_list):
            if tag.last_count:
                tags_in_database[tag.name] = tag.last_count
            else:
                unsorted_tags.append(tag.name)

        for idx, tag in enumerate(response.aggregations.wordcloud.buckets):
            logger.info(f"{idx}: {tag}")
            if tag.key not in tags_in_database:
                continue
            items.append({
                'name': tag.key,
                'count': tags_in_database[tag.key],
                'doc_count': tag.doc_count,
                'index': idx + 1
            })

        sorted_result = sorted(items, key=itemgetter('count'), reverse=True)
        result = {'items': sorted_result}
        if len(unsorted_tags) > 0:
            result['unsorted_items'] = unsorted_tags
        TextSearch.objects.create(text=q, result=json.dumps(result))
    return JsonResponse(result)
