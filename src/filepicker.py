#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getenv

from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout,
                             QLabel, QLineEdit, QErrorMessage,
                             QPushButton, QVBoxLayout, QWidget)


class SingleFilePicker(QWidget):
    def __init__(self, caption, promise):
        super().__init__()
        self.valmsg = 'File or directory not selected'
        self.fext = 'All files (*.*)'
        self.__mode_dir = False
        self.__caption = caption
        self.__promise = promise
        self.__selected_value = ''
        self.__on_create()

    def __on_create(self):
        # pick file components
        display_lb = QLabel(text=self.__caption)
        self.__pick_btn = QPushButton('Select file')
        self.__pick_btn.clicked.connect(self.pick_btn_clicked)
        # widgets in same row
        caption_wg = QWidget()
        caption_wg.setLayout(QHBoxLayout())
        caption_wg.layout().addWidget(display_lb)
        caption_wg.layout().addWidget(self.__pick_btn)
        # edit text for view path selected
        self.__path_txt = QLineEdit()
        self.__path_txt.textChanged.connect(self.handle_path_txt_text_changed)
        # add to layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(caption_wg)
        self.layout().addWidget(self.__path_txt)

    def validate(self):
        if len(self.__selected_value) == 0:
            QErrorMessage(self).showMessage(self.valmsg)
            return False
        return True

    def clean(self):
        self.__selected_value = ''
        self.__path_txt.setText('')
        self.__promise('')

    def toggle_mode_dir(self, enabled):
        self.__mode_dir = enabled
        self.fext = 'All files (*.*)'
        if self.__mode_dir:
            self.__pick_btn.setText('Select directory')
        else:
            self.__pick_btn.setText('Select file')

    def pick_btn_clicked(self):
        target = ''
        if self.__mode_dir:
            target = QFileDialog.getExistingDirectory(None, 'Select directory',
                                                      getenv('HOME'),
                                                      QFileDialog.Option.ShowDirsOnly
                                                      | QFileDialog.Option.DontResolveSymlinks
                                                      | QFileDialog.Option.DontUseNativeDialog)
        else:
            filename = QFileDialog.getOpenFileName(None, 'Select file',
                                                   getenv('HOME'), self.fext,
                                                   options=QFileDialog.Option.DontResolveSymlinks
                                                   | QFileDialog.Option.DontUseNativeDialog)
            target = filename[0]

        self.__selected_value = target
        self.__path_txt.setText(target)
        self.__promise(target)

    def handle_path_txt_text_changed(self):
        self.__path_txt.setText(self.__selected_value)

    @property
    def fext(self):
        return self.__fext

    @fext.setter
    def fext(self, fext):
        self.__fext = fext

    @property
    def valmsg(self):
        return self.__valmsg

    @valmsg.setter
    def valmsg(self, valmsg):
        self.__valmsg = valmsg
