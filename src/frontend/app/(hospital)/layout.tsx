import Nav from '@/components/nav';
import Auth from '../(landing)/auth';
import { redirect } from 'next/navigation'

export default async function RootLayout({
    children,
}: {
    children: React.ReactNode;
    }) {
    const auth = await Auth();
    if (auth === null) {
        redirect("/auth")
    }
    return (
        <>
            <Nav />
            {children}
        </>
    );
}
