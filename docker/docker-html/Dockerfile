FROM sphinxdoc/sphinx

# 通过镜像标签声明了作者信息
LABEL maintainer="Michael Miao(1247508314@qq.com)"
LABEL Description="Image to build the Sphinx documentation"


RUN set -eux; \
    # 新镜像构建成功以后创建指定目录
    # mkdir --parents /usr/share/man/man1; \
    # DEBIAN_FRONTEND=noninteractive : 直接运行命令，而无需向用户请求输入（所有操作都是非交互式的）
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes -f --no-install-recommends \
    openjdk-11-jre-headless \
    openjdk-11-jre \
    plantuml

# --no-cache-dir 缩小Docker Image 的大小
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pipenv \
    && pip install --no-cache-dir pipfile-requirements

# # Install the required packages for Python Sphinx
COPY Pipfile ./
RUN pipfile2req Pipfile > requirements.txt \
 && pip install --no-cache-dir -r requirements.txt

# CMD ["make", "html"]
