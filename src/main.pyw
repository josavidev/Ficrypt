#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QApplication,
                             QTabWidget, QErrorMessage, QMessageBox)
from PyQt5.QtGui import QIcon
from filepicker import SingleFilePicker
from cipherman import cipher, fileman
from pathlib import Path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__state = {}
        self.__on_create()

    def no_resize(self):
        self.setFixedSize(self.size())

    def __on_create(self):
        self.setWindowIcon(QIcon('res/img/icon.png'))
        self.setWindowTitle('Ficrypt')
        self.setLayout(QVBoxLayout())
        self.__load_widgets()
        self.show()

    def __load_widgets(self):
        # encrypt tab
        self.__file_enc_sfp = SingleFilePicker('Select file to encrypt:',
                                               self.filename_encrypt)
        self.__file_enc_sfp.valmsg = 'File to encrypt not selected!'
        self.__target_enc_sfp = SingleFilePicker('Select directory where place file encrypted:',
                                                 self.target_encrypt)
        self.__target_enc_sfp.valmsg = 'Directory target for encrypt not selected!'
        self.__target_enc_sfp.toggle_mode_dir(True)
        encrypt_btn = QPushButton('Encrypt file')
        encrypt_btn.setProperty('class', 'btn-primary')
        encrypt_btn.clicked.connect(self.__encrypt_btn_clicked)
        encrypt_wg = QWidget()
        encrypt_wg.setLayout(QVBoxLayout())
        encrypt_wg.layout().addWidget(self.__file_enc_sfp)
        encrypt_wg.layout().addWidget(self.__target_enc_sfp)
        encrypt_wg.layout().addWidget(encrypt_btn)
        # decrypt tab
        self.__file_dec_sfp = SingleFilePicker('Select file to decrypt:', self.filename_decrypt)
        self.__file_dec_sfp.fext = 'Encrypted file (*.enc)'
        self.__file_dec_sfp.valmsg = 'File to decrypt not selected!'
        self.__key_file_sfp = SingleFilePicker('Select key:', self.key_file)
        self.__key_file_sfp.fext = 'Key file (*.key)'
        self.__key_file_sfp.valmsg = 'Key file for decrypt not selected!'
        self.__target_dec_sfp = SingleFilePicker('Select directory where place content decrypted:',
                                                 self.target_decrypt)
        self.__target_dec_sfp.valmsg = 'Directory target for decrypt not selected!'
        self.__target_dec_sfp.toggle_mode_dir(True)
        decrypt_btn = QPushButton('Decrypt file')
        decrypt_btn.setProperty('class', 'btn-primary')
        decrypt_btn.clicked.connect(self.__decrypt_btn_clicked)
        decrypt_wg = QWidget()
        decrypt_wg.setLayout(QVBoxLayout())
        decrypt_wg.layout().addWidget(self.__file_dec_sfp)
        decrypt_wg.layout().addWidget(self.__key_file_sfp)
        decrypt_wg.layout().addWidget(self.__target_dec_sfp)
        decrypt_wg.layout().addWidget(decrypt_btn)
        # tab bar
        tab_wg = QTabWidget()
        tab_wg.addTab(encrypt_wg, 'Encrypt')
        tab_wg.addTab(decrypt_wg, 'Decrypt')
        self.layout().addWidget(tab_wg)

    # handlers
    def __encrypt_btn_clicked(self):
        if (not self.__file_enc_sfp.validate()
                or not self.__target_enc_sfp.validate()):
            return
        # get values from dict
        file_enc = self.__get_value_state('file_enc')
        target_enc = self.__get_value_state('target_enc')
        try:
            content = fileman.read_file(file_enc)
            encrypted, key = cipher.encrypt(content)
        except (UnicodeEncodeError, UnicodeDecodeError):
            QErrorMessage(self).showMessage('File coding not supported, please check your file')
            return
        # get path to save content
        filepath = Path(file_enc)
        encrypted_path = target_enc + f'/{filepath.name}.enc'
        key_path = target_enc + f'/{filepath.name}.key'
        fileman.write_bytes_file(encrypted, encrypted_path)
        fileman.write_bytes_file(key, key_path)
        QMessageBox.information(None, 'Information',
                                'File encrypted successfully.')
        self.__file_enc_sfp.clean()
        self.__target_enc_sfp.clean()

    def __decrypt_btn_clicked(self):
        if (not self.__file_dec_sfp.validate()
            or not self.__key_file_sfp.validate()
                or not self.__target_dec_sfp.validate()):
            return
        # get values from dict
        file_dec = self.__get_value_state('file_dec')
        key_file = self.__get_value_state('key_file')
        target_dec = self.__get_value_state('target_dec')
        try:
            encrypted_content = fileman.read_bytes_file(file_dec)
            key_bytes = fileman.read_bytes_file(key_file)
            content = cipher.decrypt(encrypted_content, key_bytes)
        except (UnicodeDecodeError, UnicodeEncodeError):
            QErrorMessage(self).showMessage('File coding not supported, please check your file')
            return
        except ValueError:
            QErrorMessage(self).showMessage('File integrity is corrupted, please check your file')
            return
        filepath = Path(file_dec)
        filename = target_dec + f'/{filepath.stem}'
        fileman.write_file(content, filename)
        QMessageBox.information(None, 'Information',
                                'File decrypted successfully.')
        self.__file_dec_sfp.clean()
        self.__key_file_sfp.clean()
        self.__target_dec_sfp.clean()

    # state getters and setters
    def __get_value_state(self, key):
        try:
            return self.__state[key]
        except KeyError:
            return ''

    def filename_encrypt(self, filename):
        self.__state['file_enc'] = filename

    def target_encrypt(self, path):
        self.__state['target_enc'] = path

    def filename_decrypt(self, filename):
        self.__state['file_dec'] = filename

    def key_file(self, filename):
        self.__state['key_file'] = filename

    def target_decrypt(self, path):
        self.__state['target_dec'] = path


if __name__ == '__main__':
    app = QApplication([])
    with open('src/main.qss', 'r') as qss:
        sheet = ''.join(qss.readlines())
        app.setStyleSheet(sheet)
    mw = MainWindow()
    mw.no_resize()
    app.exec_()
