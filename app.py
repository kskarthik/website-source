import markdown

from flask import Flask, render_template
from os import listdir

app = Flask(__name__)

BLOG_CONTENT_DIR = 'content/blog'

@app.route('/')
def home():
    return render_template('index.html')

def parse_post(post):
    y, m, d, *title = post[:-3].split('-')
    slug = '-'.join(title)
    return {'url': f'/blog/{y}/{m}/{d}/{slug}/', 'title': ' '.join(title)}

@app.route('/blog/')
def blog():
    posts = sorted(listdir(BLOG_CONTENT_DIR), reverse=True)
    posts = map(parse_post, posts)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<y>/<m>/<d>/<title>/')
def blog_post(y, m, d, title):
    post_path = f'{y}-{m}-{d}-{title}'
    with open(f'{BLOG_CONTENT_DIR}/{post_path}.md', 'r') as f:
        text = f.read()
        _, header, body = text.split('---')
        for h in header:
            if h.startswith('title'):
                title = h.split('title:')[0].strip()
        html = markdown.markdown(body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        return render_template('post.html', title=title, html=html)
