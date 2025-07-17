from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFormLayout, QDialog, QLabel, QSpinBox, QMenu, QSizePolicy
from PyQt5.QtCore import QStringListModel, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from src.services.purchase_service import PurchaseService
from datetime import datetime
import pandas as pd

class NewEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Novo Evento")
        self.setGeometry(200, 200, 400, 200)
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("font-size: 16px; padding: 10px;")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.date_input.setStyleSheet("font-size: 16px; padding: 10px;")
        self.date_input.textEdited.connect(self.format_date)
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet("font-size: 16px; padding: 10px;")

        layout.addRow("Nome do Evento:", self.name_input)
        layout.addRow("Data do Evento:", self.date_input)
        layout.addRow("Local do Evento:", self.location_input)

        save_button = QPushButton("Salvar")
        save_button.setStyleSheet("font-size: 16px; padding: 10px 20px;")
        save_button.clicked.connect(self.accept)
        layout.addRow(save_button)

        self.setLayout(layout)

    def format_date(self, text):
        """Formata a data automaticamente (ex.: 20250716 -> 2025-07-16)"""
        text = text.replace("-", "").strip()
        if len(text) >= 8 and text.isdigit():
            formatted = f"{text[:4]}-{text[4:6]}-{text[6:8]}"
            self.date_input.setText(formatted)
        elif text.isdigit():
            self.date_input.setText(text)

    def get_event_data(self):
        return {
            "name": self.name_input.text().strip(),
            "date": self.date_input.text().strip(),
            "location": self.location_input.text().strip()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.purchase_service = PurchaseService()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eventos Igreja - Gerenciamento de Compras")
        self.setGeometry(100, 100, 1000, 600)

        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # Seção de seleção de evento
        event_layout = QHBoxLayout()
        event_label = QLabel("Selecionar Evento:")
        event_label.setStyleSheet("font-size: 16px;")
        self.event_combo = QComboBox()
        self.event_combo.setStyleSheet("font-size: 16px; padding: 10px;")
        self.event_combo.setToolTip("Selecione o evento para exibir na lista ou adicionar compras")
        self.event_combo.setMinimumWidth(800)
        self.event_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.event_combo.currentIndexChanged.connect(self.refresh_table)
        event_layout.addWidget(event_label)
        event_layout.addWidget(self.event_combo)
        main_layout.addLayout(event_layout)

        # Formulário de entrada
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Linha 1: Comprador, Quantidade, Preço, Pagamento
        row1_layout = QHBoxLayout()
        self.buyer_name_input = QComboBox()
        self.buyer_name_input.setEditable(True)
        self.buyer_name_input.setStyleSheet("font-size: 16px; padding: 10px;")
        self.buyer_name_input.setMinimumWidth(200)
        self.buyer_name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.load_buyer_names()
        row1_layout.addWidget(self.buyer_name_input)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setStyleSheet("font-size: 16px; padding: 10px; width: 80px;")
        self.quantity_input.valueChanged.connect(self.update_total_price)
        self.unit_price_input = QLineEdit()
        self.unit_price_input.setPlaceholderText("R$ 0,00")
        self.unit_price_input.setStyleSheet("font-size: 16px; padding: 10px;")
        self.unit_price_input.textEdited.connect(self.format_price)
        self.unit_price_input.textChanged.connect(self.update_total_price)
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(["Cartão de Débito", "Cartão de Crédito", "Dinheiro", "Pix"])
        self.payment_method_combo.setStyleSheet("font-size: 16px; padding: 10px;")
        row1_layout.addWidget(self.quantity_input)
        row1_layout.addWidget(self.unit_price_input)
        row1_layout.addWidget(self.payment_method_combo)
        form_layout.addLayout(row1_layout)

        # Linha 2: Valor Total, Botões
        row2_layout = QHBoxLayout()
        total_label = QLabel("Valor Total:")
        total_label.setStyleSheet("font-size: 16px;")
        self.total_price_label = QLineEdit("R$ 0,00")
        self.total_price_label.setReadOnly(True)
        self.total_price_label.setStyleSheet("font-size: 16px; padding: 10px; background-color: #f0f0f0;")
        self.add_button = QPushButton("Adicionar Compra")
        self.add_button.clicked.connect(self.add_purchase)
        self.add_button.setStyleSheet("font-size: 16px; padding: 10px 20px;")
        self.new_event_button = QPushButton("Novo Evento")
        self.new_event_button.clicked.connect(self.add_new_event)
        self.new_event_button.setStyleSheet("font-size: 16px; padding: 10px 20px;")
        self.export_xls_button = QPushButton("Gerar Relatório XLS")
        self.export_xls_button.setEnabled(False)  # Desabilitado
        self.export_xls_button.setStyleSheet("font-size: 16px; padding: 10px 20px;")
        row2_layout.addWidget(total_label)
        row2_layout.addWidget(self.total_price_label)
        row2_layout.addWidget(self.add_button)
        row2_layout.addWidget(self.new_event_button)
        row2_layout.addWidget(self.export_xls_button)
        row2_layout.addStretch()
        form_layout.addLayout(row2_layout)

        main_layout.addLayout(form_layout)

        # Seção de filtro
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtrar Lista:")
        filter_label.setStyleSheet("font-size: 16px;")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Digite nome, sobrenome ou forma de pagamento")
        self.filter_input.setStyleSheet("font-size: 16px; padding: 10px;")
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Tabela de compras
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Comprador", "Data", "Evento", "Quantidade", "Preço Unitário", "Forma de Pagamento"])
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f8ff;
                background-color: #ffffff;
                gridline-color: #d0d0d0;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.table)

        # Verificar eventos e desativar campos
        self.populate_event_combo()
        self.check_and_toggle_inputs()

    def load_buyer_names(self):
        """Carrega os nomes dos compradores da base de dados ao iniciar"""
        try:
            buyer_names = self.purchase_service.get_all_buyer_names()
            self.buyer_name_input.addItem("")  # Adiciona um item em branco
            self.buyer_name_input.addItems(buyer_names)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar nomes: {e}")

    def keyPressEvent(self, event):
        """Captura setas para cima/baixo globalmente para mudar forma de pagamento"""
        if hasattr(self, 'payment_method_combo'):
            current_index = self.payment_method_combo.currentIndex()
            if event.key() == Qt.Key_Up:
                if current_index > 0:
                    self.payment_method_combo.setCurrentIndex(current_index - 1)
            elif event.key() == Qt.Key_Down:
                if current_index < self.payment_method_combo.count() - 1:
                    self.payment_method_combo.setCurrentIndex(current_index + 1)

    def format_price(self, text):
        """Formata o preço com R$ (ex.: 30 -> R$ 30,00)"""
        text = text.replace("R$", "").replace(",", "").replace(".", "").strip()
        if text and text.isdigit():
            try:
                value = float(text) / 100
                formatted = f"R$ {value:.2f}".replace(".", ",")
                self.unit_price_input.blockSignals(True)
                self.unit_price_input.setText(formatted)
                self.unit_price_input.blockSignals(False)
            except ValueError:
                pass

    def update_total_price(self):
        """Atualiza o valor total baseado na quantidade e preço unitário"""
        try:
            quantity = self.quantity_input.value()
            unit_price_text = self.unit_price_input.text().replace("R$", "").replace(",", ".").strip()
            unit_price = float(unit_price_text) if unit_price_text else 0.0
            total = quantity * unit_price
            self.total_price_label.setText(f"R$ {total:.2f}".replace(".", ","))
        except ValueError:
            self.total_price_label.setText("R$ 0,00")

    def populate_event_combo(self):
        self.event_combo.clear()
        try:
            events = self.purchase_service.get_all_events()
            for event in events:
                self.event_combo.addItem(f"{event.name} ({event.date} - {event.location}) [Evento-{event.id}]", event.id)
            if events:
                self.event_combo.setCurrentIndex(self.event_combo.count() - 1)
            self.check_and_toggle_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def check_and_toggle_inputs(self):
        """Desativa campos e botões se não houver eventos"""
        has_events = self.event_combo.count() > 0
        self.buyer_name_input.setEnabled(has_events)
        self.quantity_input.setEnabled(has_events)
        self.unit_price_input.setEnabled(has_events)
        self.payment_method_combo.setEnabled(has_events)
        self.event_combo.setEnabled(has_events)
        self.add_button.setEnabled(has_events)
        self.filter_input.setEnabled(has_events)
        self.table.setEnabled(has_events)
        self.new_event_button.setEnabled(True)
        self.export_xls_button.setEnabled(has_events)

    def add_new_event(self):
        dialog = NewEventDialog(self)
        if dialog.exec_():
            event_data = dialog.get_event_data()
            if not all([event_data["name"], event_data["date"], event_data["location"]]):
                QMessageBox.critical(self, "Erro", "Todos os campos do evento devem ser preenchidos!")
                return
            try:
                self.purchase_service.add_event(
                    name=event_data["name"],
                    date=event_data["date"],
                    location=event_data["location"]
                )
                self.populate_event_combo()
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))

    def add_purchase(self):
        buyer_name = self.buyer_name_input.currentText().strip()
        quantity = self.quantity_input.value()
        unit_price = self.unit_price_input.text().replace("R$", "").replace(",", ".").strip()
        event_id = self.event_combo.currentData()
        payment_method = self.payment_method_combo.currentText()

        if not all([buyer_name, str(quantity), unit_price, event_id, payment_method]):
            QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos!")
            return

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
            if quantity <= 0 or unit_price <= 0:
                QMessageBox.critical(self, "Erro", "Quantidade e preço unitário devem ser maiores que zero!")
                return

            existing_purchase = self.purchase_service.check_existing_purchase(buyer_name, event_id, unit_price, payment_method)
            if existing_purchase:
                new_quantity = existing_purchase.ticket_quantity + quantity
                self.purchase_service.update_purchase_quantity(existing_purchase.id, new_quantity)
            else:
                self.purchase_service.add_purchase(buyer_name, event_id, quantity, unit_price, payment_method)
                if buyer_name and buyer_name not in [self.buyer_name_input.itemText(i) for i in range(self.buyer_name_input.count())]:
                    self.buyer_name_input.addItem(buyer_name)
            self.buyer_name_input.setCurrentIndex(-1)
            self.quantity_input.setValue(1)
            self.unit_price_input.clear()
            self.refresh_table()
        except ValueError:
            QMessageBox.critical(self, "Erro", "Quantidade deve ser um número inteiro e preço unitário um número válido!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Excluir")
        save_action = menu.addAction("Salvar")
        action = menu.exec_(self.table.viewport().mapToGlobal(position))
        if action == delete_action:
            row = self.table.currentRow()
            if row >= 0:
                purchase_id = int(self.table.item(row, 0).text())
                self.purchase_service.delete_purchase(purchase_id)
                self.refresh_table()
        elif action == save_action:
            row = self.table.currentRow()
            if row >= 0:
                purchase_id = int(self.table.item(row, 0).text())
                buyer_name = self.table.item(row, 1).text()
                quantity = int(self.table.item(row, 4).text())
                unit_price = float(self.table.item(row, 5).text().replace("R$", "").replace(",", "."))
                payment_method = self.table.item(row, 6).text()
                # Reutiliza add_purchase para salvar edição
                self.purchase_service.delete_purchase(purchase_id)
                self.purchase_service.add_purchase(buyer_name, self.event_combo.currentData(), quantity, unit_price, payment_method)
                self.refresh_table()

    def filter_table(self):
        """Filtra a tabela por nome, sobrenome ou forma de pagamento"""
        filter_text = self.filter_input.text().strip().lower()
        event_id = self.event_combo.currentData()
        if not event_id:
            self.table.setRowCount(0)
            return
        try:
            purchases = self.purchase_service.get_purchases_by_event(event_id)
            filtered_purchases = [
                p for p in purchases
                if (filter_text in p.buyer_name.lower() or
                    filter_text in p.payment_method.lower())
            ]
            self.table.setRowCount(len(filtered_purchases))
            for row, purchase in enumerate(filtered_purchases):
                self.table.setItem(row, 0, QTableWidgetItem(str(purchase.id)))
                self.table.setItem(row, 1, QTableWidgetItem(purchase.buyer_name))
                self.table.setItem(row, 2, QTableWidgetItem(purchase.purchase_date))
                self.table.setItem(row, 3, QTableWidgetItem(str(purchase.event_id)))
                self.table.setItem(row, 4, QTableWidgetItem(str(purchase.ticket_quantity)))
                self.table.setItem(row, 5, QTableWidgetItem(f"R$ {purchase.unit_price:.2f}"))
                self.table.setItem(row, 6, QTableWidgetItem(purchase.payment_method))
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def refresh_table(self):
        self.filter_input.clear()
        self.filter_table()

    def export_to_xls(self):
        event_id = self.event_combo.currentData()
        if not event_id:
            QMessageBox.critical(self, "Erro", "Selecione um evento!")
            return
        try:
            purchases = self.purchase_service.get_purchases_by_event(event_id)
            event_name = self.event_combo.currentText().split(" [")[0]  # Extrai o nome do evento
            if not purchases or not event_name:
                QMessageBox.critical(self, "Erro", "Nenhum dado para exportar!")
                return

            # Calcula totais
            total_arrecadado = sum(p.ticket_quantity * p.unit_price for p in purchases)
            buyer_totals = {}
            payment_totals = {"Cartão de Débito": 0, "Cartão de Crédito": 0, "Dinheiro": 0, "Pix": 0}
            for p in purchases:
                buyer_totals[p.buyer_name] = buyer_totals.get(p.buyer_name, 0) + (p.ticket_quantity * p.unit_price)
                payment_totals[p.payment_method] += p.ticket_quantity * p.unit_price

            # Dados para o relatório
            report_data = {
                "Compras": [(p.buyer_name, p.ticket_quantity, f"R$ {p.unit_price:.2f}", p.payment_method) for p in purchases],
                "Total Arrecadado": [f"R$ {total_arrecadado:.2f}"],
                "Por Comprador": [(name, f"R$ {total:.2f}") for name, total in buyer_totals.items()],
                "Por Meio de Pagamento": [(method, f"R$ {total:.2f}") for method, total in payment_totals.items()]
            }

            # Cria DataFrame
            df = pd.DataFrame()
            df["Relatório - " + event_name] = ["Compras", "Total Arrecadado", "Por Comprador", "Por Meio de Pagamento"]
            for section, data in report_data.items():
                if section == "Compras":
                    df1 = pd.DataFrame(data, columns=["Comprador", "Quantidade", "Preço Unitário", "Método"])
                    df = pd.concat([df, df1], axis=1)
                elif section == "Total Arrecadado":
                    df1 = pd.DataFrame(data, columns=["Valor"])
                    df = pd.concat([df, df1], axis=1)
                elif section == "Por Comprador":
                    df1 = pd.DataFrame(data, columns=["Comprador", "Total"])
                    df = pd.concat([df, df1], axis=1)
                elif section == "Por Meio de Pagamento":
                    df1 = pd.DataFrame(data, columns=["Método", "Total"])
                    df = pd.concat([df, df1], axis=1)

            # Exporta para XLS
            file_path = f"relatorio_{event_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Sucesso", f"Relatório salvo em {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {e}")