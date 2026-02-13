# 💠 Gerador & Leitor de Pix Pro (Python)

Uma aplicação desktop moderna desenvolvida em Python para gerar **QR Codes do Pix** (Padrão EMVCo) e decodificar strings "Copia e Cola". O projeto utiliza `tkinter` para a interface gráfica e realiza o cálculo nativo do CRC16.

![Preview do Aplicativo](preview.png)
> *Interface moderna com as cores oficiais do Pix.*

## 🚀 Funcionalidades

* **Gerar QR Code:** Cria códigos estáticos válidos para pagamentos instantâneos.
* **Importar (Engenharia Reversa):** Cole um código "Pix Copia e Cola" (começado em `000201...`) e o app extrai automaticamente a Chave, Nome, Cidade e Valor.
* **Salvar em PNG:** Exporta o QR Code em alta resolução.
* **Validação CRC16:** Cálculo automático do dígito verificador exigido pelo Banco Central.
* **Interface Moderna:** Design limpo (Flat Design) utilizando `ttk` e as cores oficiais da identidade visual do Pix.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter** (Interface Gráfica)
* **Library `qrcode`** (Geração da matriz)
* **Pillow (PIL)** (Manipulação de imagem)

## 📦 Instalação e Uso

1.  **Clone o repositório ou baixe os arquivos:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Instale as dependências:**
    ```bash
    pip install qrcode[pil] pillow
    ```

3.  **Execute a aplicação:**
    ```bash
    python pix_app.py
    ```

## ⚙️ Como criar um Executável (.exe)

Se desejar transformar este script em um programa nativo para Windows (sem precisar instalar Python na máquina de quem vai usar):

1.  Instale o PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Gere o executável:
    ```bash
    pyinstaller --noconsole --onefile --icon=icone.ico --name="GeradorPixPro" pix_app.py
    ```
    *(Nota: O arquivo `.exe` será criado na pasta `/dist`)*

## 📄 Estrutura do Payload (EMVCo)

O aplicativo segue a norma **BR Code** do Banco Central, montando os IDs:
* `26`: Merchant Account Information (Onde fica a Chave Pix)
* `52`: Merchant Category Code (0000 - Geral)
* `53`: Transaction Currency (986 - BRL)
* `54`: Transaction Amount (Valor)
* `58`: Country Code (BR)
* `59`: Merchant Name
* `60`: Merchant City
* `62`: Additional Data Field (TxID)
* `63`: CRC16 (Calculado via polinômio 0x1021)

## 📝 Licença

Este projeto é de código aberto e livre para uso educacional e comercial.
