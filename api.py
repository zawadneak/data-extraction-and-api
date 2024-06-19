from flask import Flask
import pandas

app = Flask(__name__)

tipos = pandas.read_csv("tipos.csv")

@app.route("/nome-tipo/<int:tipo_id>")
def get_nome_tipo(tipo_id):
    if tipo_id is None:
        return "No tipo_id provided.",400
    
    tipo_nome = tipos.loc[int(tipo_id),"nome"]
    
    if tipo_nome is None:
        return "Tipo nome not found",404
    
    return {
        "tipo": tipo_nome
    }