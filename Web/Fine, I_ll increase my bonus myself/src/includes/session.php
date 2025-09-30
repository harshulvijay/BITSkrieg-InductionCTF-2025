<?php
// Cookie-based authentication instead of sessions

function setAuthCookie($user_data) {
    $cookie_value = base64_encode(json_encode($user_data));
    setcookie('vmm_auth', $cookie_value, time() + 3600, '/'); // 1 hour expiry
    setcookie('vmm_logged_in', 'true', time() + 3600, '/');
    setcookie('vmm_is_admin', ($user_data['role_id'] == 2 ? 'true' : 'false'), time() + 3600, '/');
}

function getAuthFromCookie() {
    if (isset($_COOKIE['vmm_auth'])) {
        $cookie_data = json_decode(base64_decode($_COOKIE['vmm_auth']), true);
        return $cookie_data;
    }
    return null;
}

function isLoggedIn() {
    return isset($_COOKIE['vmm_logged_in']) && $_COOKIE['vmm_logged_in'] === 'true';
}

function isAdmin() {
    return isset($_COOKIE['vmm_is_admin']) && $_COOKIE['vmm_is_admin'] === 'true';
}

function clearAuthCookies() {
    setcookie('vmm_auth', '', time() - 3600, '/');
    setcookie('vmm_logged_in', '', time() - 3600, '/');
    setcookie('vmm_is_admin', '', time() - 3600, '/');
}
?>
