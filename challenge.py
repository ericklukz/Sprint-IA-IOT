from bardapi import BardCookies
from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb
import os
from gtts import gTTS

app = Flask(__name__)
CORS(app)

query = ""

lista_dados = []

conn = oracledb.connect(user="rm94554", password="010204", dsn="oracle.fiap.com.br:1521/orcl")

inst_consulta = conn.cursor()
inst_cadastro = conn.cursor()

cookie_dict = {
    "__Secure-1PSID": "dAgxJZMwwbos7n9VQJkLApzRqGNgBSHQIDux6XIMkMHfnZADJ6H5b-9H_LBRBFa0y935sQ.",
    "__Secure-1PSIDTS": "sidts-CjIBNiGH7lzZB857utbk9gnMp-DbvcXwT84rzeySm-Puuz-JsOmKt-yHGjD9YH1vLMqW8hAA",
}

bard = BardCookies(cookie_dict=cookie_dict)

cliente = 1


def receber_tamanho_audio(caminho_audio):
    if os.path.isfile(caminho_audio):
        # Obtém o tamanho do arquivo em bytes
        file_size_bytes = os.path.getsize(caminho_audio)
        # Converte o tamanho do arquivo para kilobytes
        file_size_kb = file_size_bytes / 1024
        return file_size_kb
    else:
        return None


def contar_registros():
    inst_consulta.execute('SELECT * FROM T_AUDIO_CLIENTE')
    data = inst_consulta.fetchall()
    for dt in data:
        lista_dados.append(dt)
    contagem = len(lista_dados) + 1
    return contagem


@app.route('/receber-texto', methods=['POST'])
def receber_texto():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            texto = data['pergunta']
            print(texto)
            query = texto + " Resuma em poucas palavras"
            resposta = bard.get_answer(query)['content']
            audio = gTTS(resposta, lang='pt')
            caminho_audio = 'resposta_bard.wav'
            audio.save(caminho_audio)
            id = contar_registros()
            tamanho = int(receber_tamanho_audio(caminho_audio))
            print(resposta)
            inst_cadastro.callproc('inserir_audio_cliente',
                                   keywordParameters={"p_id_cliente": cliente, "p_id_audio": id,
                                                      "p_data_audio": tamanho})
            return jsonify({'resposta': resposta})
        else:
            return jsonify({'error': "Chave 'texto' não encontrada nos dados JSON"}), 400
    else:
        return jsonify({'error': "A solicitação não contém dados JSON válidos"}), 400


@app.route('/listar_todos', methods=['GET'])
def recuperar_dados():
    inst_consulta.execute('SELECT * FROM t_produto')
    data = inst_consulta.fetchall()
    produtos = []
    for dt in data:
        produto = {
            'Nome': dt[5],
            'Descricao': dt[6],
            'Valor': dt[9],
            'Frete': dt[10]
        }
        produtos.append(produto)

    ordem = ['Nome', 'Descricao', 'Valor', 'Frete']

    produtos_ordenados = []
    for produto in produtos:
        produto_ordenado = {chave: produto[chave] for chave in ordem}
        produtos_ordenados.append(produto_ordenado)
    print(produtos)
    return jsonify(produtos)


if __name__ == '__main__':
    app.run()
