import streamlit as st

# Função para gerar o arquivo TXT
def gerar_arquivo_txt(dados_cabecalho, detalhes, rodape):
    linhas = []
    
    # Adiciona o cabeçalho (Registro Tipo 1)
    linhas.append(
        f"1{dados_cabecalho['versao']:03}{dados_cabecalho['ccm']:08}"
        f"{dados_cabecalho['data_inicio']}{dados_cabecalho['data_fim']}\r\n"
    )
    
    # Adiciona os detalhes (Registro Tipo 4)
    for detalhe in detalhes:
        linha = (
            f"4{detalhe['tipo_doc']:02}{detalhe['serie_doc']:<5}{detalhe['numero_doc']:>012}"
            f"{detalhe['data_servico']}{detalhe['situacao']}{detalhe['tributacao']}"
            f"{detalhe['valor_servico']:015}{detalhe['valor_deducoes']:015}"
            f"{detalhe['codigo_servico']:05}{detalhe['codigo_subitem']:04}"
            f"{detalhe['aliquota']:04}{detalhe['iss_retido']}{detalhe['indicador_cpf_cnpj']}"
            f"{detalhe['cpf_cnpj_prestador']:<14}\r\n"
        )
        linhas.append(linha)
    
    # Adiciona o rodapé (Registro Tipo 9)
    linhas.append(
        f"9{rodape['numero_linhas']:07}{rodape['valor_total_servicos']:015}"
        f"{rodape['valor_total_deducoes']:015}\r\n"
    )
    
    # Salva o arquivo
    with open("arquivo_nfts.txt", "w", encoding="iso-8859-1") as f:
        f.writelines(linhas)
    
    return "arquivo_nfts.txt"

# Interface do Streamlit
st.title("Gerador de Arquivo de NFTS em Lote")

# Formulário para Cabeçalho
st.header("Cabeçalho")
versao = st.text_input("Versão do Layout", value="001")
ccm = st.text_input("Inscrição Municipal (CCM)", value="12345678")
data_inicio = st.text_input("Data de Início (AAAAMMDD)", value="20240101")
data_fim = st.text_input("Data de Fim (AAAAMMDD)", value="20240131")

# Formulário para Detalhes
st.header("Detalhes (Registro Tipo 4)")
detalhes = []
with st.expander("Adicionar Detalhe"):
    tipo_doc = st.text_input("Tipo de Documento", value="01")
    serie_doc = st.text_input("Série do Documento", value="A001")
    numero_doc = st.text_input("Número do Documento", value="123456")
    data_servico = st.text_input("Data do Serviço (AAAAMMDD)", value="20240110")
    situacao = st.text_input("Situação (N ou C)", value="N")
    tributacao = st.text_input("Tributação (T, I, J)", value="T")
    valor_servico = st.number_input("Valor do Serviço", min_value=0.0, step=0.01, value=100.00)
    valor_deducoes = st.number_input("Valor das Deduções", min_value=0.0, step=0.01, value=0.00)
    codigo_servico = st.text_input("Código do Serviço", value="0101")
    codigo_subitem = st.text_input("Código Subitem", value="0101")
    aliquota = st.text_input("Alíquota (%)", value="0500")
    iss_retido = st.text_input("ISS Retido (1 ou 2)", value="1")
    indicador_cpf_cnpj = st.text_input("Indicador CPF/CNPJ (1, 2, 3)", value="2")
    cpf_cnpj_prestador = st.text_input("CPF/CNPJ do Prestador", value="12345678000195")

    if st.button("Adicionar Detalhe"):
        detalhes.append({
            "tipo_doc": tipo_doc,
            "serie_doc": serie_doc,
            "numero_doc": numero_doc,
            "data_servico": data_servico,
            "situacao": situacao,
            "tributacao": tributacao,
            "valor_servico": int(valor_servico * 100),
            "valor_deducoes": int(valor_deducoes * 100),
            "codigo_servico": codigo_servico,
            "codigo_subitem": codigo_subitem,
            "aliquota": aliquota,
            "iss_retido": iss_retido,
            "indicador_cpf_cnpj": indicador_cpf_cnpj,
            "cpf_cnpj_prestador": cpf_cnpj_prestador,
        })
        st.success("Detalhe adicionado!")

# Formulário para Rodapé
st.header("Rodapé")
numero_linhas = st.number_input("Número de Linhas de Detalhe", min_value=1, step=1, value=len(detalhes))
valor_total_servicos = st.number_input("Valor Total dos Serviços", min_value=0.0, step=0.01, value=100.00)
valor_total_deducoes = st.number_input("Valor Total das Deduções", min_value=0.0, step=0.01, value=0.00)

# Botão para gerar o arquivo
if st.button("Gerar Arquivo TXT"):
    dados_cabecalho = {
        "versao": versao,
        "ccm": ccm,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }
    rodape = {
        "numero_linhas": numero_linhas,
        "valor_total_servicos": int(valor_total_servicos * 100),
        "valor_total_deducoes": int(valor_total_deducoes * 100),
    }
    arquivo_gerado = gerar_arquivo_txt(dados_cabecalho, detalhes, rodape)
    st.success("Arquivo gerado com sucesso!")
    st.download_button("Baixar Arquivo TXT", data=open(arquivo_gerado, "rb"), file_name=arquivo_gerado)

print('Hello world!')