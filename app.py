
from flask import Flask, redirect, render_template, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from controllers.notas import *
import pandas as pd
app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API Menegazzo')
spec.register(app)
import db
import dbIp
import json
app.secret_key = 'MarlonRolim'



@app.route('/')
def painelVendasav():
    #grupo = db.grupoProd()
    #meta = db.metas()
    #volumeMes = db.volumeMes()
    
    # Média Necessária
    '''
    mnambev = ((meta.Meta.sum()-volumeMes.Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    mncerv = ((meta[meta.Produto.isin(list(grupo['Cerv TT'].unique()))].Meta.sum()-volumeMes[volumeMes.Produto.isin(list(grupo['Cerv TT'].unique()))].Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    mnnab = ((meta[meta.Produto.isin(list(grupo['NAB'].unique()))].Meta.sum()-volumeMes[volumeMes.Produto.isin(list(grupo['NAB'].unique()))].Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    mnrgb = ((meta[meta.Produto.isin(list(grupo['RGB'].unique()))].Meta.sum()-volumeMes[volumeMes.Produto.isin(list(grupo['RGB'].unique()))].Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    mnheco = ((meta[meta.Produto.isin(list(grupo['HECO'].unique()))].Meta.sum()-volumeMes[volumeMes.Produto.isin(list(grupo['HECO'].unique()))].Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    mnpm = ((meta[meta.Produto.isin(list(grupo['Puro Malte'].unique()))].Meta.sum()-volumeMes[volumeMes.Produto.isin(list(grupo['Puro Malte'].unique()))].Volume.sum())/(db.diasUteis()[0]-db.diasUteis()[1])).round(1)
    
    # Buffer
    db_Buffer = db.pedidosDia('S', 'T')
    bambev = db_Buffer.Volume.sum().round(1)
    bcerv = db_Buffer[db_Buffer.Produto.isin(list(grupo['Cerv TT'].unique()))].Volume.sum().round(1)
    bnab = db_Buffer[db_Buffer.Produto.isin(list(grupo['NAB'].unique()))].Volume.sum().round(1)
    brgb = db_Buffer[db_Buffer.Produto.isin(list(grupo['RGB'].unique()))].Volume.sum().round(1)
    bheco = db_Buffer[db_Buffer.Produto.isin(list(grupo['HECO'].unique()))].Volume.sum().round(1)
    bpm = db_Buffer[db_Buffer.Produto.isin(list(grupo['Puro Malte'].unique()))].Volume.sum().round(1)
    '''
    mnambev = "1000"
    mncerv = "900"
    mnnab = "300"
    mnrgb = "400"
    mnheco = "200"
    mnpm = "150"
    bambev = "5"
    bcerv = "10"
    bnab = "15"
    brgb = "23"
    bheco = "2"
    bpm = "3"
    return render_template('index.html',mnambev=mnambev,
                                        mncerv=mncerv,
                                        mnnab=mnnab,
                                        mnrgb=mnrgb,
                                        mnheco=mnheco,
                                        mnpm=mnpm,
                                        bambev=bambev,
                                        bcerv=bcerv,
                                        bnab=bnab,
                                        brgb=brgb,
                                        bheco=bheco,
                                        bpm=bpm)

@app.route('/api/painelvendasav/volumedia')
def painelvendasavApi():
    """Volumes do dia"""
    grupo = db.grupoProd()
    db_sFalta = db.pedidosDia('N', 'N')
    db_cFalta = db.pedidosDia('N', 'T')
    db_falta = db.pedidosDia('N', 'S')
    
    volumedia = {
        "vTT" : db_sFalta.Volume.sum().round(1),
        "vTTcf" : db_cFalta.Volume.sum().round(1),
        "vTTf" : db_falta.Volume.sum().round(1),
        "vC" : db_sFalta[db_sFalta.Produto.isin(list(grupo['Cerv TT'].unique()))].Volume.sum().round(1),
        "vCcf" : db_cFalta[db_cFalta.Produto.isin(list(grupo['Cerv TT'].unique()))].Volume.sum().round(1),
        "vCf" : db_falta[db_falta.Produto.isin(list(grupo['Cerv TT'].unique()))].Volume.sum().round(1),
        "vN" : db_sFalta[db_sFalta.Produto.isin(list(grupo['NAB'].unique()))].Volume.sum().round(1),
        "vNcf" : db_cFalta[db_cFalta.Produto.isin(list(grupo['NAB'].unique()))].Volume.sum().round(1),
        "vNf" : db_falta[db_falta.Produto.isin(list(grupo['NAB'].unique()))].Volume.sum().round(1),
        "vR" : db_sFalta[db_sFalta.Produto.isin(list(grupo['RGB'].unique()))].Volume.sum().round(1),
        "vRcf" : db_cFalta[db_cFalta.Produto.isin(list(grupo['RGB'].unique()))].Volume.sum().round(1),
        "vRf" : db_falta[db_falta.Produto.isin(list(grupo['RGB'].unique()))].Volume.sum().round(1),
        "vH" : db_sFalta[db_sFalta.Produto.isin(list(grupo['HECO'].unique()))].Volume.sum().round(1),
        "vHcf" : db_cFalta[db_cFalta.Produto.isin(list(grupo['HECO'].unique()))].Volume.sum().round(1),
        "vHf" : db_falta[db_falta.Produto.isin(list(grupo['HECO'].unique()))].Volume.sum().round(1),
        "vP" : db_sFalta[db_sFalta.Produto.isin(list(grupo['Puro Malte'].unique()))].Volume.sum().round(1),
        "vPcf" : db_cFalta[db_cFalta.Produto.isin(list(grupo['Puro Malte'].unique()))].Volume.sum().round(1),
        "vPf" : db_falta[db_falta.Produto.isin(list(grupo['Puro Malte'].unique()))].Volume.sum().round(1),
    }
    
    
    return volumedia



if __name__ == '__main__':
    app.run(debug=False)