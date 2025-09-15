import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
import markdown

from PyQt5.QtWebEngineWidgets import QWebEngineView


def show_output(output:str):
    app=QApplication(sys.argv)

    html_content=markdown.markdown(output,extensions=['fenced_code','tables','toc'])

    html_template = f"""<!DOCTYPE html><html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: Arial, sans-serif;
            line-height: 1.8;
            padding: 20px;
        }}

        p {{
            margin: 1em 0;
        }}

        h1 {{
            font-size: 2em;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            color: #facc15;
        }}

        h2 {{
            font-size: 1.6em;
            margin-top: 1em;
            margin-bottom: 0.5em;
            color: #fbbf24;
        }}

        h3 {{
            font-size: 1.3em;
            margin-top: 0.8em;
            margin-bottom: 0.4em;
            color: #fcd34d;
        }}

        pre {{
            background: #1e293b;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
        }}

        code {{
            background: #1e293b;
            padding: 2px 5px;
            border-radius: 4px;
            color: #facc15;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}

        table, th, td {{
            border: 1px solid #334155;
            padding: 8px;
        }}

        th {{
            background-color: #1e293b;
            color: #facc15;
        }}
    </style>
    </head>
    <body class='p-6'>
    <div class="prose prose-invert max-w-none">
    {html_content}
    </div>
    </body>
    </html>"""


    window=QWidget()
    window.setWindowTitle("ClipBoardGPT")
    window.resize(800,600)

    layout=QVBoxLayout()

    view=QWebEngineView()
    view.setHtml(html_template)

    layout.addWidget(view)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())