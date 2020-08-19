export function getHeaderAuth(email, token) {
    return {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'email': email,
        'x-access-token': token,
    }
}
