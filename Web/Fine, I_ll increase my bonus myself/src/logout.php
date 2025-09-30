<?php
require_once 'includes/session.php';
clearAuthCookies();
header('Location: index.php');
exit;
?>