import streamlit as st
from pypdf import PdfWriter, PdfReader
from streamlit_sortables import sort_items # Nova biblioteca
import io

st.set_page_config(page_title="PDF Master - Unir Documentos", page_icon="📄", layout="wide")

st.title("📄 PDF Master: Unir e Organizar")

# Upload de Arquivos
uploaded_files = st.file_uploader(
    "Escolha os arquivos PDF", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    # Criamos uma lista com os nomes originais para o usuário ordenar
    nomes_arquivos = [f.name for f in uploaded_files]
    
    st.subheader("🔄 Organize a ordem arrastando os itens:")
    st.caption("Clique e arraste os nomes abaixo para definir a sequência final.")
    
    # ESTE É O COMPONENTE DE ARRASTAR:
    ordem_final_nomes = sort_items(nomes_arquivos, direction="vertical")
    
    # Criar um dicionário para recuperar o arquivo original pelo nome
    # (Tratando o caso de arquivos com nomes idênticos)
    file_map = {f.name: f for f in uploaded_files}

    st.markdown("---")

    if st.button("🚀 Gerar PDF Único", use_container_width=True):
        with st.spinner("Unindo PDFs na ordem selecionada..."):
            merger = PdfWriter()
            
            # Percorre a lista na ordem que o usuário deixou após arrastar
            for nome in ordem_final_nomes:
                arquivo = file_map[nome]
                merger.append(arquivo)
            
            output_pdf = io.BytesIO()
            merger.write(output_pdf)
            merger.close()
            
            st.success("✨ PDFs unidos com sucesso!")
            st.download_button(
                label="📥 Baixar PDF Final",
                data=output_pdf.getvalue(),
                file_name="pdf_unificado.pdf",
                mime="application/pdf",
                use_container_width=True
            )
else:
    st.info("Suba seus arquivos PDF para começar.")