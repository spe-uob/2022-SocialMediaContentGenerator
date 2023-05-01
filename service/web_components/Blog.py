import os
import re
import shutil
import subprocess

from . import *


class SaveToBlog(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/save_to_blog', 'SaveToBlog', ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data is None:
            return abort(400)
        content = data['content']
        title = data['title']
        images = self.get_image_list(content)
        content = self.convert_image_to_md(content)
        markdown_content = f"---\ntitle: {title}\n---\n\n"
        markdown_content += content
        blog_root = self.env.config['blog_root']
        open(os.path.join(blog_root, "source/_posts", f"{title}.md"), 'w').write(markdown_content)
        for image in images:
            if not os.path.exists(os.path.join(blog_root, "source/images", os.path.basename(image))):
                shutil.copy(image, os.path.join(blog_root, "source/images", os.path.basename(image)))
        server_app = self.env.api_server.app
        with server_app.app_context():
            pwd = os.getcwd()
            os.chdir(blog_root)
            returned_value = subprocess.run("hexo generate", shell=True, stdout=subprocess.PIPE)
            os.chdir(pwd)
        return {"status": 0, "output": returned_value.stdout.decode('utf-8')}

    @staticmethod
    def convert_image_to_md(content):
        content = re.sub(r"(<)(.*)>", '\n![\\2](\\2)\n', content)
        content = re.sub(r"\n{2,}", '', content)
        return content

    @staticmethod
    def get_image_list(content):
        result = re.findall(r"<.*>", content)
        images = []
        for item in result:
            images.append(item[1:-1])
        return images


class LoadBlog(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/load_blog', 'LoadBlog', ['GET'])
        self.env = env

    def view(self):
        blog_file = request.args.get('filename')
        blog_root = self.env.config['blog_root']
        blog_content = open(os.path.join(blog_root, "source/_posts", blog_file), 'r').read()
        blog_content = re.sub('^\n*', '', re.sub(r"^.*---", '', blog_content, flags=re.S))
        blog_content = self.restore_image(blog_content)
        return {"status": 0, "content": blog_content}

    @staticmethod
    def restore_image(content):
        content = re.sub(r"!\[(.*)\]\((.*)\)", f"<\\2>", content)
        return content


class BlogList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/blog_list', 'BlogList', ['GET'])
        self.env = env

    def view(self):
        blog_root = self.env.config['blog_root']
        blog_list = [x for x in os.listdir(os.path.join(blog_root, "source/_posts")) if x.endswith('.md')]
        return {"status": 0, "content": blog_list}


class BlogServerUrl(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/blog_server_url', 'BlogServerUrl', ['GET'])
        self.env = env

    def view(self):
        return {"status": 0, "content": self.env.config['blog_server_url']}
