import { Carrossel } from "../components/carrossel";
import { Sobre } from "../components/sobre";
import { Servicos } from "./servicos";

export function Home() {
    return (
        <>
            <Carrossel />
            <Servicos />
            <Sobre />
        </>
    )
}