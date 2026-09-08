import "../global.css"

export function Sobre() {
    return (
        <div>
            <h1 className="text-center m-3">Sobre</h1>
            <div className="accordion" id="accordion">
                <div className="accordion-item d-flex flex-column my-5 rounded-4 w-75 mx-auto">
                    <h1 className="accordion-header text-black mb-3">
                        <button className="accordion-button bg-verde-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            Sobre Nós
                        </button>
                    </h1>
                    <div id="collapseOne" className="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                        <div className="accordion-body fs-3">
                            <strong>Farmework </strong>é uma empresa especializada em soluções
                            tecnológicas para o setor agroindustrial. Nosso
                            propósito é transformar o campo por meio da inovação,
                            conectando o agronegócio à era digital com
                            ferramentas inteligentes, acessíveis e sustentáveis.
                        </div>
                    </div>
                </div>
                <div className="accordion-item d-flex flex-column my-5 rounded-4 w-75 mx-auto">
                    <h1 className="accordion-header text-black mb-3">
                        <button className="accordion-button bg-verde-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                            Equipe
                        </button>
                    </h1>
                    <div id="collapseTwo" className="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                        <div className="accordion-body fs-3">
                            <div className="d-flex flex-wrap">
                                <div className="px-3">
                                    <h2><b>Rafael</b></h2>
                                    <p className="fs-3">Representante Comercial</p>
                                </div>
                                <div className="px-3 border-black border-start">
                                    <h2><b>Kelvin</b></h2>
                                    <p className="fs-3">Engenheiro de IA</p>
                                </div>
                                <div className="px-3 border-black border-start">
                                    <h2><b>Igor</b></h2>
                                    <p className="fs-3">Desenvolvedor Eletrônico</p>
                                </div>
                                <div className="px-3 border-black border-start">
                                    <h2><b>João Vitor</b></h2>
                                    <p className="fs-3">Desenvolvedor Fullstack</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}