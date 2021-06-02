from API.Servidor import Arquivista as api_in
from API.Web import Navegador as api_out

local_c, local_e = "colombo", "pr"

servidor = api_in(cidade=local_c, estado=local_e)
web = api_out(cidade=local_c, estado=local_e)

def baixar_previsoes():

    links = servidor.pegar_urls() if servidor.pegar_urls() != {} else web.pegar_urls()

    links_salvos = servidor.salvar_urls(links)
    pasta = servidor.pasta_Downloads
    
    for estado, est_key in links_salvos.items():
        for cidade, cid_key in est_key.items():
            for nome, url in cid_key.items():
                endereco = str(f"{pasta}/{estado}/{cidade}/{nome}")
                print('\nBaixei ->', web.download(url, endereco))

baixar_previsoes()