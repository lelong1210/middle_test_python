from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

app = QApplication(sys.argv)

# Tạo một đối tượng QWebEngineView
web_view = QWebEngineView()

# Hiển thị nội dung HTML trong QWebEngineView
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
web_view.setHtml(html_content, QUrl('http://localhost/'))

# Hiển thị QWebEngineView
web_view.show()

# Chạy ứng dụng
sys.exit(app.exec_())