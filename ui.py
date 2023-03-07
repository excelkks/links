import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QMenu, QAction, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAbstractItemView, QLineEdit, QFileDialog, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from link import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("链接记录")
        # self.setGeometry(100, 100, 600, 400)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(1200)

        # 创建表格视图并设置属性
        self.table_view = QTableView()
        self.table_view.setMinimumWidth(1000)
        # self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)

        # 创建右键菜单
        self.context_menu = QMenu(self)

        self.add_row_action = QAction("插入", self)
        self.add_row_action.triggered.connect(self.add_row)

        self.delete_row_action = QAction("删除", self)
        self.delete_row_action.triggered.connect(self.delete_row)

        self.context_menu.addAction(self.add_row_action)
        self.context_menu.addAction(self.delete_row_action)

        # 创建模型并设置表头
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['链接', '源文件'])
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSortingEnabled(True)

        # # 添加数据到模型
        # for row in range(5):
        #     items = [
        #         QStandardItem(f"Name {row}"),
        #         QStandardItem(f"{20 + row}"),
        #     ]
        #     self.model.appendRow(items)

        # read data from database
        self.readFromDB()

        # 创建标签和按钮
        self.select_btn = QPushButton("选择", self)
        self.select_btn.clicked.connect(self.selectFromDialog)

        self.read_btn = QPushButton("读取", self)
        self.read_btn.clicked.connect(self.readFromDB)

        self.save_btn = QPushButton("保存", self)
        self.save_btn.clicked.connect(self.saveToDB)

        self.cancel_btn = QPushButton("退出", self)
        self.cancel_btn.clicked.connect(self.cancelDialog)

        # 创建搜索框和搜索按钮
        self.search_box = QLineEdit(self)
        self.search_box.returnPressed.connect(self.search)
        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search)

        # 创建布局并将部件添加到其中
        layout1 = QVBoxLayout()
        layout1.addWidget(self.table_view)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.select_btn)
        layout2.addWidget(self.read_btn)
        layout2.addWidget(self.save_btn)
        layout2.addWidget(self.cancel_btn)
        layout1.addLayout(layout2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.search_box)
        layout3.addWidget(self.search_button)
        layout1.addLayout(layout3)

        # 创建一个占位符小部件以创建空间
        widget = QWidget()
        widget.setLayout(layout1)

        # 将小部件设置为主窗口的中心窗口
        self.setCentralWidget(widget)

    def show_context_menu(self, pos):
        self.context_menu.exec_(self.table_view.viewport().mapToGlobal(pos))

    def add_row(self):
        items = [
            QStandardItem("New Name"),
            QStandardItem("New Age"),
        ]
        self.model.appendRow(items)

    def delete_row(self):
        rows = sorted(set(index.row() for index in self.table_view.selectedIndexes()))
        for row in reversed(rows):
            self.model.removeRow(row)

    def clear_table(self):
        model = self.model
        for row in reversed(range(model.rowCount())):
            self.model.removeRow(row)

    def search(self):
        text = self.search_box.text().lower()
        if not text:
            # 如果搜索框为空，则显示所有行
            for row in range(self.model.rowCount()):
                self.table_view.setRowHidden(row, False)
        else:
            # 否则，隐藏不包含搜索文本的所有行
            for row in range(self.model.rowCount()):
                match = False
                for column in range(self.model.columnCount()):
                    cell = self.model.index(row, column).data()
                    if text in cell.lower():
                        match = True
                        break
                self.table_view.setRowHidden(row, not match)

    def updateFromTable(self):
        clear_links()
        for row in range(self.model.rowCount()):
            linkIdx = self.model.index(row, 0)
            srcIdx = self.model.index(row, 1)
            link = self.model.data(linkIdx)
            src = self.model.data(srcIdx)
            revise_link(link, src)
    
    def selectFromDialog(self):
        if not self.table_view.selectedIndexes():
            return
        index = self.table_view.selectedIndexes()[0]
        file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*)")
        self.model.setData(index, file_path)
        self.updateFromTable()

    def readFromDB(self):
        read_links()
        self.clear_table()
        links = all_links.keys()

        for link in links:
            items = [
                QStandardItem(link),
                QStandardItem(all_links[link])
            ]
            self.model.appendRow(items)
        self.updateFromTable()

    def saveToDB(self):
        self.updateFromTable()
        save_change()
        self.readFromDB()

    def cancelDialog(self):
        self.saveToDB()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
