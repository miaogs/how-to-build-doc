.. _support_markdown:

支持 markdown 语法
======================
`Sphinx` 本身不支持 `.md` 文件生成文档，和 :ref:`change_html_theme` 一样需要我们使用第三方库 `recommonmark` 进行转换。

.. _install_mark_env:

安装 mark 环境
~~~~~~~~~~~~~~

:: 

    pip install recommonmark
    # pip install recommonmark -i https://pypi.douban.com/simple


修改 conf.py 
~~~~~~~~~~~~~~

1. **增加扩展**

    ::

        extensions = ['recommonmark']


    结合 ，修改之后变为
    ::

        extensions = [
        "sphinx_rtd_theme",
        "recommonmark"
        ]

#. **修改 source_suffix 变量**
    如果要使用除 `.md` 以外的扩展名的 `Markdown` 文件，请调整 `source_suffix` 变量。
    下面的示例配置 `Sphinx` 将所有扩展名为 `.md` 和 `.txt` 的文件解析为 `Markdown`:

    ::

        source_suffix = {
        '.rst': 'restructuredtext',
        '.txt': 'markdown',
        '.md': 'markdown',
        }



.. note::

    更多的内容可以查看 `Markdown <https://www.sphinx-doc.org/en/master/usage/markdown.html>`_ 的官网说明。