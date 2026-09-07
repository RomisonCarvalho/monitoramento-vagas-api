
async function buscar_vagas(){
    const listaVagas = document.getElementById('lista-vagas'); 

    listaVagas.classList.remove('mensagem-erro');
    listaVagas.innerHTML = '';

    try {
        const resposta = await fetch('/vagas/');
        
        if (!resposta.ok) {
            throw new Error(`Erro HTTP: ${resposta.status}`);
        }

        const vagas = await resposta.json();

        vagas.sort((a, b) => new Date(b.data) - new Date(a.data));

        const vagasPorCargo = {};
        vagas.forEach(vaga => {
            const cargo = vaga.cargo_buscado;
            if (!vagasPorCargo[cargo]) {
                vagasPorCargo[cargo] = [];
            }
            vagasPorCargo[cargo].push(vaga);
        });

        Object.entries(vagasPorCargo).forEach(([cargo, vagasDoCargo]) => {
            const grupoCargo = document.createElement('div');
            grupoCargo.className = 'grupo-cargo';
            listaVagas.appendChild(grupoCargo);    

            const tituloCargo = document.createElement('h2');
            tituloCargo.className = 'titulo-cargo';
            tituloCargo.textContent = cargo;
            grupoCargo.appendChild(tituloCargo);

            vagasDoCargo.forEach(vaga => {
                const vagaCard = document.createElement('div');
                vagaCard.className = 'vaga-card';

                    const tituloVaga = document.createElement('h3');
                    tituloVaga.textContent = vaga.titulo;
                    vagaCard.appendChild(tituloVaga);

                    const empresaVaga = document.createElement('p');
                    empresaVaga.textContent = vaga.empresa;
                    vagaCard.appendChild(empresaVaga);

                    const vagaInfo = document.createElement('div');
                    vagaInfo.className = 'vaga-info';
                    vagaCard.appendChild(vagaInfo);

                        if (vaga.localizacao && vaga.localizacao !== 'Não informado') {
                            const localizacaoVaga = document.createElement('span');
                            localizacaoVaga.textContent = vaga.localizacao;
                            vagaInfo.appendChild(localizacaoVaga);
                        }   

                        if (vaga.modelo && vaga.modelo !== 'Não informado') {
                            const modeloVaga = document.createElement('span');
                            modeloVaga.textContent = vaga.modelo;
                            vagaInfo.appendChild(modeloVaga);
                        }

                        if (vaga.tipo_vaga && vaga.tipo_vaga !== 'Não informado') {
                            const tipoVaga = document.createElement('span');
                            tipoVaga.textContent = vaga.tipo_vaga;
                            vagaInfo.appendChild(tipoVaga);
                        }
                        if (vaga.afirmativa_pcd && vaga.afirmativa_pcd !== 'Não informado') {
                            const pcdVaga = document.createElement('span');
                            pcdVaga.textContent = vaga.afirmativa_pcd;
                            vagaInfo.appendChild(pcdVaga);
                        }
                        const dataVaga = document.createElement('span');                                        
                        const [ano, mes, dia] = vaga.data.split('-');
                        dataVaga.textContent = `Publicada em ${dia}/${mes}/${ano}`;                                       
                        vagaInfo.appendChild(dataVaga);

                        const linkVaga = document.createElement('a');
                        linkVaga.href = vaga.link;
                        linkVaga.target = '_blank';
                        linkVaga.rel = 'noopener noreferrer';
                        linkVaga.textContent = 'Ver vaga';
                        vagaCard.appendChild(linkVaga);


                grupoCargo.appendChild(vagaCard);   
            });
        });
    }
    catch (erro) {
        console.error('Erro ao carregar vagas:', erro);

        listaVagas.textContent = 'Não foi possível carregar as vagas. Tente novamente mais tarde.';
        listaVagas.classList.add('mensagem-erro');
    }
}

buscar_vagas();