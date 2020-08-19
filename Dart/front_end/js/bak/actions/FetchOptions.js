export function getHeaderAuth(username, token, method) {
    return {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'username': username,
            'x-access-token': token,
        }
    }
}
