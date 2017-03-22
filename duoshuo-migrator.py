#!/usr/bin/env python

import sys
import json
import argparse
import lxml.etree as etree

def param_setting():
    parser = argparse.ArgumentParser(description='convert from duoshuo JSON exports to WXR (WordPress eXtended RSS) format')
    parser.add_argument('-i', '--input', metavar='FILE', help='read from input file, if not given, use stdin by default')
    parser.add_argument('-o', '--output', metavar='FILE', help='write to output file, if not given, use stdout by default')
    return parser

class Comment(object):

    def __init__(self, id, author_name, author_email, author_url, ip, date, approved, parent_id, content):
        super(Comment, self).__init__()
        self.id = id
        self.author_name = author_name
        self.author_email = author_email
        self.author_url = author_url
        self.ip = ip
        self.date = date
        self.approved = approved
        self.parent_id = parent_id
        self.content = content

class Article(object):

    def __init__(self, id, title, link, identifier, comment_status):
        super(Article, self).__init__()
        self.id = id
        self.title = title
        self.link = link
        self.identifier = identifier
        self.comment_status = comment_status
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

def json2objects(json_obj):
    id_to_article = {}

    articles = json_obj['threads']
    comments = json_obj['posts']

    for art in articles:
        id = int(art['thread_id'])
        title = art['title']
        link = art['url']
        identifier = str(id)
        if 'thread_key' in art and \
           art['thread_key'] is not None and \
           art['thread_key'].strip() != "":
            identifier = art['thread_key']

        id_to_article[id] = Article(id, title, link, identifier, 'open')
    
    for cmnt in comments:
        article_id = cmnt['thread_id']
        id = cmnt['post_id']
        author_name = cmnt['author_name']
        author_email = cmnt['author_email']
        author_url = cmnt['author_url']
        ip = cmnt['ip']
        date = cmnt['created_at'][:19].replace('T', ' ')
        approved = '1'
        parent_ids = cmnt.get('parents', [])
        if parent_ids is None:
            parent_ids = []
        parent_id = '0'
        if len(parent_ids) > 0:
            parent_id = parent_ids[0]
        content = cmnt['message']
        comment = Comment(id, author_name, author_email, author_url, ip, date, approved, parent_id, content)
        if article_id not in id_to_article:
            print >> sys.stderr, "article not found for thread_id %s" %(article_id)
            continue
        id_to_article[article_id].add_comment(comment)

    return id_to_article.values()

def objects2xml(articles):
    wp_ns = 'http://wordpress.org/export/1.0/'
    root = etree.Element('rss', version="2.0", 
        nsmap={'content': 'http://purl.org/rss/1.0/modules/content/',
                'dsq': 'http://www.disqus.com/',
                'dc': 'http://purl.org/dc/elements/1.1/',
                'wp': wp_ns})
    channel = etree.SubElement(root, 'channel')
    for article in articles:
        item = etree.SubElement(channel, 'item')
        if not article.title:
            article.title = 'NULL'
            print >> sys.stderr, "found article without title, id=%s, link=%s" %(article.id, article.link)
        etree.SubElement(item, 'title').text = article.title
        etree.SubElement(item, 'link').text = article.link
        etree.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = etree.CDATA('')
        try:
            etree.SubElement(item, '{http://www.disqus.com/}thread_identifier').text = article.identifier
        except Exception as e:
            print >> sys.stderr, "invalid thread key: %s: %s" % (article.identifier, e)
            continue
        etree.SubElement(item, '{http://www.disqus.com/}thread_identifier').text = article.identifier
        etree.SubElement(item, '{' + wp_ns + '}post_date_gmt').text = ''
        etree.SubElement(item, '{' + wp_ns + '}comment_status').text = article.comment_status

        for comment in article.comments:
            cmnt = etree.SubElement(item, '{' + wp_ns + '}comment')
            remote = etree.SubElement(cmnt, '{http://www.disqus.com/}remote')
            etree.SubElement(remote, '{http://www.disqus.com/}id').text = ''
            etree.SubElement(remote, '{http://www.disqus.com/}avatar').text = ''
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_id').text = str(comment.id)
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_author').text = comment.author_name
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_author_email').text = comment.author_email
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_author_url').text = comment.author_url
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_author_IP').text = comment.ip
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_date_gmt').text = comment.date
            content = comment.content
            if not content:
                content = ''
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_content').text = etree.CDATA(content)
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_approved').text = '1'
            etree.SubElement(cmnt, '{' + wp_ns + '}comment_parent').text = str(comment.parent_id)
    result = etree.tostring(root, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    return result

def main():
    input_file = sys.stdin
    input_file_name = None
    output_file = sys.stdout
    output_file_name = None

    parser = param_setting()
    args = parser.parse_args()

    input_file_name = args.input
    if input_file_name is not None:
        input_file = open(input_file_name)
    content = input_file.read()

    data = json.loads(content)
    articles = json2objects(data)
    result = objects2xml(articles)

    output_file_name = args.output
    if output_file_name is not None:
        output_file = open(output_file_name, 'w')
    output_file.write(result)

if __name__ == '__main__':
    main()
