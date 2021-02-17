FROM sphinxdoc/sphinx-latexpdf

# 通过镜像标签声明了作者信息
LABEL maintainer="Michael Miao(1247508314@qq.com)"
LABEL Description="Image to build the Sphinx documentation"


RUN set -eux; \
    # 新镜像构建成功以后创建指定目录
    # 为什么要这么做，参考 
    # https://github.com/geerlingguy/ansible-role-java/issues/64#issuecomment-393299088
    # https://askubuntu.com/questions/107783/failing-package-manager
    # https://askubuntu.com/questions/983727/many-dependency-problems-installing-jdk-and-netbeans
    # https://github.com/puckel/docker-airflow/issues/182
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=863199
    # 或者 使用 sudo apt-get install -f 
    mkdir --parents /usr/share/man/man1; \
    # DEBIAN_FRONTEND=noninteractive : 直接运行命令，而无需向用户请求输入（所有操作都是非交互式的）

    # downloads info on whether there are updates available
    apt-get update \
    # emoves downloaded installation packages that were cached
    && apt-get clean \

    # uninstalls packages that were once needed for other packages (without the user specifying/knowing about them) but now nothing needs them anymore.
    && apt-get autoremove \

    # ## attempts to fix any broken dependencies between packages. 
    # && apt-get install -f \

    # ## installs packages that were already unpacked but not finished installing
    # && dpkg --configure -a \

    && DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes -f --no-install-recommends \
    plantuml \

    && apt-get install openjdk-11-jre

# --no-cache-dir 缩小Docker Image 的大小
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pipenv \
    && pip install --no-cache-dir pipfile-requirements

# # Install the required packages for Python Sphinx
COPY Pipfile ./
RUN pipfile2req Pipfile > requirements.txt \
 && pip install --no-cache-dir -r requirements.txt

CMD ["make", "latexpdf"]
