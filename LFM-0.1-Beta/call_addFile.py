# coding=utf-8
import sys
import os
import json
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from addFile import Ui_Form
from qt_material import apply_stylesheet

label_data_path = 'labelData.json'
file_label_data_path = 'fileLabelData.json'


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        # ui初始化
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 拖动初始化
        self.path = ""
        self.setAcceptDrops(True)
        # 反馈文字框初始化
        self.text = ''
        # 事件绑定
        self.label_pushButton.clicked.connect(self.add_child_label)
        self.delete_pushButton.clicked.connect(self.delete)
        self.help_pushButton.clicked.connect(self.help)
        self.label_treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_treeWidget.customContextMenuRequested.connect(self.select)
        self.selected_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.selected_listWidget.customContextMenuRequested.connect(self.unselect)
        self.add_pushButton.clicked.connect(self.add_to_warehouse)
        # labelTree 初始化
        self.root = QTreeWidgetItem(self.label_treeWidget)
        self.root.setText(0, 'label')
        # 标签树初始化
        if not os.path.isfile(label_data_path):
            info_dict = {'label': {'name': 'label', 'child': {}}}
            info_json = json.dumps(info_dict, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
            f = open(label_data_path, 'w', encoding='utf-8')
            f.write(info_json)
            f.close()
        f2 = open(label_data_path, 'r', encoding='utf-8')
        self.label = json.load(f2)
        f2.close()
        self.updateTree()
        # 已存文件标签信息初始化
        if not os.path.isfile(file_label_data_path):
            info_saved = {"_fileName_": "file_label_data"}
            info_json = json.dumps(info_saved, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
            f = open(file_label_data_path, 'w', encoding='utf-8')
            f.write(info_json)
            f.close()
        f2 = open(file_label_data_path, 'r', encoding='utf-8')
        self.file_label = json.load(f2)
        f2.close()
        # 已选标签初始化
        self.selectedSet = set()
        # 操作优化
        self.label_treeWidget.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(
            self.tree_expand_or_not)  # 双击展开or收起

    def add_to_warehouse(self):
        target_path = r".\warehouse"
        filename = self.path.split('/')[-1]
        if self.path == '':
            self.error("没有拖入文件,请先拖入文件")
            return
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        shutil.copy(self.path, target_path)
        for label in self.selectedSet:
            if label in self.file_label.keys():
                if filename not in self.file_label[label]:
                    self.file_label[label].append(filename)
            else:
                self.file_label[label] = [filename]
        self.info("添加成功")

    def select(self):
        """从label树中选择label至已选区域"""
        if self.label_treeWidget.currentItem() is not None:
            self.selectedSet.add(self.label_treeWidget.currentItem().text(0))
            self.selected_listWidget.clear()
            for label in self.selectedSet:
                item = QListWidgetItem(self.selected_listWidget)
                item.setText(label)

    def unselect(self):
        """从已选区域取消选择"""
        if self.selected_listWidget.currentItem() is not None:
            self.selectedSet.discard(self.selected_listWidget.currentItem().text())
            self.selected_listWidget.clear()
            for label in self.selectedSet:
                item = QListWidgetItem(self.selected_listWidget)
                item.setText(label)

    def help(self):
        self.info("----------------------------------")
        self.info("欢迎使用这玩意儿。")
        self.info("在左侧对标签使用右键可以选择。")
        self.info("右键已经选择的标签取消选择。")
        self.info("拖入文件后点击“添加至仓库”,会将文件放入与软件在同目录的文件夹“warehouse”中")
        self.info("----------------------------------")

    def tree_expand_or_not(self, item, column):
        if item.isExpanded():
            self.label_treeWidget.currentItem().setExpanded(True)
        else:
            self.label_treeWidget.currentItem().setExpanded(False)

    def updateTree(self):
        """读取self.label来更新tree图"""
        while self.root.childCount() > 0:
            for i in range(self.root.columnCount()):
                self.root.removeChild(self.root.child(i))
        self.addItemFromDic(self.root, self.label['label'])

    def addItemFromDic(self, item, dic):
        """从字典和item中还原item至tree图中"""
        for childName in dic['child'].keys():
            child = QTreeWidgetItem(item)
            child.setText(0, childName)
            self.addItemFromDic(child, dic['child'][childName])

    def info(self, info):
        """在feedback框中添加语句"""
        self.text += info + '\n'
        self.feedback.setText(self.text)

    def error(self, info):
        """在feedback框中添加error语句"""
        self.text += "error:" + info + '\n'
        self.feedback.setText(self.text)

    def add_child_label(self):
        item = self.label_treeWidget.currentItem()
        name = self.label_lineEdit.text()
        if item is not None and name != '':
            childItem = QTreeWidgetItem(item)
            childItem.setText(0, name)
            if not self.addLabel(childItem):
                item.removeChild(childItem)

    def delete(self):
        item = self.label_treeWidget.currentItem()
        if item.parent() is None:
            self.error("根目录不可删除")
        else:
            loc = self.getLocation_treeWidget(item)
            itemDict = self.getDictFromLocation(item)
            name = item.text(0)
            itemDict['child'].pop(name)
            # parent = item.parent()
            # parent.removeChild(item)
            self.updateTree()
            self.info("已删除标签:" + loc + '\\' + name)
        self.updateTree()

    def getLocation_treeWidget(self, item):
        """获取在treeWidget的目录"""
        if item.parent():
            temp = item.parent().text(0)
            parent = self.getLocation_treeWidget(item.parent())  # 递归获取上层节点，直到顶层
            if parent:
                res = os.path.join(parent, temp)
                return res
            else:
                return temp  # 最终返回节点索引
        else:
            return 0

    def getDictFromLocation(self, item):
        """找到对应location的字典"""
        loc_str = self.getLocation_treeWidget(item)
        loc_list = loc_str.split('\\')
        # print(loc_list)
        label_dict = self.label
        for i in range(len(loc_list)):
            name = loc_list[i]
            # print(name+'++')
            label_dict = label_dict[name]
            if i != len(loc_list) - 1:
                label_dict = label_dict['child']
        return label_dict

    def addLabel(self, item):
        """添加label至self.label字典中"""
        label_dict = self.getDictFromLocation(item)
        if item.text(0) in label_dict['child'].keys():
            self.error("同目录不可重名")
            return False
        label_dict['child'][item.text(0)] = {'name': item.text(0), 'child': {}}
        self.info("添加成功:" + self.getLocation_treeWidget(item) + '\\' + item.text(0))
        return True

    def dragEnterEvent(self, event):
        file = event.mimeData().urls()[0].toLocalFile()
        if file != self.path:
            self.path = file
            # 鼠标放开函数事件
            event.accept()
            self.info("已选择文件" + self.path)
            self.info("点击“添加至仓库”，将存入带有标签信息的图片")

    def saveLabelTree(self):
        info_json = json.dumps(self.label, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        f = open(label_data_path, 'w', encoding='utf-8')
        f.write(info_json)
        f.close()
        info_json = json.dumps(self.file_label, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        f = open(file_label_data_path, 'w', encoding='utf-8')
        f.write(info_json)
        f.close()

    def closeEvent(self, event):
        """关闭窗口时弹出确认消息,是否保存"""
        reply = QMessageBox.question(self, 'Warning', '此次操作是否保存？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.saveLabelTree()
            event.accept()
        else:
            event.accept()


if __name__ == "__main__":
    # PyQt5程序都需要app对象,用sys.argv确保能够双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 设置qss
    apply_stylesheet(app, theme="dark_cyan.xml")
    # 将窗口部件显示到屏幕上
    myWin.show()
    # 调用app的exec_()方法后，会进入主循环,程序运行
    # 保证程序能正常退出
    sys.exit(app.exec_())
