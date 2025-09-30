<?php
require_once 'includes/session.php';

if (!isLoggedIn()) {
  header('Location: index.php');
  exit;
}

$db_file = __DIR__ . '/db/employees.db';
$employees = [];
$search_query = '';
$error = '';

try {
  $pdo = new PDO("sqlite:$db_file");
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  $sql = "SELECT employee_id, name, email, phone, department FROM employees WHERE role_id = 5 AND department = 'Customer Service'";

  if (isset($_GET['search']) && !empty($_GET['search'])) {
    $search_query = $_GET['search'];
    // VULNERABLE: Direct string concatenation for SQLMap exploitation
    $sql = "SELECT employee_id, name, email, phone, department FROM employees WHERE role_id = 5 AND department = 'Customer Service' AND name LIKE '%{$search_query}%'";
  }

  $result = $pdo->query($sql);
  $employees = $result->fetchAll(PDO::FETCH_ASSOC);

} catch (Exception $e) {
  $error = 'Database error: ' . $e->getMessage();
}

$current_user = getAuthFromCookie();
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VMM Employee Directory</title>
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
      background: #f5f5f5;
      min-height: 100vh;
    }

    .navbar {
      background: var(--vmm-red);
      color: white;
      padding: 15px 0;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .nav-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .nav-brand {
      font-size: 1.8em;
      font-weight: 700;
    }

    .nav-links {
      display: flex;
      gap: 20px;
      align-items: center;
    }

    .nav-links a {
      color: white;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    .nav-links a:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .container {
      max-width: 1200px;
      margin: 40px auto;
      padding: 0 20px;
    }

    .welcome {
      background: white;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 30px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .search-section {
      background: white;
      padding: 25px;
      border-radius: 10px;
      margin-bottom: 30px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .search-form {
      display: flex;
      gap: 15px;
      align-items: end;
    }

    .form-group {
      flex: 1;
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
    }

    .search-btn {
      background: var(--vmm-blue);
      color: white;
      border: none;
      padding: 12px 25px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      height: fit-content;
    }

    .search-btn:hover {
      background: #003d7a;
    }

    .employees-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
    }

    .employee-card {
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s;
    }

    .employee-card:hover {
      transform: translateY(-5px);
    }

    .employee-name {
      color: var(--vmm-red);
      font-size: 1.3em;
      font-weight: 600;
      margin-bottom: 10px;
    }

    .employee-info {
      color: #666;
      margin-bottom: 8px;
    }

    .employee-id {
      background: var(--vmm-blue);
      color: white;
      padding: 4px 12px;
      border-radius: 15px;
      font-size: 0.9em;
      display: inline-block;
      margin-top: 10px;
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
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">VMM EMS</div>
      <div class="nav-links">
        <a href="search.php">Directory</a>
        <a href="review.php">Reviews</a>
        <span>Welcome, <?php echo htmlspecialchars($current_user['name']); ?></span>
        <a href="logout.php">Logout</a>
      </div>
    </div>
  </nav>

  <div class="container">
    <div class="welcome">
      <h2>Customer Support Team Directory</h2>
      <p>Search through our Customer Support team members. Contact them for any assistance you need!</p>
    </div>

    <div class="search-section">
      <form class="search-form" method="GET">
        <div class="form-group">
          <label for="search">Search Customer Support Employee by Name (from the <code>employees</code> table)</label>
          <input type="text" id="search" name="search" value="<?php echo htmlspecialchars($search_query); ?>"
            placeholder="Enter employee name...">
        </div>
        <button type="submit" class="search-btn">Search</button>
      </form>
    </div>

    <?php if ($error): ?>
      <div class="error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <div class="employees-grid">
      <?php foreach ($employees as $employee): ?>
        <div class="employee-card">
          <div class="employee-name"><?php echo htmlspecialchars($employee['name']); ?></div>
          <div class="employee-info">📧 <?php echo htmlspecialchars($employee['email']); ?></div>
          <div class="employee-info">📞 <?php echo htmlspecialchars($employee['phone']); ?></div>
          <div class="employee-info">🏢 <?php echo htmlspecialchars($employee['department']); ?></div>
          <div class="employee-id"><?php echo htmlspecialchars($employee['employee_id']); ?></div>
        </div>
      <?php endforeach; ?>
    </div>

    <?php if (empty($employees) && !$error): ?>
      <div style="text-align: center; padding: 40px; color: #666;">
        <h3>No employees found</h3>
        <p>Try adjusting your search criteria.</p>
      </div>
    <?php endif; ?>
  </div>
</body>

</html>