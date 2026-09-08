import { createBrowserRouter } from "react-router";
import { Sobre } from "./components/sobre";
import { Home } from "./pages/home";
import { Layout } from "./_layout/layout";
import { Servicos } from "./pages/servicos";

export const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout />,
        children: [
            { path: '/', element: <Home /> },
            { path: '/sobre', element: <Sobre /> },
            { path: '/servicos', element: <Servicos /> },
            { path: '/contato', element: <div>Contato</div> },
        ]
    },
]);