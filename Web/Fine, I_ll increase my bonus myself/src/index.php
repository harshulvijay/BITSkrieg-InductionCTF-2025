<?php
require_once 'includes/session.php';
require_once 'includes/db_init.php';

$error = '';

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = $_POST['username'] ?? '';
  $password = $_POST['password'] ?? '';

  try {
    $pdo = getDatabaseConnection();
    // VULNERABLE: Direct string concatenation for SQLMap exploitation
    $sql = "SELECT employee_id, name, username, role_id, department FROM employees WHERE username = '{$username}' AND password = '{$password}'";
    $result = $pdo->query($sql);
    $user = $result->fetch(PDO::FETCH_ASSOC);

    if ($user) {
      setAuthCookie($user);
      header('Location: search.php');
      exit;
    } else {
      $error = 'Invalid username or password';
    }
  } catch (Exception $e) {
    $error = 'Database error: ' . $e->getMessage();
  }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VMM Employee Portal - Login</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    :root {
      --vmm-red: #d9232d;
      --vmm-blue: #004a99;
      --vmm-gold: #ffd700;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, var(--vmm-red), var(--vmm-blue));
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .login-container {
      background: white;
      padding: 40px;
      border-radius: 15px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
      text-align: center;
    }

    .logo {
      color: var(--vmm-red);
      font-size: 2.5em;
      font-weight: 700;
      margin-bottom: 10px;
    }

    .subtitle {
      color: var(--vmm-blue);
      margin-bottom: 30px;
      font-weight: 500;
    }

    .form-group {
      margin-bottom: 20px;
      text-align: left;
    }

    .form-group label {
      display: block;
      margin-bottom: 8px;
      color: var(--vmm-blue);
      font-weight: 600;
    }

    .form-group input {
      width: 100%;
      padding: 12px 15px;
      border: 2px solid #e1e1e1;
      border-radius: 8px;
      font-size: 1em;
      transition: border-color 0.3s;
    }

    .form-group input:focus {
      outline: none;
      border-color: var(--vmm-blue);
    }

    .login-btn {
      width: 100%;
      background: var(--vmm-red);
      color: white;
      border: none;
      padding: 15px;
      border-radius: 8px;
      font-size: 1.1em;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
    }

    .login-btn:hover {
      background: #b81e25;
      transform: translateY(-2px);
    }

    .error {
      background: #f8d7da;
      color: #721c24;
      padding: 15px;
      border-radius: 8px;
      margin-bottom: 20px;
      border: 1px solid #f5c6cb;
    }
  </style>
</head>

<body>
  <div class="login-container">
    <div class="logo">VMM Portal</div>
    <div class="subtitle">Vishal Mega Mart - Employee Directory</div>

    <?php if ($error): ?>
      <div class="error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <form method="POST">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
      </div>
      <button type="submit" class="login-btn">Access Employee Directory</button>
    </form>
  </div>
</body>

</html>