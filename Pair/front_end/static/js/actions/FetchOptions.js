export function getHeaderAuth(username, token) {
    return {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'username': username,
        'x-access-token': token,
    }
}
