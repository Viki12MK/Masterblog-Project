import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'John Doe', 'title': 'Second Post', 'content': 'This is another post.'}
]

data_file = 'storage.json'


def save_posts(posts):
    with open(data_file, 'w') as file:
        json.dump(posts, file)
    return posts


def load_posts():
    with open(data_file, 'r') as file:
        return json.load(file)


blog_posts = load_posts()


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST', 'DELETE'])
def delete(post_id):
    if request.method == 'POST' or request.method == 'DELETE':
        # Find the blog post with the given id and remove it from the list
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break

        # Save the updated file
        save_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        for post in blog_posts:
            if post['id'] == post_id:
                post['title'] = title
                post['author'] = author
                post['content'] = content
                break

        # Save the updated post to the file
        save_posts(blog_posts)

        # Redirect back to index
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    # Find the blog post with the given id and increment the 'like' value
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    # Save the updated posts to the file
    save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
