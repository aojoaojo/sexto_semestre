import '../global.css';

interface CardOverCarrosselProps {
    titulo: string;
    texto: string;
}

export function CardOverCarrossel({ titulo, texto }: CardOverCarrosselProps) {
    return (
        <div className='position-absolute top-50 start-50 translate-middle w-75 bg-verde-3 rounded-5 text-center'>
            <h1 className='mx-5 mt-3'>{titulo}</h1>
            <p className='mx-5 fs-3'>{texto}</p>
        </div>
    )
}