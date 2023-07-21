import { cookies } from 'next/headers';

async function Auth() {
    const doc_id = cookies().get('doc_id')?.value
    if (doc_id) {
        const password = cookies().get('password')?.value;
        const response = await fetch('http://127.0.0.1:5000/signin', {
            method: 'POST',
            body: JSON.stringify({
                doc_id: doc_id,
                password: password,
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        return data;
    }
    return null;
}

export default Auth;
