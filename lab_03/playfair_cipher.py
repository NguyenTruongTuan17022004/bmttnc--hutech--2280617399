import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt # Import Qt for Qt.AlignCenter (đã được dùng trong UI nếu bạn dùng layout)
from ui_playfair import Ui_MainWindow # Đảm bảo file này đã được sinh ra từ playfair_ui.ui
import requests

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút với các hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

        # Căn giữa cho tiêu đề và thông tin sinh viên nếu bạn đang dùng setupUI từ file .ui
        # (Lưu ý: Nếu bạn đã chỉnh sửa file .ui để dùng layout và alignment,
        # thì những dòng này không cần thiết ở đây nữa, nhưng tôi giữ lại để rõ ràng)
        # self.ui.label_title.setAlignment(Qt.AlignCenter)
        # self.ui.label_student_info.setAlignment(Qt.AlignCenter)


    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt" # Endpoint API Playfair Encrypt
        plain_text = self.ui.txt_plaintext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not plain_text or not key:
            QMessageBox.warning(self, "Input Error", "Please enter both Plain Text and Key.")
            return

        payload = {
            "plain_text": plain_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            
            # Cố gắng parse JSON dù thành công hay thất bại (trừ khi không có phản hồi)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_ciphertext.setPlainText(data.get("encrypted_message", "Error: No encrypted message received"))
                QMessageBox.information(self, "Success", "Encryption Successful!")
            else:
                try:
                    data = response.json()
                    error_message = data.get("error", f"Unknown API error (Status: {response.status_code})")
                except ValueError: # Nếu phản hồi không phải JSON
                    error_message = f"API returned non-JSON response or invalid JSON. Status: {response.status_code}. Raw: {response.text}"
                
                QMessageBox.critical(self, "Encryption Failed", f"Error: {error_message}")
                print(f"API Error: Status Code {response.status_code}, Response: {response.text}") 

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Network Error", 
                                 f"Could not connect to the API server at {url}. "
                                 "Please ensure the Flask API is running.")
            print(f"Connection Error: Could not connect to {url}")
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Network Error", "Request to API timed out.")
            print("Request Timeout")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "API Error", f"An unexpected error occurred during API call: {e}")
            print(f"Request Exception: {e}")
        except Exception as e: # Catch all other potential errors
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")
            print(f"Unexpected Error: {e}")


    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt" # Endpoint API Playfair Decrypt
        cipher_text = self.ui.txt_ciphertext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not cipher_text or not key:
            QMessageBox.warning(self, "Input Error", "Please enter both Cipher Text and Key.")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            
            # Cố gắng parse JSON dù thành công hay thất bại (trừ khi không có phản hồi)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plaintext.setPlainText(data.get("decrypted_message", "Error: No decrypted message received"))
                QMessageBox.information(self, "Success", "Decryption Successful!")
            else:
                try:
                    data = response.json()
                    error_message = data.get("error", f"Unknown API error (Status: {response.status_code})")
                except ValueError: # Nếu phản hồi không phải JSON
                    error_message = f"API returned non-JSON response or invalid JSON. Status: {response.status_code}. Raw: {response.text}"
                
                QMessageBox.critical(self, "Decryption Failed", f"Error: {error_message}")
                print(f"API Error: Status Code {response.status_code}, Response: {response.text}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Network Error", 
                                 f"Could not connect to the API server at {url}. "
                                 "Please ensure the Flask API is running.")
            print(f"Connection Error: Could not connect to {url}")
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Network Error", "Request to API timed out.")
            print("Request Timeout")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "API Error", f"An unexpected error occurred during API call: {e}")
            print(f"Request Exception: {e}")
        except Exception as e: # Catch all other potential errors
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())