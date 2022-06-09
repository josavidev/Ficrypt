# Ficrypt
A single desktop application for **encrypt file contents with AES mode CBC**. Available for *Windows, Linux and Mac OS*.

## Requirements installation
- **Python 3**
- **virtualenv**
- **pip**

## How to run
### **Linux**
Please use shell script `ficrypt.sh` to run application, this script creates a virtualenv for install requirements and activate it automatically for run app. Command:
```
> ./ficrypt.sh
```

#### **Ubuntu and derivatives**
In Ubuntu (*specially if you installed minimal version*) you may need install the package `libxcb-xinerama0` to run the application. You can install it via apt:
```
> sudo apt install libxcb-xinerama0
```

---
### Dependencies
- `pycryptodome`: Because `pycrypto` is officially unsupported.
- `PyQt5`: Core for create GUI.

### Tests
If you want run tests for verify module functionality, please install `pytest` and run it from project folder.

#### Version 1.0-beta